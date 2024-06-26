# BinanceVolatilityBot

BinanceVolatilityBot은 CCXT를 이용하여 자동매매 봇을 구현한 프로젝트입니다. 이 봇은 변동성 돌파 전략과 EMA 기반 추세 추종 전략을 적용하여 자동으로 선물거래를 수행합니다.

## [CCXT – CryptoCurrency eXchange Trading Library](https://github.com/ccxt/ccxt/tree/master)

### [Manual](https://github.com/ccxt/ccxt/wiki) · [FAQ](https://github.com/ccxt/ccxt/wiki/FAQ) · [Examples](https://github.com/ccxt/ccxt/tree/master/examples) · [Contributing](https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md)

 [![binancecoinm](https://user-images.githubusercontent.com/1294454/117738721-668c8d80-b205-11eb-8c49-3fad84c4a07f.jpg)](https://accounts.binance.com/en/register?ref=D7YA7CLY)                                            [![CCXT Certified](https://img.shields.io/badge/CCXT-Certified-green.svg)](https://github.com/ccxt/ccxt/wiki/Certification)  [![CCXT Pro](https://img.shields.io/badge/CCXT-Pro-black)](https://ccxt.pro)  [![Sign up with Binance COIN-M using CCXT's referral link for a 10% discount!](https://img.shields.io/static/v1?label=Fee&message=%2d10%25&color=orange)](https://accounts.binance.com/en/register?ref=D7YA7CLY)   
 
#### ***Thank you CCXT!***

## 전략 소개

### 변동성 돌파 전략

변동성 돌파 전략 예시
![변동성 돌파 전략 예시 사진](https://github.com/ddjunho/binanceauto/blob/main/img/volatility_explained.png)(https://www.tradingview.com/chart/TSLA/vlvAMwqN-Volatility-Breakout-Trading-Explained/)


#### 변동성 돌파 전략 원리

돌파 가격 = 현재 시가 + (이전 고가 - 이전 저가) * k값 

오늘 가격이 돌파 가격을 넘어가면 매수하고 다음날 아침 장이 시작하면 모두 매도한다.

이전 시가 : $920, 이전 고가 : $1000, 이전 저가 : $900, 이전 종가 $960

현재 시가 : $960

돌파 가격 = $960 + ($1000 - $900) * 0.6 = $1020

현재 장중에 돌파 가격 $1020을 넘어서면 매수해서 다음 시작시 모두 매도
#### 오늘 매수해서 내일 팔기 때문에 시장 심리에 휘둘리지 않습니다.
이러한 매매 전략을 백테스팅으로 구현한 결과입니다. 백테스팅 코드는 [backtest.py](https://github.com/ddjunho/BinanceVolatilityBot/blob/main/tests/backtest.py)에서 확인할 수 있습니다.
![돌파전략 매수시 순이익](https://github.com/ddjunho/binanceauto/blob/main/img/buy_strategy_cumulative_profit_price.png)
빨간색이 순 이익입니다. 수수료를 제외하고 매수 포지션만 잡을 시 200일간의 누적 수익을 지표로 나타내었습니다.
![매수포지션 MDD](https://github.com/ddjunho/binanceauto/blob/main/img/buy_strategy_drawdown.png)
MDD(Most Drawdown, 최대 손실 낙폭)는 누적 이익률의 최대값(Peak)에서 가장 크게 하락한 비율을 백분율로 나타냅니다.

timeframe = '6h'

매수 전략 - 최종 누적 수익률: 55.5006352412013%, MDD: -9.999630944195218%, 최적의 K값: 0.513664700396083

실제로 이렇게 수익을 얻을 수 있으면 좋겠지만 현실은 그렇지 않습니다. 큰 세력이 매물대를 뚫고 한 번에 고가 갱신을 해버리기 때문에 적절한 매수 가격대를 구하지 못하고 높은 가격에 사고 낮은 가격에 파는 대참사가 있을 수 있습니다.

그리하여 [***Auto ARIMA***](https://github.com/ddjunho/BinanceVolatilityBot/tree/main?tab=readme-ov-file#%EC%98%88%EC%B8%A1-%EA%B8%B0%EB%8A%A5) 모델을 사용해서 15분 뒤의 최저 가격을 예측하고 해당 가격보다 낮을 때 매수를 진행할 수 있도록 하였습니다.<br><br><br>

### EMA 기반 추세 추종 전략
이 전략은 이동 평균을 기반으로 한 자동매매 전략입니다. 여기서는 9일, 21일, 54일 이동 평균을 사용하여 주가의 추세와 모멘텀을 평가하고, 매수 조건을 설정합니다. 이 매수 전략은 자동매매 시스템에 적용될 수 있습니다.
![ema전략](https://github.com/ddjunho/binanceauto/blob/main/img/ema.png)

#### 매수 조건
이 전략에서는 다음과 같은 세 가지 매수 조건을 사용합니다:

기본 매수 조건 (Buy_conditions):<br>
9일 이동 평균 (ema_9)이 21일 이동 평균 (ema_21)보다 클 때.<br>
조건: ema_9 > ema_21<br>
설명: 이 조건은 단기 추세가 중기 추세보다 강하다는 신호로 해석됩니다. 자동매매 시스템은 이 신호가 발생할 때 해당 종목을 매수할 수 있습니다.<br>

강한 매수 조건 (ema_Buy_conditions):<br>
9일 이동 평균과 21일 이동 평균의 차이 (ema_9 - ema_21)가 21일 이동 평균과 54일 이동 평균의 차이 (ema_21 - ema_54)보다 클 때.<br>
조건: (ema_9 - ema_21) > (ema_21 - ema_54)<br>
설명: 이 조건은 단기 상승 모멘텀이 중기 상승 모멘텀보다 강하다는 것을 의미합니다. 자동매매 시스템은 이 상황을 강력한 매수 신호로 간주하여 해당 종목을 더 확신 있게 매수할 수 있습니다.<br>

이전의 매수 조건 변화 (Previous_ema_Buy_conditions):<br>
현재 9일 이동 평균과 21일 이동 평균의 차이 (ema_9 - ema_21)가 이전 값보다 클 때.<br>
조건: (ema_9 - ema_21)가 전일의 (ema_9 - ema_21)보다 클 때.<br>
설명: 이 조건은 단기 이동 평균이 중기 이동 평균에 비해 더 빠르게 상승하고 있음을 나타냅니다. 자동매매 시스템은 이 경향을 감지하여 단기적인 매수 모멘텀을 포착할 수 있습니다.<br>

여기서도 [***Auto ARIMA***](https://github.com/ddjunho/BinanceVolatilityBot/tree/main?tab=readme-ov-file#%EC%98%88%EC%B8%A1-%EA%B8%B0%EB%8A%A5) 모델을 사용해서 5분 뒤의 최저 가격을 예측하고 해당 가격보다 낮을 때 매수를 진행할 수 있도록 하였습니다.<br><br><br>
### 예측 기능
ARIMA(Autoregressive Integrated Moving Average)는 시계열 데이터를 예측하기 위해 사용되는 모델로, 세 가지 주요 요소로 구성됩니다:<br>

자기회귀(AR, Autoregressive): 과거 값들이 현재 값에 영향을 미치는 모델입니다.<br>
누적차분(I, Integrated): 데이터를 정상 상태로 변환하기 위해 필요한 차분 과정입니다.<br>
이동평균(MA, Moving Average): 백색 잡음에 의해 설명되는 현재 값의 모델입니다.<br>
이 세 가지 요소를 결합하여 ARIMA 모델은 시계열 데이터의 패턴을 설명하고 예측하는 데 사용됩니다.<br>

predict_price는 이 ARIMA 모델을 사용하여 금융 자산(예: 주식 또는 암호화폐)의 미래 가격을 예측하는 기능입니다. 이 함수는 특정 미래 시간 간격에 대한 종가를 예측하고 고가와 저가를 추정합니다. 함수의 구성 요소와 프로세스를 자세히 설명하겠습니다.

#### 함수 매개변수
prediction_time: 예측 시간 간격을 지정하는 문자열 (예: '1h'는 1시간, '3m'는 3분 등).<br>
add_mintes: 예측 간격에 추가할 추가 분 수를 나타내는 정수 (기본값은 0).

#### 데이터 가져오기:

함수는 get_candles(exchange, symbol, timeframe=prediction_time, limit=200)을 호출하여 과거 가격 데이터를 가져옵니다.
이 데이터는 timestamp, open, high, low, close, volume 열을 포함합니다.
열 이름 변경 및 인덱싱:<br>
df = df.rename(columns={'timestamp': 'ds', 'open': 'open', 'high': 'high', 'low': 'low', 'close': 'y', 'volume': 'volume'})<br>
df.set_index('ds', inplace=True)

#### ARIMA 모델 학습
모델 초기화 및 학습:<br>
auto_arima를 사용하여 ARIMA 모델을 초기화하고 학습합니다.<br>
model = auto_arima(df['y'], seasonal=False, suppress_warnings=True)<br>
#### 예측 시간 계산
prediction_time에 따라 추가할 분(minute)을 계산합니다.
```python
if prediction_time == '6h':
    minutes_to_add = 60*6 + add_mintes
elif prediction_time == '3m':
    minutes_to_add = 3 + add_mintes
elif prediction_time == '5m':
    minutes_to_add = 5 + add_mintes  
elif prediction_time == '10m':
    add_mintes = 5
    minutes_to_add = 5 + add_mintes  
elif prediction_time == '15m':
    minutes_to_add = 15 + add_mintes
elif prediction_time == '1h':
    minutes_to_add = 60 + add_mintes
elif prediction_time == '1d':
    minutes_to_add = 24 * 60 + add_mintes
```
#### 미래 데이터 포인트 생성
미래 시점에 대한 데이터를 생성합니다.
```python
future = pd.DataFrame(index=[df.index[-1] + pd.Timedelta(minutes=minutes_to_add)])
future['open'] = df['open'].iloc[-1]
future['high'] = df['high'].iloc[-1]
future['low'] = df['low'].iloc[-1]
future['volume'] = df['volume'].iloc[-1]
```
#### 예측 수행
모델을 사용하여 예측을 수행합니다.
forecast, conf_int = model.predict(n_periods=1, exogenous=[future.values], return_conf_int=True)

#### 예측 결과 저장
예측된 종가를 저장하고 고가와 저가를 예측 구간(confidence interval)으로부터 계산합니다.
```python
close_value = forecast[0]
predicted_close_price = close_value
predicted_high_price = conf_int[0][1]
predicted_low_price = conf_int[0][0]
```
#### 결론
이 함수는 주어진 시간 간격 후의 종가를 예측하고, 신뢰 구간을 사용하여 고가와 저가를 추정하는 과정을 자동화합니다.<br><br>


## 자동매매 시작하기

### 패키지 설치

이 프로젝트를 실행하기 위해서는 먼저 패키지를 설치해야 합니다. 아래 명령어를 사용하여 설치할 수 있습니다.

```bash
git clone https://github.com/ddjunho/BinanceVolatilityBot.git
cd BinanceVolatilityBot
pip install .
```

또는 개발 환경에서 패키지를 설치할 경우:

```bash
pip install -e .
```

### Binance API 키 설정

binance_keys.py 파일을 작성하여 Binance API 키와 시크릿 키를 설정해야 합니다.

```python
# binance_keys.py

api_key = 'your_binance_api_key'
api_secret = 'your_binance_api_secret'
```
```bash
echo -e "api_key = 'your_binance_api_key'\napi_secret = 'your_binance_api_secret'" > BinanceVolatilityBot/binance_keys.py
```
### Telegram 설정
[BotFather](https://telegram.me/BotFather)를 통해 봇을 생성 후
telepot_bot_id.py 파일을 작성하여 Telegram 봇의 API 토큰과 채팅 ID를 설정합니다.

```python
# telepot_bot_id.py

token = 'your_telegram_bot_token'
chat_id = 'your_telegram_chat_id'
```
```bash
echo -e "token = 'your_telegram_bot_token'\nchat_id = 'your_telegram_chat_id'" > BinanceVolatilityBot/telepot_bot_id.py
```
### Telegram 사용법
이 Telegram 봇은 암호화폐 자동매매 시스템을 위해 설계되었습니다. 사용자가 Telegram을 통해 명령어를 입력하면, 해당 봇은 사용자가 설정한 조건에 따라 자동으로 암호화폐를 매매하는 기능을 제공합니다. 각 명령어를 정확히 입력하여 원하는 설정을 변경하거나 정보를 얻을 수 있습니다.

#### 기능 목록
```
시작 및 중지
/start: 자동매매를 시작합니다.
/stop: 자동매매를 중지후 초기화합니다.

도움말
/help: 사용 가능한 모든 명령어와 각 명령어의 설명을 제공합니다.

레버리지 설정
/leverage(num): 레버리지 값을 설정합니다. (num은 1에서 10 사이의 값)
예시: /leverage(5)

K 값 설정
/set(k): K 값을 설정합니다. (k는 0.2에서 0.75까지 0.05 단위로 설정 가능)
예시: /set(0.5)

익절 수치 설정
/Profit_Percentage(num): 익절 수치를 설정합니다. (num은 100에서 200 사이의 값)
예시: /Profit_Percentage(120)

가격 예측
/predict_3m, /predict_5m, /predict_15m, /predict_1h, /predict_6h, /predict_1d: 각각 3분, 5분, 15분, 1시간, 6시간, 1일 뒤의 가격을 예측합니다.

조건 충족 코인 목록
/Condition_fulfillment_symbols: ema 조건을 충족하는 암호화폐 심볼 목록을 제공합니다.
```
## 실행

백그라운드로 BinanceVolatilityBot을 사용할 수 있습니다. 아래의 명령어를 사용합니다.

```bash
nohup python3 BinanceVolatilityBot.py > output.log &
```

### 테스트

돌파의 기준인 k값을 구하려면 backtest.py 을 실행합니다.
매수와 매도의 최종 누적 수익률을 구하고 최적의 k값을 찾을 수 있습니다. 현재값 : 0.55

```bash
python3 tests/backtest.py
```

간단한 점검를 수행하려면 test_binance_volatility_bot.py 파일을 실행합니다.

```bash
pytest tests/test_binance_volatility_bot.py
```

테스트는 정상적으로 작동하는지 확인하고, 필요한 경우 추가적인 유닛 테스트를 작성하여 기능을 검증할 수 있습니다.


## ***주의사항***

#### 현재는 이더리움(ETHUSDT)만 거래하도록 설정되어 있습니다.

#### 선물 시장에서 거래를 수행하며, 매수와 공매도 양 방향 포지션으로 전략이 구현되어있습니다.

#### 레버리지는 이익을 극대화할 수 있지만, 동시에 손실도 배수로 커질 수 있습니다. 따라서 레버리지 사용 시 신중을 기해야 합니다.

#### 수수료는 고려하지 않았습니다.

#### API 키와 시크릿 키, Telegram 봇의 토큰과 채팅 ID는 외부에 노출되지 않도록 주의해야 합니다.

#### 실전 거래에 앞서 충분한 백테스팅과 시뮬레이션을 진행하여 전략의 신뢰성을 검증하는 것이 좋습니다.
