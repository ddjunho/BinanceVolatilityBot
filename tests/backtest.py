import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bayes_opt import BayesianOptimization
import ccxt

################ 백테스트 ################

# 백테스트 기본 설정
from binance_keys import api_key, api_secret

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
    limit=800  # 6h 데이터로 200일치
)

df = pd.DataFrame(data=candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# 변동성 돌파 전략 함수 설정
def VBS(df, config_data, long=True):
    k = config_data['k']

    # 목표가 계산
    df['range'] = df['high'] - df['low']  # 고점과 저점의 차이
    if long:
        df['target'] = df['open'] + df['range'].shift(1) * k  # 매수 목표가
    else:
        df['target'] = df['open'] - df['range'].shift(1) * k  # 공매도 목표가

    # 거래 시뮬레이션
    if long:
        df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)
    else:
        df['ror'] = np.where(df['low'] < df['target'], df['close'] / df['target'], 1)

    # 최종 수익률
    df['total'] = df['ror'].cumprod()
    final_cum_ror = df['total'].iloc[-1] - 1

    # 연간 수익률 (CAGR)
    N = ((df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]).days / 365.0)
    CAGR = (final_cum_ror + 1) ** (1 / N) - 1

    # Drawdown (DD) 계산
    array_v = np.array(df['total'])
    dd_list = -(np.maximum.accumulate(array_v) - array_v) / np.maximum.accumulate(array_v)
    mdd = dd_list.min()

    return final_cum_ror * 100, CAGR * 100, mdd * 100, df['total'], dd_list

################ 최적화 ################

### 매수 전략의 베이지안 최적화 함수
def optimize_buy_strategy(df):
    def black_box_function_buy(k):
        config_data = {'k': k}
        revenue = VBS(df, config_data, long=True)
        return revenue[0]  # 최종 누적 수익률 반환

    pbounds_buy = {'k': (0.20, 1.0)}  # 매개 변수 k의 범위

    optimizer_buy = BayesianOptimization(f=black_box_function_buy, pbounds=pbounds_buy, random_state=1)
    optimizer_buy.maximize(init_points=5, n_iter=100)  # 최적화 수행

    max_beyes_k_buy = optimizer_buy.max['params']['k']  # 최적의 k 값

    final_result_buy = VBS(df, {'k': max_beyes_k_buy}, long=True)  # 최적화된 전략으로 백테스트

    return final_result_buy, max_beyes_k_buy

### 공매도 전략의 베이지안 최적화 함수
def optimize_short_strategy(df):
    def black_box_function_short(k):
        config_data = {'k': k}
        revenue = VBS(df, config_data, long=False)
        return revenue[0]  # 최종 누적 수익률 반환

    pbounds_short = {'k': (0.20, 1.0)}  # 매개 변수 k의 범위

    optimizer_short = BayesianOptimization(f=black_box_function_short, pbounds=pbounds_short, random_state=1)
    optimizer_short.maximize(init_points=5, n_iter=100)  # 최적화 수행

    max_beyes_k_short = optimizer_short.max['params']['k']  # 최적의 k 값

    try:
        final_result_short = VBS(df, {'k': max_beyes_k_short}, long=False)  # 최적화된 전략으로 백테스트
    except Exception as e:
        print(f"Error occurred in short strategy optimization: {e}")
        final_result_short = (np.nan, np.nan, np.nan, None, None)

    return final_result_short, max_beyes_k_short

# 매수 전략 최적화 결과 계산
final_result_buy, max_beyes_k_buy = optimize_buy_strategy(df)

# 공매도 전략 최적화 결과 계산
final_result_short, max_beyes_k_short = optimize_short_strategy(df)

# 결과 출력
print("매수 전략 - 최종 누적 수익률: ", final_result_buy[0], "%, MDD: ", final_result_buy[2], "%, 최적의 K값: ", max_beyes_k_buy)
print("공매도 전략 - 최종 누적 수익률: ", final_result_short[0], "%, MDD: ", final_result_short[2], "%, 최적의 K값: ", max_beyes_k_short)

################ 시각화 및 저장 ################

# 매수 전략 그래프 저장
# 첫번째 그림: 누적 수익 및 가격 그래프
fig, ax1 = plt.subplots(figsize=(15, 8))
ax1.plot(df['timestamp'], final_result_buy[-2], color='red', label='Cumulative Profit')  # 누적 수익 그래프
ax1.set_xlabel('Time')
ax1.set_ylabel('Cumulative Profit', color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['close'], color='blue', label='Price')  # 가격 그래프
ax2.set_ylabel('Price', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.title('Buy Strategy - Cumulative Profit and Price')

# 그래프 저장
plt.savefig('buy_strategy_cumulative_profit_price.png')
plt.close()

# 두번째 그림: Drawdown 그래프
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(df['timestamp'], final_result_buy[-1])  # DD 그래프
ax.set_xlabel('Time')
ax.set_ylabel('Drawdown (DD)')
ax.grid(True)
plt.title('Buy Strategy - Drawdown (DD)')

# 그래프 저장
plt.savefig('buy_strategy_drawdown.png')
plt.close()

# 공매도 전략 그래프 저장
# 첫번째 그림: 누적 수익 및 가격 그래프
fig, ax1 = plt.subplots(figsize=(15, 8))
ax1.plot(df['timestamp'], final_result_short[-2], color='red', label='Cumulative Profit')  # 누적 수익 그래프
ax1.set_xlabel('Time')
ax1.set_ylabel('Cumulative Profit', color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['close'], color='blue', label='Price')  # 가격 그래프
ax2.set_ylabel('Price', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.title('Short Strategy - Cumulative Profit and Price')

# 그래프 저장
plt.savefig('short_strategy_cumulative_profit_price.png')
plt.close()

# 두번째 그림: Drawdown 그래프
fig, ax = plt.subplots(figsize=(15, 8))
ax.plot(df['timestamp'], final_result_short[-1])  # DD 그래프
ax.set_xlabel('Time')
ax.set_ylabel('Drawdown (DD)')
ax.grid(True)
plt.title('Short Strategy - Drawdown (DD)')

# 그래프 저장
plt.savefig('short_strategy_drawdown.png')
plt.close()
