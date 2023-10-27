# 전략 코드 작성하기

Qupyter engine은 다음과 같은 순서로 동작합니다.
아래 설명 중 코멘트에 `(Hook)` 적혀있는 함수들은 사용자가 직접 작성이 가능한 함수 입니다.

```python
async def run():
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

## Hooks

다음은 각각의 hook 들에 대한 설명입니다.

### on_initialize

사용자 전략 실행 시 처음 한번 실행되는 함수입니다. 필요한 초기화 작업을 수행하고 실행주기, 손/익절 조건등의 설정 값을 반환하도록 작성합니다.

```python
async def on_initialize():
  """ 필요한 사용자 초기화 코드를 실행합니다 """
  config = {
    'interval': 60, # 전략 실행 주기(초). 기본값: 1분

    'stop_loss_config': { # 손절 조건 등록 (optional)
      'A005930': -0.1 # 삼성전자 종목을 평단가 대비 -10% 손실인 경우 손절
    },

    'take_profit_config': { # 익절 조건 (optional)
      'A005930': 0.1 # 삼성전자 종목을 평단가 대비 10% 이상 수익인 경우 익절
    },

    'open_market_time_margin': 300, # 거래 시작 시간 조정 (초). 기본값 300(5분)

    'close_market_time_margin': 300, # 거래 마감 시간 조정 (초). 기본값 300(5분)

    'test_trade': False, # 모의 투자 환경 여부. 기본값 False(실거래)
  }

  return config

```

다음은 각 설정값에 대한 설명입니다.

- interval : 거래 주기 (trade_func 가 호출되는 간격) 입니다. 기본 값은 1분입니다.
- stop_loss_config : 손절 조건을 등록합니다. 가격을 확인하는 주기는 위 `interval`과 같습니다.
- take_profit_config : 익절 조건을 등록합니다. 가격을 확인하는 주기는 위 `interval`과 같습니다.
- open_market_time_margin : 거래 시작시간을 조정하기 위해 사용됩니다. 지정된 시간 만큼 거래 시작 시간을 지연합니다.
- close_market_time_margin: 거래 종료시간을 조정하기 위해 사용됩니다. 지정된 시간 만큼 먼저 당일 거래를 마감합니다.
- test_trade: 모의투자 환경 여부. True로 설정하면 모의투자용 API key를 사용하여 모의투자 환경에서 거래를 진행합니다.

### on_market_open

매일 거래 시작 시 가장 먼저 1회 호출 됩니다.

이 hook이 호출되는 시간은 당일 장 거래 시작 시간 (보통 9시, 수능일은 10시) + 사용자가 설정 한 `open_market_time_margin` 초를 더한 시간입니다.
예를 들어 사용자가 `open_market_time_margin`을 300(5분)으로 설정한 경우, 9시 5분에 `on_market_open`이 호출됩니다.

#### on_market_open 사용 시 주의 사항

- 처음 전략 실행 또는 업데이트 시 시간이 위 호출 시간 보다 5분이 경과한 경우, 이 hook은 호출되지 않습니다.
- 이 hook이 호출되고 5분 이내에 전략을 업데이트하게 되면 이 hook은 다시 호출 됩니다.

### on_market_close

매일 거래 종료 시 마지막에 1회 호출 됩니다.

이 hook이 호출되고 나면 해당일에는 더이상 `trade_func` 가 호출되지 않습니다.

이 hook이 호출되는 시간은 당일 장 종료 전 동시 호가 시작 시간 (보통 3시 20분) 에서 사용자가 설정한 `close_market_time_margin` 초를 뺀 시간입니다.
예를 들어 사용자가 `close_market_time_margin`을 600(10분)으로 설정한 경우, 3시 10분에 `on_market_close` hook이 호출됩니다.

#### on_market_close 사용 시 주의 사항

- 당일 동시 호가 시작 이후에 전략이 새로 배포되거나 업데이트 된 경우 이 hook은 호출되지 않습니다.
- 이 hook이 호출되고 실제 동시호가 시작 시간 전에 전략을 업데이트하게 되면 이 hook은 다시 호출됩니다.

### trade_func

사용자 전략 코드를 구현합니다. 설정 된 주기마다 호출 되고 매매지시가 필요한 경우 응답으로 전달합니다.

```python
async def trade_func(account_info, pending_orders, positions, broker) -> List:
  """사용자 전략 코드 구현.

  Args:
    account_info: 계좌 정보.
    pending_orders: 미체결 주문 목록.
    positions: 보유 포지션.
    broker: 시세 조회를 위한 증권 사 API wrapper.

  Returns:
    매매 지시 목록, 없는 경우 `None`.
  """


  ##### 전략 코드 작성 #####

  return [
    ( 'A005930', 69100, 13 ), # 삼성전자 13주를 69100원에 매수
    ( 'A252670', 2800, -1 ), # KODEX 200 선물 인버스2X 1주를 2800원에 매도
  ]
```
