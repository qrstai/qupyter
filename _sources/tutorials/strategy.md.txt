# 전략 코드 작성하기

Qupyter engine은 다음과 같은 순서로 동작합니다.
아래 설명 중 코멘트에 `(Hook)` 적혀있는 함수들은 사용자가 직접 작성이 가능한 함수 입니다.

```{note}
아래 코드(run 함수)는 사용자가 직접 작성하는 부분이 아닌, Qupyter Engine의 동작 흐름를 보여주기 위한 의사 코드(psuedo code) 입니다.
```

```python
async def run():
  # (Hook) 초기화를 진행합니다. 필요한 설정 값을 반환합니다.
  config = await on_initialize()

  # 사용자가 반환 한 설정 값을 적용합니다
  update_config(config)

  # (Hook) 당일 거래 시작 시 `on_market_open` hook을 호출합니다.
  trade_signals = await on_market_open(account_info, pending_orders, positions, broker)

  # 증권사 API를 통해 매매 지시를 실행합니다.
  execute_trades(trade_signals)

  while is_trading_time:
    # (Hook) 미체결 주문을 처리합니다
    await handle_pending_positions(pending_orders, broker)

    # 손절 조건이 설정 된 경우 확인하고 처리합니다.
    await monitor_stop_loss(positions, stop_loss_config, broker)

    # 익절 조건을 설정 된 경우 확인하고 처리합니다.
    await monitor_take_profit(positions, take_profit_config, broker)

    # (Hook) 전략을 실행하고, 매매 지시를 반환합니다.
    trade_signals = await trade_func(account_info, pending_orders, positions, broker)

    # 증권사 API를 통해 사용자 매매 지지를 실행합니다.
    execute_trades(trade_signals)

    # 정해 진 interval 만큼 대기합니다.
    sleep(interval)

  # (Hook) 당일 거래 종료 시 `on_market_close` hook을 호출합니다.
  trade_signals = await on_market_close(account_info, pending_orders, positions, broker)

  # 증권사 API를 통해 매매 지시를 실행합니다.
  execute_trades(trade_signals)
```

## Hooks

다음은 각각의 hook 들에 대한 설명입니다.

### on_initialize

사용자 전략 실행 시 처음 한번 실행되는 함수입니다. 필요한 초기화 작업을 수행하고 실행주기, 손/익절 조건등의 설정 값을 반환하도록 작성합니다.

```python
async def on_initialize():
  """ 필요한 사용자 초기화 코드를 실행합니다 """
  config = {
    # 증권사 식별자. ebest 또는 kis
    'brokerage': 'ebest',

    # 전략 실행 주기(초). 기본값: 1분
    'interval': 60,

    # 손절 조건 등록 (optional)
    'stop_loss_config': {
      'A005930': -0.1 # 삼성전자 종목을 평단가 대비 -10% 손실인 경우 손절
    },

    # 익절 조건 (optional)
    'take_profit_config': {
      'A005930': 0.1 # 삼성전자 종목을 평단가 대비 10% 이상 수익인 경우 익절
    },

    # 거래 시작 시간 조정 (초). 기본값 300(5분)
    'open_market_time_margin': 300,

    # 거래 마감 시간 조정 (초). 기본값 300(5분)
    'close_market_time_margin': 300,

    # 모의 투자 환경 여부. 기본값 False(실거래)
    'test_trade': False,

    # 증권사 계좌 상세 정보
    'broker_settings': {
      # 계좌번호 (56781234-01 중 앞 부분)
      'account_number': '56781234',

      # 계좌 상품번호 (56781234-01 중 뒤 2자리)
      'product_code': '01',

      # (법인) 법인 계좌 여부
      'is_corp': False,

      # (법인) 증권사에 등록된 전화번호
      'phone_number': '',

      # (법인) 제휴사 회원 관리를 위한 고객식별키
      'personal_secret_key': ''

      # (법인) 증권사 등록 일련번호
      'seq_no': '',

      # (법인) 증권사 등록 IP 주소
      'ip_addr': '',
    }
  }

  return config

```

다음은 각 설정값에 대한 설명입니다.

- brokerage: 증권사 식별자 (ebest: 이베스트증권, kis: 한국투자증권)
- interval : 거래 주기 (trade_func 가 호출되는 간격) 입니다. 기본 값은 1분입니다.
- stop_loss_config : 손절 조건을 등록합니다. 가격을 확인하는 주기는 위 `interval`과 같습니다.
- take_profit_config : 익절 조건을 등록합니다. 가격을 확인하는 주기는 위 `interval`과 같습니다.
- open_market_time_margin : 거래 시작시간을 조정하기 위해 사용됩니다. 지정된 시간 만큼 거래 시작 시간을 지연합니다.
- close_market_time_margin: 거래 종료시간을 조정하기 위해 사용됩니다. 지정된 시간 만큼 먼저 당일 거래를 마감합니다.
- test_trade: 모의투자 환경 여부. True로 설정하면 모의투자용 API key를 사용하여 모의투자 환경에서 거래를 진행합니다.

아래 항목은 증권사 계정 상세 정보에 대한 설명입니다. 현재 한국투자증권을 이용하는 경우에만 필요합니다.

- broker_settings.account_number : 계좌번호.
- broker_settings.product_code: 계좌상품번호.

아래 항목들은 법인계좌를 이용하는 경우에만 필요합니다.

- broker_settings.is_corp: 법인계좌여부 (기본값: False)
- broker_settings.phone_number: 법인 전화번호. 한국투자증권 법인계좌인 경우 필요합니다.
- broker_settings.personal_secret_key: 제휴사 회원 관리를 위한 고객식별키. 한국투자증권 법인계좌이고 제휴사인 경우 필요합니다.
- broker_settings.seq_no: 일련번호. 한국투자증권 법인계좌인 경우 필요합니다.
- broker_settings.ip_addr: IP 주소. 한국투자증권 법인계좌인 경우 필요합니다.

### on_market_open

```{note}
파라미터와 반환값 정보는 [Hooks - on_market_open](qrst.hooks.on_market_open) 문서를 참고하세요.
```

매일 거래 시작 시 가장 먼저 1회 호출 됩니다.

이 hook이 호출되는 시간은 당일 장 거래 시작 시간 (보통 9시, 수능일은 10시) + 사용자가 설정 한 `open_market_time_margin` 초를 더한 시간입니다. 예를 들어 사용자가 `open_market_time_margin`을 300(5분)으로 설정한 경우, 9시 5분에 `on_market_open`이 호출됩니다.

```{warning}
- 처음 전략 실행 또는 업데이트 시 시간이 위 호출 시간 보다 5분이 경과한 경우, 이 hook은 호출되지 않습니다.
- 이 hook이 호출되고 5분 이내에 전략을 업데이트하게 되면 이 hook은 다시 호출 됩니다.
```

### on_market_close

```{note}
파라미터와 반환값 정보는 [Hooks - on_market_close](qrst.hooks.on_market_close) 문서를 참고하세요.
```

매일 거래 종료 시 마지막에 1회 호출 됩니다.

이 hook이 호출되고 나면 해당일에는 더이상 `trade_func` 가 호출되지 않습니다.

이 hook이 호출되는 시간은 당일 장 종료 전 동시 호가 시작 시간 (보통 3시 20분) 에서 사용자가 설정한 `close_market_time_margin` 초를 뺀 시간입니다.

예를 들어 사용자가 `close_market_time_margin`을 600(10분)으로 설정한 경우, 3시 10분에 `on_market_close` hook이 호출됩니다.

```{warning}
- 당일 동시 호가 시작 이후에 전략이 새로 배포되거나 업데이트 된 경우 이 hook은 호출되지 않습니다.
- 이 hook이 호출되고 실제 동시호가 시작 시간 전에 전략을 업데이트하게 되면 이 hook은 다시 호출됩니다.
```


### trade_func

사용자 전략 코드를 구현합니다. 설정 된 주기마다 호출 되고 매매지시가 필요한 경우 응답으로 전달합니다.

```python
async def trade_func(account_info, pending_orders, positions, broker):
  """사용자 전략 코드 구현.

  Args:
    account_info (dict): 계좌 정보.
    pending_orders (tuple): 미체결 주문 목록.
    positions (list): 보유 포지션.
    broker (StockBroker): 시세 조회를 위한 증권 사 API wrapper.

  Returns:
    매매 지시 목록, 없는 경우 `None`.
  """


  ##### 전략 코드 작성 #####

  return [
    ( 'A005930', 69100, 13 ), # 삼성전자 13주를 69100원에 매수
    ( 'A252670', 2800, -1 ), # KODEX 200 선물 인버스2X 1주를 2800원에 매도
  ]
```

```{note}
파라미터에 대한 자세한 설명은 [Hooks - trade_func()](qrst.hooks.trade_func)
문서를 참고하세요.
```

### handle_pending_orders

미체결 주문을 확인하고 정정/취소할 내역을 반환합니다. 매 주기마다 `trade_func` 가 호출되기 전 미체결주문이 남아있으면 호출됩니다.

```{note}
이 hook을 구현하지 않은 경우의 기본 동작은 미체결 주문을 모두 취소하는 것입니다.
```

```python
async def handle_pending_orders(pending_orders, broker):
  result = []

  for (asset_code, orders) in pending_orders:
    for order in orders:
      if order.price != order.current_price: # 제출한 주문 가격과 현재 가격이 달라진 경우
        if order.trade_type == 1: # 매도 주문의 경우 변경된 주문으로 정정하는 주문을 제출합니다.
          print(f"[handle_pending_orders] update order price: {order.asset_code}) {order.price} -> {order.current_price}")
          result.append((asset_code, order.order_id, order.current_price, order.quantity))
        else: # 매수 주문의 경우 기존 주문을 취소합니다.
          print(f"[handle_pending_orders] cancel order: {order.asset_code} {order.price} -> {order.current_price}")
          result.append((asset_code, order.order_id, 0, -1*order.quantity))

  return result
```

`(종목코드, 원주문번호, 정정가격, 수량)` 형식의 튜플을 원소로 갖는 리스트를 반환합니다.

- 전량/일부 취소의 경우 가격은 None 으로 지정하고 취소하고자하는 수량을 음수로 지정합니다.
- 정정의 경우 가격과 수량을 지정합니다.

```{note}
파라미터와 응답형식에 대한 자세한 설명은 [Hooks - handle_pending_orders()](qrst.hooks.handle_pending_orders)
문서를 참고하세요.
```
