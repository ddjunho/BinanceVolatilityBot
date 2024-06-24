import pandas as pd
import numpy as np
from bayes_opt import BayesianOptimization
import ccxt

################ 백테스트 ################

# 백테스트 기본 셋팅
from BinanceVolatilityBot.binance_keys import api_key, api_secret

exchange = ccxt.binance({
    'rateLimit': 1000,
    'enableRateLimit': True,
    'apiKey': api_key,
    'secret': api_secret,
    'options': {
        'defaultType': 'future'
    }
})
symbol = 'ETHUSDT'
timeframe = '6h'  # 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# 데이터 읽어오기: 전체 데이터
candles = exchange.fetch_ohlcv(
    symbol=symbol,
    timeframe=timeframe,
    since=None,
    limit=800 #6h이므로 200일
)

df = pd.DataFrame(data=candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# 변동성 돌파 전략 함수 설정

def VBS(df, config_data, long=True):
    k = config_data['k']

    # 목표가 구하기
    df['range'] = df['high'] - df['low']  # 고저 변동폭
    if long:
        df['target'] = df['open'] + df['range'].shift(1) * k  # 매수 목표가 계산
    else:
        df['target'] = df['open'] - df['range'].shift(1) * k  # 공매도 목표가 계산

    # 매매 시뮬레이션
    if long:
        df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)
    else:
        df['ror'] = np.where(df['low'] < df['target'], df['close'] / df['target'], 1)

    # 최종 누적 산출
    df['total'] = df['ror'].cumprod()
    final_cum_ror = (df['total'].iloc[-1].astype(float)) * 100 - 100

    # 연간 수익률 (기간 수익률)
    N = ((df.index[-1] - df.index[0])) / 365
    CAGR = (final_cum_ror ** (1 / N))

    # dd값 기록 및 mdd 계산
    array_v = np.array(df['total'])
    dd_list = -(np.maximum.accumulate(array_v) - array_v) / np.maximum.accumulate(array_v)
    peak_lower = np.argmax(np.maximum.accumulate(array_v) - array_v)
    peak_upper = np.argmax(array_v[:peak_lower])
    mdd = round((array_v[peak_lower] - array_v[peak_upper]) / array_v[peak_upper] * 100, 3)

    return final_cum_ror, CAGR, mdd

################ 최적화 ################

### 매수 전략의 베이지안 최적화 함수

def optimize_buy_strategy(df):
    # 매수 전략을 위한 함수
    def black_box_function_buy(k):
        config_data = {'k': k}
        revenue = VBS(df, config_data, long=True)
        return revenue[0]  # 최종 누적 수익률 리턴

    # parameter k의 범위
    pbounds_buy = {'k': (0.20, 1.0)}

    # 베이지안 최적화 시행베이지안 최적화의 반복 횟수
    optimizer_buy = BayesianOptimization(f=black_box_function_buy, pbounds=pbounds_buy, random_state=1)
    optimizer_buy.maximize(init_points=5, n_iter=100) # 반복 횟수

    # 최적의 k값 도출
    max_beyes_k_buy = optimizer_buy.max['params']['k']

    # 최적화된 전략으로 다시 시뮬레이션
    final_result_buy = VBS(df, {'k': max_beyes_k_buy}, long=True)

    return final_result_buy, max_beyes_k_buy

### 공매도 전략의 베이지안 최적화 함수

def optimize_short_strategy(df):
    # 공매도 전략을 위한 함수
    def black_box_function_short(k):
        config_data = {'k': k}
        revenue = VBS(df, config_data, long=False)
        return revenue[0]  # 최종 누적 수익률 리턴

    # parameter k의 범위
    pbounds_short = {'k': (0.20, 1.0)}

    # 베이지안 최적화 시행
    optimizer_short = BayesianOptimization(f=black_box_function_short, pbounds=pbounds_short, random_state=1)
    optimizer_short.maximize(init_points=5, n_iter=100)

    # 최적의 k값 도출
    max_beyes_k_short = optimizer_short.max['params']['k']

    # 최적화된 전략으로 다시 시뮬레이션
    try:
        final_result_short = VBS(df, {'k': max_beyes_k_short}, long=False)
    except Exception as e:
        print(f"Error occurred in short strategy optimization: {e}")
        final_result_short = (np.nan, np.nan, np.nan)

    return final_result_short, max_beyes_k_short

# 매수 전략 최적화 결과 계산
final_result_buy, max_beyes_k_buy = optimize_buy_strategy(df)

# 공매도 전략 최적화 결과 계산
final_result_short, max_beyes_k_short = optimize_short_strategy(df)

# 결과 출력
print("매수 전략 - 최종 누적 수익률: ", final_result_buy[0], "%, MDD: ", final_result_buy[2], "%, 최적의 K값: ", max_beyes_k_buy)
print("공매도 전략 - 최종 누적 수익률: ", final_result_short[0], "%, MDD: ", final_result_short[2], "%, 최적의 K값: ", max_beyes_k_short)
