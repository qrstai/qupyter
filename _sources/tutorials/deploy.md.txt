# 전략 배포 하기

Qupyter platform 에 작성한 전략을 배포하는 방법을 살펴보겠습니다.

## 전략 코드 준비

사용자가 직접 작성한 전략 코드를 준비합니다. 다음은 예제 전략코드입니다.

### 5min_breakout_strategy.py

```python
from typing import List
import datetime
import time


async def trade_func(account_info, pending_orders, positions, broker):
    """
    전략에 의한 매매 지시 목록을 생성합니다

    전략: 최근 5분봉의 저가를 하향 돌파시 매수, 고가를 상향 돌파시 매도
    """

    # 현재 시간을 데이터 조회 기준 분봉으로 변환
    current_time = datetime.datetime.now().replace(second=0, microsecond=0)

    asset_code = 'A005930'  # 거래 종목 코드 (삼성전자)
    orders = []  # 매매 지시 내역

    # 증권사 함수를 활용하여 현재가 조회
    current_data_df = broker.get_price(asset_code=asset_code)
    current_price = current_data_df.iloc[0]['current_price']

    # 증권사 함수를 활용하여 1분봉 데이터 조회
    minute_data_df = broker.get_historical_minute_data(asset_code=asset_code, interval=1)

    # 최근 5분봉의 고가와 저가 획득
    range_df = minute_data_df[minute_data_df.index < current_time].tail(5)
    range_high = range_df['high'].max()
    range_low = range_df['low'].min()

    # 현재가가 최근 5분봉의 고가를 상향 돌파한 경우, 1주 매도
    if current_price > range_high:
        # 포지션 보유 여부 확인
        position_size = 0
        for p in positions:
            if p.asset_code == asset_code:
                position_size = p.quantity
                break

        # 포지션이 있는 경우, 1주 매도를 매매 지시 수량(음수)으로 지정
        if position_size > 0:
            sell_size = -1
            orders.append((asset_code, current_price, sell_size))

    # 현재가가 최근 5분봉의 저가를 하향 돌파한 경우, 1주 매수
    elif current_price < range_low:
        # 현금 주문 가능 금액 조회
        investable_cash = account_info['investable_cash']

        # 매매 수수료(0.015%)를 포함한 1주 매수시 소요되는 금액 확인
        buy_size = 1
        buy_amount = int(current_price * buy_size * (1 + 0.00015))

        # 매수 가능한 현금이 있는 경우, 1주 매수를 매매 지시 수량(양수)으로 지정
        if investable_cash > buy_amount:
            orders.append((asset_code, current_price, buy_size))

    return orders
```

전략코드 실행에 필요한 package가 있다면 requirements.txt에 나열합니다

### requirements.txt

```text
finance-datareader==0.9.50
```

## 배포

배포는 `qup deploy` 명령을 사용해서 진행합니다.

```bash
jovyan@jupyter-qupyter:~/strategy2$ qup deploy --help
Usage: qup deploy [OPTIONS] ENTRY_FILENAME

  Deploy strategy

  ENTRY_FILENAME: Path to the strategy entry file

Options:
  -n, --name TEXT  Specify the name of the strategy. If not provided, the
                   filename will be used as the name.
  --help           Show this message and exit.
```

작성한 전략 파일을 인자로 전달합니다. `-n` 옵션을 사용해 전략의 이름을 따로 지정할 수 있습니다.
지정하지 않는 경우 파일이름을 전략 이름으로 사용합니다.

아래와 같이 실행하여 배포를 진행합니다.

```bash
jovyan@jupyter-qupyter:~/strategy2$ qup deploy ./5min_breakout_strategy.py
START DEPLOYMENT
- strategy_name: 5min-breakout-strategy
- entry_filename: ./5min_breakout_strategy.py

done. kghoon_7e888d06.zip
Create new pod...
Wait for pod ready...
Pod is ready - name: qupyter-volatility-break-zfclnmrp
done
jovyan@jupyter-qupyter:~/strategy2$
```

### 배포된 전략 목록 확인

배포가 완료되면 아래와 같이 `qup list` 명령을 사용해서 배포된 전략 목록에서 확인 할 수 있습니다.

```bash
jovyan@jupyter-qupyter:~/strategy2$ qup list
STRATEGY           DEPLOYMENT ID                      STATUS     CREATED AT
5min-breakout-strategy   qupyter-5min-breakout-strategy-zfclnmrp   Running    2023-10-19 06:49:28
jovyan@jupyter-qupyter:~/strategy2$
```

### 배포된 전략 실행 로그 확인

아래와 같이 `qup logs` 명령을 사용하여 로그를 확인 할 수 있습니다.

```bash
Usage: qup logs [OPTIONS] DEPLOYMENT_ID

  Show logs for deployed strategy

Options:
  -f, --follow  Specify if the logs should be streamed.
  --help        Show this message and exit.
```

로그 확인 시에는 `qup list`에서 확인 할 수 있는 `DEPLOYMENT ID` 를 인자로 전달합니다.
`-f` 옵션을 사용하면 로그를 실시간으로 tailing 할 수 있습니다.

```bash
jovyan@jupyter-qupyter:~/strategy2$ qup logs qupyter-5min-breakout-strategy-zfclnmrp
Collecting finance-datareader==0.9.50
  Downloading finance_datareader-0.9.50-py3-none-any.whl (19 kB)
Collecting bs4==0.0.1
  Downloading bs4-0.0.1.tar.gz (1.1 kB)
  Preparing metadata (setup.py): started
  Preparing metadata (setup.py): finished with status 'done'
Collecting requests-file
  Downloading requests_file-1.5.1-py2.py3-none-any.whl (3.7 kB)
Collecting lxml
  Downloading lxml-4.9.3-cp310-cp310-musllinux_1_1_x86_64.whl (7.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.7/7.7 MB 52.9 MB/s eta 0:00:00

...
..
.

target_price:191650.0 current_price:188900
2023-10-19 15:38:53.182729 [EXECUTOR] Call trade_func hook
today_open:69700 yesterday_range:1700.0 k:0.5
target_price:70550.0 current_price:69500
today_open:189900 yesterday_range:3500.0 k:0.5
target_price:191650.0 current_price:188900
jovyan@jupyter-qupyter:~/strategy2$
```
