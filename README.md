## 설치

### 패키지 설치

이 프로젝트를 실행하기 위해서는 먼저 패키지를 설치해야 합니다. 아래 명령어를 사용하여 설치할 수 있습니다.

<details>
<summary>pip install .</summary>

```bash
pip install .
</details>
또는 개발 환경에서 패키지를 설치할 경우:

<details>
<summary>pip install -e .</summary>
bash
코드 복사
pip install -e .
</details>
Binance API 키 설정
binance_keys.py 파일을 작성하여 Binance API 키와 시크릿 키를 설정해야 합니다.

<details>
<summary>binance_keys.py</summary>
python
코드 복사
# binance_keys.py

api_key = 'your_binance_api_key'
api_secret = 'your_binance_api_secret'
</details>
Telegram 설정
telepot_bot_id.py 파일을 작성하여 Telegram 봇의 API 토큰과 채팅 ID를 설정합니다.

<details>
<summary>telepot_bot_id.py</summary>
python
코드 복사
# telepot_bot_id.py

token = 'your_telegram_bot_token'
chat_id = 'your_telegram_chat_id'
</details>
실행
프로젝트를 실행하여 BinanceVolatilityBot을 사용할 수 있습니다. 아래의 명령어를 사용합니다.

<details>
<summary>BinanceVolatilityBot 실행</summary>
bash
코드 복사
python BinanceVolatilityBot/BinanceVolatilityBot.py
</details>
테스트
간단한 테스트를 수행하려면 tests/test_binance_volatility_bot.py 파일을 실행합니다.

<details>
<summary>테스트 실행</summary>
bash
코드 복사
pytest tests/test_binance_volatility_bot.py
</details>
주의사항
보안: API 키와 시크릿 키, Telegram 봇의 토큰과 채팅 ID는 외부에 노출되지 않도록 주의해야 합니다.
실전 사용: 실전 거래에 앞서 충분한 백테스팅과 시뮬레이션을 진행하여 전략의 신뢰성을 검증하는 것이 좋습니다.
