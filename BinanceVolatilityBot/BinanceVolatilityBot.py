import pandas as pd
import ccxt
import time
import datetime
import schedule
from pmdarima import auto_arima
import telepot
from telepot.loop import MessageLoop


# Binance API키 설정
from binance_keys import api_key, api_secret

#텔레그램 봇
from telepot_bot_id import token, chat_id
bot = telepot.Bot(token)

# Binance API 설정
exchange = ccxt.binance({
    'rateLimit': 1000,
    'enableRateLimit': True,
    'apiKey': api_key,
    'secret': api_secret,
    'options': {
        'defaultType': 'future'
    }
})

# 트레이딩 페어 및 타임프레임 설정
symbol = 'ETHUSDT'
timeframe = '6h'

# 레버리지 설정
leverage = 4
exchange.fapiPrivatePostLeverage({'symbol': symbol, 'leverage': leverage*2+2})

# 텔레그램으로 메시지를 보내는 함수
def send_to_telegram(message):
    try:
        bot.sendMessage(chat_id, message)
    except Exception as e:
        send_to_telegram(f"An error occurred while sending to Telegram: {e}")


Profit_Percentage = 150
stop = False
k_value = 0.55
postponement = False
execute_volatility_breakout_strategy = True
execute_ema_trading_strategy = True
execute_scalping_strategy = True
def handle(msg):
    global stop, k_value, leverage, Profit_Percentage, start, postponement, execute_volatility_breakout_strategy, execute_ema_trading_strategy, execute_scalping_strategy
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] == '/start':
            if postponement == True: 
                send_to_telegram("거래 재개")
                postponement = False
            else : 
                send_to_telegram('Starting...')
                stop = False
                start = True
        elif msg['text'] == '/stop':
            send_to_telegram('Stopping...')
            stop = True
        elif msg['text'] == '/help':
            send_to_telegram(f'/start - 시작\n/stop - 중지\n/leverage(num) - leverage값을 설정\n 현재 leverage값 : {leverage}\n/set(k) - k 값을 설정\n 현재 k값 : {k_value}\n/Profit_Percentage(num) - 익절 수치를 설정\n 현재 Profit_Percentage값 : {Profit_Percentage}->{round(100/Profit_Percentage,2)}%\n/predict - 예언하기\n/Condition_fulfillment_symbols - 조건 충족 코인\n/execute_and_stop - 전략별 실행 및 중지\n/postponing_trading - 거래연기하기')
        elif msg['text'] == '/predict':
            send_to_telegram(f'/predict_3m - 3분뒤 가격예측\n/predict_5m - 5분뒤 가격예측\n/predict_15m - 15분뒤 가격예측\n/predict_30m - 30분뒤 가격예측\n/predict_1h - 1시간뒤 가격예측\n/predict_6h - 6시간뒤 가격예측\n/predict_1d - 1일뒤 가격예측')
        elif msg['text'] == '/postponing_trading':
            postponement = True
            postpone_trading()
        elif msg['text'] =='/execute_and_stop':
            send_to_telegram("/execute_volatility_breakout_strategy - 변동성 돌파 전략을 실행\n/execute_ema_trading_strategy - EMA 기반 트레이딩 전략을 실행\n/execute_scalping_strategy - stochastic_rsi단타 전략을 실행\n/stop_volatility_breakout_strategy - 변동성 돌파 전략을 중지\n/stop_ema_trading_strategy - EMA 기반 트레이딩 전략을 중지\n/stop_scalping_strategy - stochastic_rsi단타 전략을 중지")
        elif msg['text'] =='/execute_volatility_breakout_strategy':
            send_to_telegram("변동성 돌파 전략을 실행합니다.")
            execute_volatility_breakout_strategy = True
        elif msg['text'] =='/execute_ema_trading_strategy':
            send_to_telegram("EMA 기반 트레이딩 전략을 실행합니다.")
            execute_ema_trading_strategy = True
        elif msg['text'] =='/execute_scalping_strategy':
            send_to_telegram("stochastic_rsi단타 전략을 실행합니다.")
            execute_scalping_strategy = True
        elif msg['text'] =='/stop_volatility_breakout_strategy':
            send_to_telegram("변동성 돌파 전략을 중지합니다.")
            execute_volatility_breakout_strategy = False
        elif msg['text'] =='/stop_ema_trading_strategy':
            send_to_telegram("EMA 기반 트레이딩 전략을 중지합니다.")
            execute_ema_trading_strategy = False
        elif msg['text'] =='/stop_scalping_strategy':
            send_to_telegram("stochastic_rsi단타 전략을 중지합니다.")
            execute_scalping_strategy = False
        elif msg['text'] == '/leverage':
            send_to_telegram('/leverage(1~10)')
        elif msg['text'] == '/leverage(1)':
            leverage = 1
        elif msg['text'] == '/leverage(2)':
            leverage = 2
        elif msg['text'] == '/leverage(3)':
            leverage = 3
        elif msg['text'] == '/leverage(4)':
            leverage = 4
        elif msg['text'] == '/leverage(5)':
            leverage = 5
        elif msg['text'] == '/leverage(6)':
            leverage = 6
        elif msg['text'] == '/leverage(7)':
            leverage = 7
        elif msg['text'] == '/leverage(8)':
            leverage = 8
        elif msg['text'] == '/leverage(9)':
            leverage = 9
        elif msg['text'] == '/leverage(10)':
            leverage = 10
            
        elif msg['text'] == '/set':
            send_to_telegram('0.2 ~ 0.75 까지 0.05단위로 k값 설정')
        elif msg['text'] == '/set(0.2)':
            k_value = 0.2
        elif msg['text'] == '/set(0.25)':
            k_value = 0.25
        elif msg['text'] == '/set(0.3)':
            k_value = 0.3
        elif msg['text'] == '/set(0.35)':
            k_value = 0.35
        elif msg['text'] == '/set(0.4)':
            k_value = 0.4
        elif msg['text'] == '/set(0.45)':
            k_value = 0.45
        elif msg['text'] == '/set(0.5)':
            k_value = 0.5
        elif msg['text'] == '/set(0.55)':
            k_value = 0.55
        elif msg['text'] == '/set(0.6)':
            k_value = 0.6
        elif msg['text'] == '/set(0.65)':
            k_value = 0.65
        elif msg['text'] == '/set(0.7)':
            k_value = 0.7
        elif msg['text'] == '/set(0.75)':
            k_value = 0.75
        elif msg['text'] == '/Profit_Percentage':
            send_to_telegram('/Profit_Percentage(100) # 1.00\n/Profit_Percentage(110) # 0.91\n/Profit_Percentage(120) # 0.83\n/Profit_Percentage(130) # 0.77\n/Profit_Percentage(140) # 0.71\n/Profit_Percentage(150) # 0.67\n/Profit_Percentage(160) # 0.62\n/Profit_Percentage(170) # 0.59\n/Profit_Percentage(180) # 0.56\n/Profit_Percentage(190) # 0.53\n/Profit_Percentage(200) # 0.50')
        elif msg['text'] == '/Profit_Percentage(100)':
            Profit_Percentage = 100 # 1
        elif msg['text'] == '/Profit_Percentage(110)':
            Profit_Percentage = 110 # 0.9090909...
        elif msg['text'] == '/Profit_Percentage(120)':
            Profit_Percentage = 120 # 0.833333...
        elif msg['text'] == '/Profit_Percentage(130)':
            Profit_Percentage = 130 # 0.769230...
        elif msg['text'] == '/Profit_Percentage(140)':
            Profit_Percentage = 140 # 0.714285...
        elif msg['text'] == '/Profit_Percentage(150)':
            Profit_Percentage = 150 # 0.666666...
        elif msg['text'] == '/Profit_Percentage(160)':
            Profit_Percentage = 160 # 0.625
        elif msg['text'] == '/Profit_Percentage(170)':
            Profit_Percentage = 170 # 0.588235...
        elif msg['text'] == '/Profit_Percentage(180)':
            Profit_Percentage = 180 # 0.555555...
        elif msg['text'] == '/Profit_Percentage(190)':
            Profit_Percentage = 190 # 0.526315...
        elif msg['text'] == '/Profit_Percentage(200)':
            Profit_Percentage = 200 # 0.5   
        elif msg['text'] == '/predict_6h':
            send_to_telegram('모델학습 및 예측 중...')
            predict_price(prediction_time='6h')
            send_to_telegram(f'predicted_high_price -> {predicted_high_price}')
            send_to_telegram(f'predicted_low_price -> {predicted_low_price}')
            send_to_telegram(f'predicted_close_price -> {predicted_close_price}')
        elif msg['text'] == '/predict_3m':
            send_to_telegram('모델학습 및 예측 중...')
            predict_price(prediction_time='3m')
            send_to_telegram(f'predicted_high_price -> {predicted_high_price}')
            send_to_telegram(f'predicted_low_price -> {predicted_low_price}')
            send_to_telegram(f'predicted_close_price -> {predicted_close_price}')
        elif msg['text'] == '/predict_5m':
            send_to_telegram('모델학습 및 예측 중...')
            predict_price(prediction_time='5m')
            send_to_telegram(f'predicted_high_price -> {predicted_high_price}')
            send_to_telegram(f'predicted_low_price -> {predicted_low_price}')
            send_to_telegram(f'predicted_close_price -> {predicted_close_price}')
        elif msg['text'] == '/predict_15m':
            send_to_telegram('모델학습 및 예측 중...')
            predict_price(prediction_time='15m')
            send_to_telegram(f'predicted_high_price -> {predicted_high_price}')
            send_to_telegram(f'predicted_low_price -> {predicted_low_price}')
            send_to_telegram(f'predicted_close_price -> {predicted_close_price}')
        elif msg['text'] == '/predict_30m':
            send_to_telegram('모델학습 및 예측 중...')
            predict_price(prediction_time='30m')
            send_to_telegram(f'predicted_high_price -> {predicted_high_price}')
            send_to_telegram(f'predicted_low_price -> {predicted_low_price}')
            send_to_telegram(f'predicted_close_price -> {predicted_close_price}')
        elif msg['text'] == '/predict_1h':
            send_to_telegram('모델학습 및 예측 중...')
            predict_price(prediction_time='1h')
            send_to_telegram(f'predicted_high_price -> {predicted_high_price}')
            send_to_telegram(f'predicted_low_price -> {predicted_low_price}')
            send_to_telegram(f'predicted_close_price -> {predicted_close_price}')
        elif msg['text'] == '/predict_1d':
            send_to_telegram('모델학습 및 예측 중...')
            predict_price(prediction_time='1d')
            send_to_telegram(f'predicted_high_price -> {predicted_high_price}')
            send_to_telegram(f'predicted_low_price -> {predicted_low_price}')
            send_to_telegram(f'predicted_close_price -> {predicted_close_price}')

        elif msg['text'] == '/Condition_fulfillment_symbols':
            symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT", "DOTUSDT", "LTCUSDT", "MATICUSDT", "AVAXUSDT", "SHIBUSDT", "FILUSDT", "INJUSDT", "FETUSDT" ]
            filtered_symbols = filter_symbols(symbols)
            send_to_telegram(filtered_symbols)
# 텔레그램 메시지 루프
MessageLoop(bot, handle).run_as_thread()

def postpone_trading():
    global postponement, stop, delay_time
    now = datetime.datetime.now()
    delay_time = datetime.datetime(now.year, now.month, now.day, now.hour, 0)
    if stop == False:
        send_to_telegram(f"UTC : {delay_time + datetime.timedelta(hours=(6 - delay_time.hour % 6))}까지 거래 연기")
        stop = True
    if (now >= delay_time + datetime.timedelta(hours=(6 - delay_time.hour % 6))):
        send_to_telegram("거래 재개")
        postponement = False
        stop = False

# 매수 및 매도 주문 함수 정의
def place_limit_order(symbol, side, amount, price):
    order = exchange.create_order(
        symbol=symbol,
        type="LIMIT",
        side=side,
        amount=amount,
        price=price
    )
    return order

#시장가 주문
def place_market_order(symbol, side, amount):
    order = exchange.create_order(
        symbol=symbol,
        type="MARKET",
        side=side,
        amount=amount
    )
    return order

# 전체 잔액 정보 조회
def get_balance():
    balance = exchange.fetch_balance(params={"type": "future"})
    return balance

# 매매량 계산 함수 정의
def calculate_quantity(symbol):
    try:
        balance = get_balance()
        total_balance = float(balance['total']['USDT'])
        
        # 현재 BTCUSDT 가격 조회
        ticker = exchange.fetch_ticker(symbol)
        btc_price = float(ticker['last'])
        
        # USDT 잔고를 BTC로 환산
        quantity = total_balance / btc_price 
        
        # 소수점 이하 자리 제거
        quantity = round(quantity, 3)
        
        return quantity
    except Exception as e:
        error_message = f"An error occurred while calculating the quantity: {e}"
        send_to_telegram(error_message)
        return None

predicted_close_price = 0

def get_candles(exchange, symbol, timeframe='6h', limit=100):
    candles = exchange.fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        since=None,
        limit=limit
    )
    df = pd.DataFrame(data=candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def predict_price(prediction_time='1h'):
    """Auto ARIMA로 다음 종가, 고가, 저가 가격 예측"""

    df = get_candles(exchange, symbol, timeframe=prediction_time, limit=200)

    global predicted_close_price, predicted_high_price, predicted_low_price
    
    # ARIMA 모델에 사용할 열 선택 및 이름 변경
    df = df.rename(columns={'timestamp': 'ds', 'open': 'open', 'high': 'high', 'low': 'low', 'close': 'y', 'volume': 'volume'})
    
    # 데이터프레임에서 시간 열을 인덱스로 설정
    df.set_index('ds', inplace=True)
    
    # Auto ARIMA 모델 초기화 및 학습
    model = auto_arima(df['y'], seasonal=False, suppress_warnings=True)
    
    # 다음 n분 후를 예측할 데이터 포인트 생성
    if prediction_time == '6h':
        minutes_to_add = 60*6
    elif prediction_time == '3m':
        minutes_to_add = 3
    elif prediction_time == '5m':
        minutes_to_add = 5
    elif prediction_time == '15m':
        minutes_to_add = 15
    elif prediction_time == '30m':
        minutes_to_add = 30
    elif prediction_time == '1h':
        minutes_to_add = 60
    elif prediction_time == '1d':
        minutes_to_add = 24 * 60
        
    future = pd.DataFrame(index=[df.index[-1] + pd.Timedelta(minutes=minutes_to_add)])
    future['open'] = df['open'].iloc[-1]
    future['high'] = df['high'].iloc[-1]
    future['low'] = df['low'].iloc[-1]
    future['volume'] = df['volume'].iloc[-1]
    
    # 예측 수행
    forecast, conf_int = model.predict(n_periods=1, exogenous=[future.values], return_conf_int=True)
    
    # 예측된 종가, 고가, 저가 출력
    close_value = forecast[0]
    predicted_close_price = close_value
    
    # 다음과 같이 최대값과 최소값을 구할 수 있습니다.
    predicted_high_price = conf_int[0][1]
    predicted_low_price = conf_int[0][0]

# Bollinger Bands 계산 함수 정의
def calculate_bollinger_bands(data, window, num_std_dev):
    rolling_mean = data['close'].rolling(window=window).mean()
    rolling_std = data['close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)
    return upper_band, lower_band

def calculate_ema(data, period):
    ema = data['close'].ewm(span=period, adjust=False).mean()
    return ema

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    data['rsi'] = rsi
    return data

def stochastic_rsi(data, period=14, smooth_k=3, smooth_d=3):
    """
    스토케스틱 RSI를 계산하는 함수.

    매개변수:
    - data: 'high', 'low', 'close' 열을 포함한 DataFrame.
    - period: RSI 기간 (기본값은 14).
    - smooth_k: %K를 부드럽게 만들기 위한 기간 (기본값은 3).
    - smooth_d: %D를 부드럽게 만들기 위한 기간 (기본값은 3).
    반환값:
    - 'stoch_rsi_k' 및 'stoch_rsi_d'.
    """
    # RSI 계산
    data = calculate_rsi(data, period+1)

    # 스토케스틱 RSI (%K) 계산
    min_rsi = data['rsi'].rolling(window=period, center = False).min()
    max_rsi = data['rsi'].rolling(window=period, center = False).max()
    stoch = 100 * (data['rsi'] - min_rsi) / (max_rsi - min_rsi)
    stoch_rsi_k = stoch.rolling(window=smooth_k, center = False).mean()
    # 스토케스틱 RSI (%D) 계산
    stoch_rsi_d = stoch_rsi_k.rolling(window=smooth_d, center = False).mean()

    return stoch_rsi_k, stoch_rsi_d

def is_doji_candle(df, threshold=0.2):
    price_range = df['high'].iloc[-2] - df['low'].iloc[-2]
    body_range = abs(df['open'].iloc[-2] - df['close'].iloc[-2])

    # 도지 캔들 판별 조건
    if body_range < threshold * price_range:
        return True
    else: 
        return False

def calculate_volume_oscillator(data):
    short_ema = data.ewm(span=5, adjust=False).mean()
    long_ema = data.ewm(span=10, adjust=False).mean()
    oscillator = (short_ema - long_ema) / short_ema * 100
    return oscillator

def reset_signals():
    global waiting_sell_signal, waiting_buy_signal
    global waiting_ema_buy_signal
    global waiting_ema_sell_signal
    waiting_sell_signal = False
    waiting_buy_signal = False
    waiting_ema_buy_signal = False
    waiting_ema_sell_signal = False

schedule.every().day.at("00:01").do(reset_signals)
schedule.every().day.at("06:01").do(reset_signals)
schedule.every().day.at("12:01").do(reset_signals)
schedule.every().day.at("18:01").do(reset_signals)

signal = False
buy_signal = False
sell_signal = False
waiting_buy_signal = False
waiting_sell_signal = False
# 변동성 돌파 전략을 적용한 매매 로직
def volatility_breakout_strategy(symbol, df, k_value):
    # 변동성 돌파 전략
    global range
    global target_long
    global target_short
    global waiting_buy_signal
    global waiting_sell_signal
    global buy_signal
    global sell_signal
    global predicted_buy_low_price
    global predicted_sell_high_price
    global entry_time
    global long_stop_loss
    global short_stop_loss
    global future_close_price
    global long_quantity
    global short_quantity
    global limit_order
    global buy_price
    global sell_price
    global profit
    
    # 변동성 범위 계산
    range = (df['high'].iloc[-2] - df['low'].iloc[-2]) * k_value
    # 롱(매수) 목표가 및 숏(매도) 목표가 설정
    target_long = df['close'].iloc[-2] + range
    target_short = df['close'].iloc[-2] - range
    target_long2 = (df['close'].iloc[-2] + range + 0.3)
    target_short2 = (df['close'].iloc[-2] - range + 0.3)
    stoch_rsi_k, stoch_rsi_d = stochastic_rsi(df, period=14, smooth_k=3, smooth_d=3)
    is_doji=is_doji_candle(df)
    if (df['high'].iloc[-1] > target_long2) or (df['low'].iloc[-1] < target_short2):
        is_doji = False
    # 매수 및 매도 주문 로직
    if buy_signal == False and is_doji == False:
        if stoch_rsi_k.iloc[-2]<100 and stoch_rsi_d.iloc[-2] < 95:
            # 어제 종가보다 오늘 시가가 높고, 오늘 고가가 목표 롱 가격을 돌파한 경우 혹은 역추세 돌파시
            if (df['open'].iloc[-2] < df['close'].iloc[-2]) or (df['high'].iloc[-1] > target_long2):
                if df['high'].iloc[-1] > target_long:
                    if waiting_buy_signal == False:
                        if df['high'].iloc[-1] > target_long2:
                            predict_price(prediction_time='15m')
                            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
                            send_to_telegram(f"돌파가격 : {target_long}")
                            predicted_buy_low_price = predicted_low_price
                            send_to_telegram(f"최적매수가격 : {predicted_buy_low_price}")
                            waiting_buy_signal = True
                        else:
                            # 15분 뒤 가격 예측 및 텔레그램 전송
                            predict_price(prediction_time='5m')
                            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
                            send_to_telegram(f"돌파가격 : {target_long}")
                            predicted_buy_low_price = predicted_low_price
                            send_to_telegram(f"최적매수가격 : {predicted_buy_low_price}")
                            waiting_buy_signal = True
                    # 현재 가격이 예측한 최적 매수가격보다 낮으면 매수 주문 실행
                    if df['close'].iloc[-1] < predicted_buy_low_price:
                        long_stop_loss = (df['low'].iloc[-1] + df['open'].iloc[-2])/2 
                        buy_price = df['close'].iloc[-1]
                        if long_stop_loss > buy_price:
                            send_to_telegram(f"손절가보다 매수가격이 더 작기에 최적매수가격을 재지정합니다.")
                            predict_price(prediction_time='3m')
                            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
                            send_to_telegram(f"돌파가격 : {target_long}")
                            predicted_buy_low_price = predicted_low_price
                            send_to_telegram(f"최적매수가격 : {predicted_buy_low_price}")
                        else:
                            long_quantity = calculate_quantity(symbol) * (leverage - 0.2)
                            limit_order = place_limit_order(symbol, 'buy', long_quantity, df['close'].iloc[-1])
                            send_to_telegram(f"매수 - Price: {buy_price}, Quantity: {long_quantity}")
                            send_to_telegram(f"손절가 - {long_stop_loss}")
                            buy_signal = True
                            upper_band, lower_band = calculate_bollinger_bands(df, window=20, num_std_dev=2.5)
                            future_close_price = upper_band.iloc[-1] # 과매수
                            now = datetime.datetime.now()
                            entry_time = datetime.datetime(now.year, now.month, now.day, now.hour, 0)

    if sell_signal == False and is_doji == False:
        if stoch_rsi_k.iloc[-2] > 0 and stoch_rsi_d.iloc[-2] > 5:
            # 어제 종가보다 오늘 시가가 낮고, 오늘 저가가 목표 숏 가격을 돌파한 경우 혹은 역추세 돌파시
            if (df['open'].iloc[-2] > df['close'].iloc[-2]) or (df['low'].iloc[-1] < target_short2):
                if df['low'].iloc[-1] < target_short:
                    if waiting_sell_signal == False:
                        if df['low'].iloc[-1] < target_short2:
                            predict_price(prediction_time='15m')
                            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
                            send_to_telegram(f"돌파가격 : {target_short}")
                            predicted_sell_high_price = predicted_high_price
                            send_to_telegram(f"최적매도가격 : {predicted_sell_high_price}")
                            waiting_sell_signal = True
                        else:
                        # 15분 뒤 가격 예측 및 텔레그램 전송
                            predict_price(prediction_time='5m')
                            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
                            send_to_telegram(f"돌파가격 : {target_short}")
                            predicted_sell_high_price = predicted_high_price
                            send_to_telegram(f"최적매도가격 : {predicted_sell_high_price}")
                            waiting_sell_signal = True
                    # 현재 가격이 예측한 최적 매도가격보다 높으면 매도 주문 실행
                    if df['close'].iloc[-1] > predicted_sell_high_price:
                        short_stop_loss = (df['high'].iloc[-1] + df['open'].iloc[-2])/2
                        sell_price = df['close'].iloc[-1]
                        if short_stop_loss < sell_price:
                            send_to_telegram(f"손절가보다 매도가격이 더 크기에 최적매도가격을 재지정합니다.")
                            predict_price(prediction_time='3m')
                            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
                            send_to_telegram(f"돌파가격 : {target_short}")
                            predicted_sell_high_price = predicted_high_price
                            send_to_telegram(f"최적매도가격 : {predicted_sell_high_price}")
                        else:
                            short_quantity = calculate_quantity(symbol) * (leverage - 0.2)
                            limit_order = place_limit_order(symbol, 'sell', short_quantity, df['close'].iloc[-1])
                            send_to_telegram(f"매도 - Price: {sell_price}, Quantity: {short_quantity}")
                            send_to_telegram(f"손절가 - {short_stop_loss}")
                            sell_signal = True
                            upper_band, lower_band = calculate_bollinger_bands(df, window=20, num_std_dev=2.5)
                            future_close_price = lower_band.iloc[-1] # 과매도
                            now = datetime.datetime.now()
                            entry_time = datetime.datetime(now.year, now.month, now.day, now.hour, 0)

    # 매수 또는 매도 신호가 발생한 경우
    if buy_signal or sell_signal:
        # 주문 정보 가져오기
        order_info = exchange.fetch_order(limit_order['id'], symbol)
        order_status = None
        if order_info is not None:
            order_status = order_info['status']
        if order_status == 'open':
            if (datetime.datetime.now() >= entry_time + datetime.timedelta(hours=(6 - entry_time.hour % 6))):
                exchange.cancel_order(limit_order['id'], symbol)
                buy_signal = False
                sell_signal = False
                send_to_telegram(f'시간초과로 인한 포지션 취소')
        
        else:
            # 지정된 시간이 경과하면 주문을 종료하고 이익을 실현
            if buy_signal and (datetime.datetime.now() >= entry_time + datetime.timedelta(hours=(6 - entry_time.hour % 6))):
                place_limit_order(symbol, 'sell', long_quantity, df['close'].iloc[-1])
                profit = (df['close'].iloc[-1] - buy_price) / buy_price * 100 * leverage  # leverage 적용
                send_to_telegram(f"롱포지션 종료 \nQuantity: {long_quantity}\nprofit: {profit}")
                buy_signal = False

            elif sell_signal and (datetime.datetime.now() >= entry_time + datetime.timedelta(hours=(6 - entry_time.hour % 6))):
                place_limit_order(symbol, 'buy', short_quantity, df['close'].iloc[-1])
                profit = -(df['close'].iloc[-1] - sell_price) / sell_price * 100 * leverage  # leverage 적용
                send_to_telegram(f"숏포지션 종료 \nQuantity: {short_quantity}\nprofit: {profit}")
                sell_signal = False

            # 과매수시 익절
            if buy_signal == True:
                if future_close_price < df['close'].iloc[-1]:
                    place_limit_order(symbol, 'sell', long_quantity, df['close'].iloc[-1])
                    profit = (df['close'].iloc[-1] - buy_price) / buy_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"롱포지션 종료 \nQuantity: {long_quantity}\nprofit: {profit}")
                    buy_signal = False
                    waiting_buy_signal = False
                #손절
                elif long_stop_loss > df['close'].iloc[-1]:
                    place_market_order(symbol, 'sell', long_quantity)
                    profit = (df['close'].iloc[-1] - buy_price) / buy_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"롱포지션 손절 \nQuantity: {long_quantity}\nprofit: {profit}")
                    buy_signal = False
                    waiting_buy_signal = False

            # 과매도시 익절
            elif sell_signal == True:
                if future_close_price > df['close'].iloc[-1]:
                    place_limit_order(symbol, 'buy', short_quantity, df['close'].iloc[-1])
                    profit = -(df['close'].iloc[-1] - sell_price) / sell_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"숏포지션 종료 \nQuantity: {short_quantity}\nprofit: {profit}")
                    sell_signal = False
                    waiting_sell_signal = False
                #손절
                elif short_stop_loss < df['close'].iloc[-1]:
                    place_market_order(symbol, 'buy', short_quantity)
                    profit = -(df['close'].iloc[-1] - sell_price) / sell_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"숏포지션 손절 \nQuantity: {short_quantity}\nprofit: {profit}")
                    sell_signal = False
                    waiting_sell_signal = False

            # Profit_Percentage 손익시 포지션 종료
            if buy_signal == True:
                if df['close'].iloc[-1]> predicted_buy_low_price + predicted_buy_low_price/Profit_Percentage :
                    place_limit_order(symbol, 'sell', long_quantity, df['close'].iloc[-1])
                    profit = (df['close'].iloc[-1] - buy_price) / buy_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"롱포지션 종료 \nQuantity: {long_quantity}\nprofit: {profit}")
                    buy_signal = False
                    waiting_buy_signal = False
            elif sell_signal == True:
                if df['close'].iloc[-1]< predicted_sell_high_price - predicted_sell_high_price/Profit_Percentage :
                    place_limit_order(symbol, 'buy', short_quantity, df['close'].iloc[-1])
                    profit = -(df['close'].iloc[-1] - sell_price) / sell_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"숏포지션 종료 \nQuantity: {short_quantity}\nprofit: {profit}")
                    sell_signal = False
                    waiting_sell_signal = False

ema_buy_signal = False
ema_sell_signal = False
waiting_ema_buy_signal = False
waiting_ema_sell_signal = False
# EMA 기반 트레이딩 전략
def generate_ema_signals(symbol, df):
    global waiting_ema_buy_signal
    global waiting_ema_sell_signal
    global ema_buy_signal
    global ema_sell_signal
    global ema_predicted_buy_low_price
    global ema_predicted_sell_high_price
    global ema_entry_time
    global ema_long_stop_loss
    global ema_short_stop_loss
    global ema_future_close_price
    global ema_long_quantity
    global ema_short_quantity
    global ema_limit_order
    global ema_buy_price
    global ema_sell_price
    global ema_profit

    # ema 계산
    ema_9 = calculate_ema(df, 9)
    ema_21 = calculate_ema(df, 21)
    ema_54 = calculate_ema(df, 54)
    Buy_conditions = ema_9.iloc[-1] > ema_21.iloc[-1]
    Sell_conditions = ema_9.iloc[-1] < ema_21.iloc[-1]
    ema_Buy_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) > (ema_21.iloc[-1] - ema_54.iloc[-1])
    ema_Sell_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) < (ema_21.iloc[-1] - ema_54.iloc[-1])
    Previous_ema_Buy_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) > (ema_9.iloc[-2] - ema_21.iloc[-2])
    Previous_ema_Sell_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) < (ema_9.iloc[-2] - ema_21.iloc[-2])
    
    if ema_buy_signal == False and Buy_conditions and ema_Buy_conditions and Previous_ema_Buy_conditions:
        if waiting_ema_buy_signal == False:
            # 5분 뒤 가격 예측 및 텔레그램 전송
            predict_price(prediction_time='5m')
            send_to_telegram("ema 조건 충족")
            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
            ema_predicted_buy_low_price = predicted_low_price
            send_to_telegram(f"최적매수가격 : {ema_predicted_buy_low_price}")
            waiting_ema_buy_signal = True
        # 현재 가격이 예측한 최적 매수가격보다 낮으면 매수 주문 실행
        if df['close'].iloc[-1] < ema_predicted_buy_low_price:
            ema_long_stop_loss = (df['low'].iloc[-1] + df['open'].iloc[-2]) / 2
            ema_buy_price = df['close'].iloc[-1]
            if ema_long_stop_loss > ema_buy_price:
                waiting_ema_buy_signal = False
                send_to_telegram(f"손절가보다 매수가격이 더 작기에 최적매수가격을 재지정합니다.")
            else:
                ema_long_quantity = calculate_quantity(symbol) * (leverage - 0.2)
                ema_limit_order = place_limit_order(symbol, 'buy', ema_long_quantity, df['close'].iloc[-1])
                send_to_telegram(f"ema 조건 충족\n매수 - Price: {ema_buy_price}, Quantity: {ema_long_quantity}")
                send_to_telegram(f"손절가 - {ema_long_stop_loss}")
                ema_buy_signal = True
                upper_band, lower_band = calculate_bollinger_bands(df, window=20, num_std_dev=2.5)
                ema_future_close_price = upper_band.iloc[-1] # 과매수
                now = datetime.datetime.now()
                ema_entry_time = datetime.datetime(now.year, now.month, now.day, now.hour, 0)
    
    elif ema_sell_signal == False and Sell_conditions and ema_Sell_conditions and Previous_ema_Sell_conditions:
        if waiting_ema_sell_signal == False:
            # 5분 뒤 가격 예측 및 텔레그램 전송
            predict_price(prediction_time='5m')
            send_to_telegram("ema 조건 충족")
            send_to_telegram(f"현재가 : {df['close'].iloc[-1]}")
            ema_predicted_sell_high_price = predicted_high_price
            send_to_telegram(f"최적매도가격 : {ema_predicted_sell_high_price}")
            waiting_ema_sell_signal = True
        # 현재 가격이 예측한 최적 매도가격보다 높으면 매도 주문 실행
        if df['close'].iloc[-1] > ema_predicted_sell_high_price:
            ema_short_stop_loss = (df['high'].iloc[-1] + df['open'].iloc[-2]) / 2
            ema_sell_price = df['close'].iloc[-1]
            if ema_short_stop_loss < ema_sell_price:
                waiting_ema_sell_signal = False
                send_to_telegram(f"손절가보다 매도가격이 더 크기에 최적매도가격을 재지정합니다.")
            else:  
                ema_short_quantity = calculate_quantity(symbol) * (leverage - 0.2)
                ema_limit_order = place_limit_order(symbol, 'sell', ema_short_quantity, df['close'].iloc[-1])
                send_to_telegram(f"ema조건충족\n매도 - Price: {df['close'].iloc[-1]}, Quantity: {ema_short_quantity}")
                send_to_telegram(f"손절가 - {ema_short_stop_loss}")
                ema_sell_signal = True
                upper_band, lower_band = calculate_bollinger_bands(df, window=20, num_std_dev=2.5)
                ema_future_close_price = lower_band.iloc[-1] # 과매도
                now = datetime.datetime.now()
                ema_entry_time = datetime.datetime(now.year, now.month, now.day, now.hour, 0)
    
    # 매수 또는 매도 신호가 발생한 경우
    if ema_buy_signal or ema_sell_signal:
        # 주문 정보 가져오기
        order_info = exchange.fetch_order(ema_limit_order['id'], symbol)
        order_status = None
        if order_info is not None:
            order_status = order_info['status']
        
        if order_status == 'open':
            if datetime.datetime.now() >= ema_entry_time + datetime.timedelta(hours=(6 - ema_entry_time.hour % 6)):
                exchange.cancel_order(ema_limit_order['id'], symbol)
                ema_buy_signal = False
                ema_sell_signal = False
                send_to_telegram(f'시간초과로 인한 ema포지션 취소')
        
        else:
            # 지정된 시간이 경과하면 주문을 종료하고 이익을 실현
            if ema_buy_signal and datetime.datetime.now() >= ema_entry_time + datetime.timedelta(hours=(6 - ema_entry_time.hour % 6)):
                place_limit_order(symbol, 'sell', ema_long_quantity, df['close'].iloc[-1])
                ema_profit = (df['close'].iloc[-1] - ema_buy_price) / ema_buy_price * 100 * leverage  # leverage 적용
                send_to_telegram(f"ema롱포지션 종료 \nQuantity: {ema_long_quantity}\nprofit: {ema_profit}")
                ema_buy_signal = False

            elif ema_sell_signal and datetime.datetime.now() >= ema_entry_time + datetime.timedelta(hours=(6 - ema_entry_time.hour % 6)):
                place_limit_order(symbol, 'buy', ema_short_quantity, df['close'].iloc[-1])
                ema_profit = -(df['close'].iloc[-1] - ema_sell_price) / ema_sell_price * 100 * leverage  # leverage 적용
                send_to_telegram(f"ema숏포지션 종료 \nQuantity: {ema_short_quantity}\nprofit: {ema_profit}")
                ema_sell_signal = False

            # 과매수시 익절
            if ema_buy_signal == True:
                if ema_future_close_price < df['close'].iloc[-1]:
                    place_limit_order(symbol, 'sell', ema_long_quantity, df['close'].iloc[-1])
                    ema_profit = (df['close'].iloc[-1] - ema_buy_price) / ema_buy_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"ema롱포지션 종료 \nQuantity: {ema_long_quantity}\nprofit: {ema_profit}")
                    ema_buy_signal = False
                    waiting_ema_buy_signal = False
                # 손절
                elif ema_long_stop_loss > df['close'].iloc[-1]:
                    place_market_order(symbol, 'sell', ema_long_quantity)
                    ema_profit = (df['close'].iloc[-1] - ema_buy_price) / ema_buy_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"ema롱포지션 손절 \nQuantity: {ema_long_quantity}\nprofit: {ema_profit}")
                    ema_buy_signal = False
                    waiting_ema_buy_signal = False

            # 과매도시 익절
            elif ema_sell_signal == True:
                if ema_future_close_price > df['close'].iloc[-1]:
                    place_limit_order(symbol, 'buy', ema_short_quantity, df['close'].iloc[-1])
                    ema_profit = -(df['close'].iloc[-1] - ema_sell_price) / ema_sell_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"ema숏포지션 종료 \nQuantity: {ema_short_quantity}\nprofit: {ema_profit}")
                    ema_sell_signal = False
                    waiting_ema_sell_signal = False
                # 손절
                elif ema_short_stop_loss < df['close'].iloc[-1]:
                    place_market_order(symbol, 'buy', ema_short_quantity)
                    ema_profit = -(df['close'].iloc[-1] - ema_sell_price) / ema_sell_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"ema숏포지션 손절 \nQuantity: {ema_short_quantity}\nprofit: {ema_profit}")
                    ema_sell_signal = False
                    waiting_ema_sell_signal = False

            # Profit_Percentage 손익 시 포지션 종료
            if ema_buy_signal == True:
                if df['close'].iloc[-1] > ema_predicted_buy_low_price + ema_predicted_buy_low_price / Profit_Percentage :
                    place_limit_order(symbol, 'sell', ema_long_quantity, df['close'].iloc[-1])
                    ema_profit = (df['close'].iloc[-1] - ema_buy_price) / ema_buy_price * 100 * leverage  # leverage 적용
                    send_to_telegram(f"ema롱포지션 종료 \nQuantity: {ema_long_quantity}\nprofit: {ema_profit}")
                    ema_buy_signal = False
                    waiting_ema_buy_signal = False
            elif ema_sell_signal == True:
                if df['close'].iloc[-1] < ema_predicted_sell_high_price - ema_predicted_sell_high_price / Profit_Percentage :
                    place_limit_order(symbol, 'buy', ema_short_quantity, df['close'].iloc[-1])
                    ema_profit = -(df['close'].iloc[-1] - ema_sell_price) / ema_sell_price * 100 * leverage
                    send_to_telegram(f"ema숏포지션 종료 \nQuantity: {ema_short_quantity}\nprofit: {ema_profit}")
                    ema_sell_signal = False
                    waiting_ema_sell_signal = False

def filter_symbols(symbols):
    selected_symbols = []

    for i in symbols:
        df = get_candles(exchange, i, timeframe=timeframe, limit=100)
        ema_9 = calculate_ema(df, 9)
        ema_21 = calculate_ema(df, 21)
        ema_54 = calculate_ema(df, 54)

        Buy_conditions = ema_9.iloc[-1] > ema_21.iloc[-1]
        Sell_conditions = ema_9.iloc[-1] < ema_21.iloc[-1]
        rsi_Buy_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) > (ema_21.iloc[-1] - ema_54.iloc[-1])
        rsi_Sell_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) < (ema_21.iloc[-1] - ema_54.iloc[-1])
        Previous_rsi_Buy_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) > (ema_9.iloc[-2] - ema_21.iloc[-2])
        Previous_rsi_Sell_conditions = (ema_9.iloc[-1] - ema_21.iloc[-1]) < (ema_9.iloc[-2] - ema_21.iloc[-2])

        if (Buy_conditions and rsi_Buy_conditions and Previous_rsi_Buy_conditions) or \
           (Sell_conditions and rsi_Sell_conditions and Previous_rsi_Sell_conditions):
            selected_symbols.append(i)

    return selected_symbols


us_long = False
us_short = False
def Ultra_Scalping():
    global us_long, us_short, us_long_quantity, us_short_quantity, us_long_price, us_short_price, us_profit
    df = get_candles(exchange, symbol, timeframe=timeframe, limit=50)
    stoch_rsi_k, stoch_rsi_d = stochastic_rsi(df, period=14, smooth_k=3, smooth_d=3)
    us_profit = 1.003
    ema_21 = calculate_ema(df, 21)
    volume_oscillator = calculate_volume_oscillator(df['volume'].astype(float))

    # 최근 5개 값 추출
    recent_oscillator = volume_oscillator[-5:-1]

    # 30를 넘는지 확인
    if not (recent_oscillator > 30).any():
        if not us_long:
            if ema_21.iloc[-1] > df['close'].iloc[-1]:
                if stoch_rsi_k.iloc[-2] > 15 > stoch_rsi_d.iloc[-2]:
                    us_long = True
                    us_long_quantity = calculate_quantity(symbol) * 2
                    us_long_price = df['close'].iloc[-1]
                    place_limit_order(symbol, 'buy', us_long_quantity, df['close'].iloc[-1])
        elif not us_short:
            if ema_21.iloc[-1] < df['close'].iloc[-1]:
                if stoch_rsi_k.iloc[-2] < 86 < stoch_rsi_d.iloc[-2]:
                    us_short = True
                    us_short_quantity = calculate_quantity(symbol) * 2
                    us_short_price = df['close'].iloc[-1]
                    place_limit_order(symbol, 'sell', us_short_quantity, df['close'].iloc[-1])

    if us_long:
        if df['close'].iloc[-1] > ema_21.iloc[-1] :
            us_long = False
            place_limit_order(symbol, 'sell', us_long_quantity, df['close'].iloc[-1])
        elif us_long_price > (df['low'].iloc[-1] + df['open'].iloc[-2]) / 2:
            us_long = False
            place_market_order(symbol, 'sell', us_long_quantity)

    if us_short:
        if df['close'].iloc[-1] < ema_21.iloc[-1] :
            us_short = False
            place_limit_order(symbol, 'buy', us_short_quantity, df['close'].iloc[-1])
        elif us_short_price  < (df['high'].iloc[-1] + df['open'].iloc[-2]) / 2:
            us_short = False
            place_market_order(symbol, 'buy', us_short_quantity)




# 매매 주기 (예: 1초마다 전략 실행)
trade_interval = 1  # 초 단위
count=0
start = True
print('Autotrade_Start')

while True:
    try:
        if not stop:
            df = get_candles(exchange, symbol, timeframe=timeframe, limit=100)
            
            if execute_volatility_breakout_strategy:
                # 변동성 돌파 전략 코드 작성
                volatility_breakout_strategy(symbol, df, k_value)

            if execute_ema_trading_strategy:
                # EMA 기반 트레이딩 전략 코드 작성
                generate_ema_signals(symbol, df)

            if execute_scalping_strategy:
                # 초단타 전략 코드 작성
                Ultra_Scalping()
            schedule.run_pending()

            if start == True:
                send_to_telegram("***주의사항***\n\n현재는 이더리움(ETHUSDT)만 거래하도록 설정되어 있습니다.\n\n선물 시장에서 거래를 수행하며, 매수와 공매도 양 방향 포지션으로 전략이 구현되어 있습니다.\n\n레버리지는 이익을 극대화할 수 있지만, 동시에 손실도 배수로 커질 수 있습니다. 따라서 레버리지 사용 시 신중을 기해야 합니다.\n\n실전 거래에 앞서 충분한 백테스팅과 시뮬레이션을 진행하여 전략의 신뢰성을 검증하는 것이 좋습니다.\n")
                # 변동성 조건 임의 계산
                range = (df['high'].iloc[-2] - df['low'].iloc[-2]) * k_value
                target_long = df['close'].iloc[-2] + range
                target_short = df['close'].iloc[-2] - range
                # ema 계산
                ema_9 = calculate_ema(df, 9)
                ema_21 = calculate_ema(df, 21)
                ema_54 = calculate_ema(df, 54)
                upper_band, lower_band = calculate_bollinger_bands(df, window=20, num_std_dev=2.5)
                stoch_rsi_k, stoch_rsi_d = stochastic_rsi(df, period=14, smooth_k=3, smooth_d=3)
                rsi = calculate_rsi(df, period=14)
                send_to_telegram(f"UTC : {datetime.datetime.now()}")
                send_to_telegram(f"range : {range}\ntarget_long : {target_long}\ntarget_short : {target_short}\nema_9 : {ema_9.iloc[-1]}\nema_21 : {ema_21.iloc[-1]}\nema_54 : {ema_54.iloc[-1]}\nupper_band, lower_band : {upper_band.iloc[-1], lower_band.iloc[-1]}\nstoch_rsi_k, stoch_rsi_d : {stoch_rsi_k.iloc[-2], stoch_rsi_d.iloc[-2]}\nrsi : {rsi['rsi'].iloc[-1]}\n종가 : {df['close'].iloc[-1]}")
                send_to_telegram(f"{symbol} 매매 시작")
                start = False
            # 대기 시간
            time.sleep(trade_interval)
        elif stop:
            buy_signal = False
            waiting_buy_signal = False
            sell_signal = False
            waiting_sell_signal = False

            ema_buy_signal = False
            ema_sell_signal = False
            waiting_ema_buy_signal = False
            waiting_ema_sell_signal = False

            if postponement:
                postpone_trading()
            time.sleep(60)
    except Exception as e:
        send_to_telegram(f"An error occurred: {e}")
        count+=1
        if count==5:
            stop = True
            send_to_telegram("오류 발생으로 매매 중지")
            count=0
        pass
print("pkill -f binanceETCauto.py && nohup python3 binanceETCauto.py > output.log 2>&1 &")
