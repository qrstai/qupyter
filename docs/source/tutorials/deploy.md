# 전략 배포 하기

Qupyter platform 에 작성한 전략을 배포하는 방법을 살펴보겠습니다.

## 전략 코드 준비

사용자가 직접 작성한 전략 코드를 준비합니다. 다음은 변동성 돌파 전략을 구현한 예제 코드입니다.

### volatility_break.py

```python

import FinanceDataReader as fdr
from datetime import timedelta, datetime

async def on_initialize():
    return {
        'interval': 60, # 거래 주기는 60초로 지정합니다
    }

async def trade_func(user_account, pending_orders, positions, broker):
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    target_asset_codes = [
        'A005930', # 삼성전자
        'A005380', # 현대자동차
    ]

    def __get_current_price_map(asset_codes):
        """ 이베스트 API가 전달하는 가격정보를 종목키를 기준으로 grouping 하여 반환 """
        docs = broker.get_current_prices(asset_codes)
        result_map = {}
        for d in docs:
            result_map[d['shcode']] = d
        return result_map

    def __have_position(asset_code):
        """ 해당 종목을 보유중이거나 주문이 진행중인지 확인 """
        for p in positions:
            if p.asset_code == asset_code:
                return True

        for o in pending_orders:
            if o.asset_code == asset_code and o.quantity > 0:
                return True

        return False


    # 보유 중인 포지션을 장시작시 시장가에 모두 매도
    if now.hour == 9 and now.minute == 10 and positions.length > 0:
        result = []

        price_map = __get_current_price_map(list(map(lambda p: p.asset_code, positions)))

        for p in positions:
            result.append({ p.asset_code, price_map[p.asset_code], p.quantity * -1 })

        return result

    else:
        result = []
        total_balance = user_account['total_balance'] * 0.8
        price_map = __get_current_price_map(target_asset_codes)

        for asset_code in target_asset_codes:
            shcode = asset_code[1:]

            if not __have_position(shcode):
                read_start = (yesterday - timedelta(days=7)).strftime('%Y-%m-%d')
                read_end = yesterday.strftime('%Y-%m-%d')

                # finance-datareader 에서 오늘을 제외한 최근 7거래일의 가격 정보를 가져온다.
                df = fdr.DataReader(shcode, read_start, read_end)
                if df is None or len(df) == 0:
                    print('Error: yesterday price data not available')
                    continue

                yesterday_series = df.iloc[-1]

                # 마지막 거래일의 가격 변동폭 (고가-저가) 을 구한다.
                yesterday_range = yesterday_series['High'] - yesterday_series['Low']

                # 오늘 시가를 구한다.
                today_open = price_map[shcode]['open']

                # 진입 조건 강도 조절을 위한 상수
                k = 0.5

                # 목표가격 = 오늘 시가 + 어제의 변동폭 * 상수
                target_price = today_open + yesterday_range * k

                # 현재가격
                current_price = price_map[shcode]['price']

                print(f"오늘 시작가={today_open} 최근 거래일 변동폭={yesterday_range} k:{k}", end="")
                print(f"목표가={target_price} 현재가={current_price}")

                # 현재 가격이 목표가격에 도달한 경우 진입한다
                if current_price >= target_price:
                    budget = int(total_balance / len(target_asset_codes))
                    quantity = int(budget / current_price)

                    if quantity > 0:
                        result.append((asset_code, current_price, quantity))

        for p in positions:
            print(f"{p.asset_name}({p.asset_code}) : {p.current_pnl} ({p.current_pnl_pct}%) ", end="")
            print(f"현재가={p.current_price} 평단가={p.average_purchase_price} ", end="")
            print(f"수수료={p.commission} 세금={p.tax} 신용이자={p.loan_interest}")

        return result
```

전략코드 실행에 필요한 package를 requirements.txt에 나열합니다

### requirements.txt

```text
finance-datareader==0.9.50
bs4==0.0.1
```

## 배포

배포는 `qup deploy` 명령을 사용해서 진행합니다.

```bash
jovyan@jupyter-kghoon:~/strategy2$ qup deploy --help
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
jovyan@jupyter-kghoon:~/strategy2$ qup deploy ./volatility_break.py
START DEPLOYMENT
- strategy_name: volatility-break
- entry_filename: ./volatility_break.py

done. kghoon_7e888d06.zip
Create new pod...
Wait for pod ready...
Pod is ready - name: kghoon-volatility-break-zfclnmrp
done
jovyan@jupyter-kghoon:~/strategy2$
```

### 배포된 전략 목록 확인

배포가 완료되면 아래와 같이 `qup list` 명령을 사용해서 배포된 전략 목록에서 확인 할 수 있습니다.

```bash
jovyan@jupyter-kghoon:~/strategy2$ qup list
STRATEGY           DEPLOYMENT ID                      STATUS     CREATED AT
volatility-break   kghoon-volatility-break-zfclnmrp   Running    2023-10-19 06:49:28
jovyan@jupyter-kghoon:~/strategy2$
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
jovyan@jupyter-kghoon:~/strategy2$ qup logs kghoon-volatility-break-zfclnmrp
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
jovyan@jupyter-kghoon:~/strategy2$
```
