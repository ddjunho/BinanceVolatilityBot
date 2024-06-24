# BinanceVolatilityBot
BinanceVolatilityBot은 파이썬으로 작성된 자동매매 봇입니다. 이 봇은 Binance 거래소에서 거래를 수행하며, 변동성 돌파 전략과 EMA(지수 이동 평균) 기반 트레이딩 전략을 활용합니다.

파일 구성
프로젝트는 다음과 같은 파일들로 구성되어 있습니다:

BinanceVolatilityBot.py: 메인 실행 파일로, 자동매매 봇의 주요 기능이 구현되어 있습니다.
binance_keys.py: Binance API 키를 설정하는 파일입니다. 반드시 설정되어 있어야 합니다.
telepot_bot_id.py: Telegram 봇의 API 키를 설정하는 파일입니다. Telegram 알림 기능을 위해 필요합니다.
tests/test_binance_volatility_bot.py: BinanceVolatilityBot.py 파일의 간단한 단위 테스트를 수행하는 파일입니다.
실행 방법
환경 설정: binance_keys.py 파일에 Binance API 키를 입력하세요. telepot_bot_id.py 파일에는 Telegram 봇의 API 키를 입력하세요.

의존성 설치: 필요한 패키지들을 설치합니다. 주로 requests, pandas, numpy, python-binance 등의 패키지가 필요할 수 있습니다.

'''bash
봇 실행: 다음 명령으로 BinanceVolatilityBot.py 파일을 실행합니다.
pip install requests pandas numpy python-binance
'''
bash
코드 복사
python BinanceVolatilityBot/BinanceVolatilityBot.py
전략
봇은 다음 두 가지 전략을 사용하여 자동 거래를 수행합니다:

변동성 돌파 전략: 가격의 변동성을 기반으로 일정 범위를 돌파할 때 매수 또는 매도를 결정합니다.
EMA 기반 트레이딩 전략: 지수 이동 평균을 활용하여 단기 및 장기 추세를 분석하고, 이를 바탕으로 매매 결정을 내립니다.
테스트
프로젝트는 단위 테스트 파일 tests/test_binance_volatility_bot.py를 포함하고 있습니다. 이 파일을 사용하여 주요 함수와 클래스를 테스트할 수 있습니다. 테스트는 다음과 같이 실행합니다:

bash
코드 복사
python tests/test_binance_volatility_bot.py
주의 사항
API 보안: Binance API 키와 Telegram 봇의 API 키는 보안에 유의하여 관리해야 합니다.
자동 거래 위험: 자동 거래 시스템은 많은 위험을 수반할 수 있으므로, 코드를 이해하고 테스트를 충분히 거친 후 사용하는 것이 좋습니다.
이 README 파일은 프로젝트의 설치 및 사용 방법에 대한 간략한 소개를 제공합니다. 추가적인 설정이나 세부 사항은 코드의 주석 및 문서화된 부분을 참조하세요.
