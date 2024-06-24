from BinanceVolatilityBot.BinanceVolatilityBot import (
    get_candles,
    calculate_ema,
    calculate_bollinger_bands,
    stochastic_rsi,
    calculate_rsi,
    send_to_telegram
)
import datetime

def test_binance_volatility_bot(exchange, symbol, timeframe, k_value):
    # 변동성 조건 임의 계산
    df = get_candles(exchange, symbol, timeframe=timeframe, limit=100)
    range_value = (df['high'].iloc[-2] - df['low'].iloc[-2]) * k_value
    target_long = df['close'].iloc[-2] + range_value
    target_short = df['close'].iloc[-2] - range_value

    # ema 계산
    ema_9 = calculate_ema(df, 9)
    ema_21 = calculate_ema(df, 21)
    ema_54 = calculate_ema(df, 54)

    # 볼린저 밴드 계산
    upper_band, lower_band = calculate_bollinger_bands(df, window=20, num_std_dev=2.5)

    # 스토캐스틱 RSI 계산
    stoch_rsi_k, stoch_rsi_d = stochastic_rsi(df, period=14, smooth_k=3, smooth_d=3)

    # RSI 계산
    rsi = calculate_rsi(df, period=14)

    # 결과 출력
    print(f"UTC : {datetime.datetime.now()}")
    print(f"range : {range_value}\ntarget_long : {target_long}\ntarget_short : {target_short}\nema_9 : {ema_9.iloc[-1]}\nema_21 : {ema_21.iloc[-1]}\nema_54 : {ema_54.iloc[-1]}\nupper_band, lower_band : {upper_band.iloc[-1], lower_band.iloc[-1]}\nstoch_rsi_k, stoch_rsi_d : {stoch_rsi_k.iloc[-1], stoch_rsi_d.iloc[-1]}\nrsi : {rsi['rsi'].iloc[-1]}\n종가 : {df['close'].iloc[-1]}")
    
    # Telegram으로 메시지 전송
    send_to_telegram("테스트 중")

    print("테스트 정상 완료")

if __name__ == "__main__":
    exchange = "your_exchange_name"
    symbol = "BTCUSDT"
    timeframe = "1h"
    k_value = 0.5  # 예시로 임의의 k_value 설정

    test_binance_volatility_bot(exchange, symbol, timeframe, k_value)
