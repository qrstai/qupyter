
# 유닛 테스트 작성하기

아래는 qupyter의 [Unittest Helpers](qupyter.test.MockStockBroker) 를 활용한 5분봉 돌파전략에 대한 예제 유닛 테스트 코드 입니다.

## tests.py

```python

import unittest
import os
import five_min_breakout as strategy

from qupyter import test

class Test5MinBreakoutStrategy(unittest.IsolatedAsyncioTestCase):

    async def test_sell_signal(self):
        broker = test.MockStockBroker()
        asset_code = 'A005930'

        # 현재가를 7만원으로 설정
        broker.set_price(asset_code, current_price=70000)

        # 최근 분봉의 저가를 6만원, 고가를 6만5천원으로 설정
        broker.set_historical_minute_data(asset_code, [{'low': 60000, 'high': 65000}])

        # 투자 가능금액을 10만원으로 설정
        broker.set_account(investable_cash=100000)

        account_info = broker.get_account()
        pending_orders = []

        # 매도 가능한 보유포지션을 설정
        positions = [test.position(asset_code=asset_code, quantity=1)]

        result = await strategy.trade_func(account_info, pending_orders, positions, broker)

        # 매도 지시 결과 기본 형식 검증
        test.validate_trade_func_result(result)

        # 매도 지시가 생성되었는지 확인
        self.assertEqual(len(result), 1)

        # 매도 지시의 종목 코드, 가격, 수량이 정확한지 확인
        asset_code, price, qty = result[0]

        self.assertEqual(asset_code, 'A005930')
        self.assertEqual(price, 70000)
        self.assertEqual(qty, 1) # -1 이 맞는 값. 테스트를 위해 일부러 틀린 값으로 작성.


if __name__ == '__main__':
    unittest.main()

```

- [MockStockBroker](qupyter.test.MockStockBroker) 를 사용하여 `StockBroker`의 시세 조회 함수가 반환하는 값을 mocking 할 수 있습니다.
위 예제 코드에서는 현재가, 분봉, 현금 잔고등을 원하는 값으로 지정했습니다.

- [position](qupyter.test.position), [order](qupyter.test.order)를 사용하여 필요한 mock 객체를 생성할 수 있습니다.
위 예제 코드에서는 매도할 보유 포지션을 전달하기 위해 `position` 함수를 사용했습니다.

- [validate_trade_func_result](qupyter.test.validate_trade_func_result), [validate_handle_pending_orders_result](qupyter.test.validate_handle_pending_orders_result) validator 함수를 사용하여 사용자 작성 hook이 반환하는 결과 값에 대한 기본적은 형식 검증을 할 수 있습니다.

## 실행

위 코드를 실행한 결과는 다음과 같습니다.

```bash
(base) jovyan@jupyter-kghoon:~/5min_breakout$ python ./tests.py
.F
======================================================================
FAIL: test_sell_signal (__main__.Test5MinBreakoutStrategy)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/opt/conda/lib/python3.10/unittest/async_case.py", line 64, in _callTestMethod
    self._callMaybeAsync(method)
  File "/opt/conda/lib/python3.10/unittest/async_case.py", line 87, in _callMaybeAsync
    return self._asyncioTestLoop.run_until_complete(fut)
  File "/opt/conda/lib/python3.10/asyncio/base_events.py", line 649, in run_until_complete
    return future.result()
  File "/opt/conda/lib/python3.10/unittest/async_case.py", line 101, in _asyncioLoopRunner
    ret = await awaitable
  File "/home/jovyan/5min_breakout/./tests.py", line 68, in test_sell_signal
    self.assertEqual(qty, 1)
AssertionError: -1 != 1

----------------------------------------------------------------------
Ran 2 tests in 0.019s
```

제일 하단 코드를 수정하고 다시 실행합니다.

```python

...
        self.assertEqual(qty, -1) # -1 로 수정

```

다시 실행.

```bash
(base) jovyan@jupyter-kghoon:~/5min_breakout$ python ./tests.py
..
----------------------------------------------------------------------
Ran 1 tests in 0.020s

OK
```
