# 전략 코드 작성하기

Qupyter engine은 다음과 같은 순서로 동작합니다.
아래 설명 중 코멘트에 `(Hook)` 적혀있는 함수들은 사용자가 직접 작성이 가능한 함수 입니다.

```python
async def run():
  # (Hook) 초기화를 진행합니다. 필요한 설정 값을 반환합니다.
  config = await on_initialize()

  # 사용자가 반환 한 설정 값을 적용합니다
  update_config(config)

  while True:
    # 미체결 주문을 처리합니다
    await handle_pending_positions(pending_orders)

    # 손절 조건이 설정 된 경우 확인하고 처리합니다.
    await monitor_stop_loss(positions, stop_loss_config)

    # 익절 조건을 설정 된 경우 확인하고 처리합니다.
    await monitor_take_profit(positions, take_profit_config)

    # (Hook) 전략을 실행하고, 매매 지시를 반환합니다.
    trade_signals = await trade_func()

    # 증권사 API를 통해 사용자 매매 지지를 실행합니다.
    execute_trades(trade_signals)

    # 정해 진 interval 만큼 대기합니다.
    sleep(interval)
```

## Hooks

다음은 각각의 hook 들에 대한 설명입니다.

### on_intialize

사용자 전략 실행 시 처음 한번 실행되는 함수입니다. 필요한 초기화 작업을 수행하고 실행주기, 손/익절 조건등의 설정 값을 반환하도록 작성합니다.

```python
async def on_initialize() {
  """ 필요한 사용자 초기화 코드를 실행합니다 """
  config = {
    'interval': 30, # 전략 실행 주기. 기본값: 10분

    'stop_loss_config': { # 손절 조건 등록 (optional)
      'A005930': -0.1 # 삼성전자 종목을 평단가 대비 -10% 손실인 경우 손절
    },

    'take_profit_config': { # 익절 조건 (optional)
      'A005930': 0.1 # 삼성전자 종목을 평단가 대비 10% 이상 수익인 경우 익절
    }
  }

  return config
}
```

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
    { 'A005930', 69100, 13 }, # 삼성전자 13주를 69100원에 매수
    { 'A252670', 2800, -1 }, # KODEX 200 선물 인버스2X 1주를 2800원에 매도
  ]
```
