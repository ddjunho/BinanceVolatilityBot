# BinanceVolatilityBot

BinanceVolatilityBot은 CCXT – 암호화폐 교환 거래 라이브러리를 이용하여 자동매매 봇을 구현한 프로젝트입니다. 이 봇은 변동성 돌파 전략과 EMA 기반 트레이딩 전략을 적용하여 자동으로 거래를 수행합니다.

## [CCXT – CryptoCurrency eXchange Trading Library](https://github.com/ccxt/ccxt/tree/master)

### [Manual](https://github.com/ccxt/ccxt/wiki) · [FAQ](https://github.com/ccxt/ccxt/wiki/FAQ) · [Examples](https://github.com/ccxt/ccxt/tree/master/examples) · [Contributing](https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md)

 [![binancecoinm](https://user-images.githubusercontent.com/1294454/117738721-668c8d80-b205-11eb-8c49-3fad84c4a07f.jpg)](https://accounts.binance.com/en/register?ref=D7YA7CLY)                                 binancecoinm           [Binance COIN-M](https://accounts.binance.com/en/register?ref=D7YA7CLY)                                [![API Version *](https://img.shields.io/badge/*-lightgray)](https://binance-docs.github.io/apidocs/delivery/en/)              cex   [![CCXT Certified](https://img.shields.io/badge/CCXT-Certified-green.svg)](https://github.com/ccxt/ccxt/wiki/Certification)  [![CCXT Pro](https://img.shields.io/badge/CCXT-Pro-black)](https://ccxt.pro)  [![Sign up with Binance COIN-M using CCXT's referral link for a 10% discount!](https://img.shields.io/static/v1?label=Fee&message=%2d10%25&color=orange)](https://accounts.binance.com/en/register?ref=D7YA7CLY)   
 
[ccxt library](https://docs.ccxt.com)

#### ***Thank you CCXT!***

## 설정

### 패키지 설치

이 프로젝트를 실행하기 위해서는 먼저 패키지를 설치해야 합니다. 아래 명령어를 사용하여 설치할 수 있습니다.

```bash
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

### Telegram 설정

telepot_bot_id.py 파일을 작성하여 Telegram 봇의 API 토큰과 채팅 ID를 설정합니다.

```python
# telepot_bot_id.py

token = 'your_telegram_bot_token'
chat_id = 'your_telegram_chat_id'
```

## 실행

프로젝트를 실행하여 BinanceVolatilityBot을 사용할 수 있습니다. 아래의 명령어를 사용합니다.

```bash
nohup python3 BinanceVolatilityBot.py > output.log &
```

### 테스트

간단한 테스트를 수행하려면 tests/test_binance_volatility_bot.py 파일을 실행합니다.

```bash
pytest tests/test_binance_volatility_bot.py
```

테스트는 정상적으로 작동하는지 확인하고, 필요한 경우 추가적인 유닛 테스트를 작성하여 기능을 검증할 수 있습니다.

## ***주의사항***

#### 보안 : API 키와 시크릿 키, Telegram 봇의 토큰과 채팅 ID는 외부에 노출되지 않도록 주의해야 합니다.

#### 실전 사용 : 실전 거래에 앞서 충분한 백테스팅과 시뮬레이션을 진행하여 전략의 신뢰성을 검증하는 것이 좋습니다.
