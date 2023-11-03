"""
qupyter 전략 단위 테스트를 위한 Mock 객체들을 정의합니다.

아래와 같은 방법으로 사용할 수 있습니다.

:examples:

.. code-block:: python

    import asyncio
    from qupyter import test
    from qupyter.brokerage.ebest import EBestStockBroker

    def test_trade_func():
        broker = EBestStockBroker(test_trade=True)
        account_info = broker.get_account()

        positions = [
            test.position(asset_code='005930', quantity=10, average_purchase_price=68000, current_price=70000),
            test.position(asset_code='252670', quantity=10, average_purchase_price=2800, current_price=3000),
        ]

        pending_orders = [
            test.order(asset_code='005930', trade_type='1', quantity=10, price=68000),
            test.order(asset_code='252670', trade_type='2', quantity=10, price=2800),
        ]

        result = asyncio.run(trade_func(account_info, pending_orders, positions, broker))
        print(result)


"""

import random

from datetime import datetime
from qupyter.brokerage import StockOrder, StockPosition


def order(**kwargs) -> StockOrder:
    """
    StockOrder Mock 객체 생성

    아래 필드들은 모두 선택적으로 지정할 수 있습니다.

    :param order_id: 주문번호 (기본값: 1~999999 사이의 임의의 정수)
    :type order_id: int
    :param asset_code: 종목코드 (기본값: '005930')
    :type asset_code: str
    :param trade_type: 매매구분 (1: 매도, 2: 매수) (기본값: 1)
    :type trade_type: str
    :param quantity: 주문수량 (기본값: 1)
    :type quantity: int
    :param price: 주문가격 (기본값: 68000)
    :type price: int
    :param filled_quantity: 체결수량 (기본값: 0)
    :type filled_quantity: int
    :param filled_price: 체결가격 (기본값: 0)
    :type filled_price: int
    :param pending_quantity: 미체결수량 (기본값: quantity - filled_quantity)
    :type pending_quantity: int
    :param order_time: 주문시간 (기본값: 현재시간)
    :type order_time: datetime
    :param order_method: 주문방식 (기본값: 'TEST')
    :type order_method: str
    :param current_price: 현재가 (기본값: 68000)
    :type current_price: int

    :return: 주문 객체
    :rtype: StockOrder
    """
    order_id = kwargs.get('order_id', random.randint(1, 999999))
    asset_code = kwargs.get('asset_code', '005930') # 삼성전자
    trade_type = kwargs.get('trade_type', '1') # 매도
    quantity = kwargs.get('quantity', 1)
    price = kwargs.get('price', 68000)
    filled_quantity = kwargs.get('filled_quantity', 0)
    filled_price = kwargs.get('filled_price', 0)
    pending_quantity = kwargs.get('pending_quantity', quantity - filled_quantity)
    order_time = kwargs.get('order_time', datetime.now())
    order_method = kwargs.get('order_method', 'TEST')
    current_price = kwargs.get('current_price', 68000)

    return StockOrder(order_id, asset_code, trade_type, quantity, price, filled_quantity, filled_price, pending_quantity, order_time, order_method, current_price)


def position(**kwargs) -> StockPosition:
    """
    StockPosition Mock 객체 생성

    아래 필드들은 모두 선택적으로 지정할 수 있습니다.

    :param asset_code: 종목코드 (기본값: '005930')
    :type asset_code: str
    :param asset_name: 종목명 (기본값: '삼성전자')
    :type asset_name: str
    :param quantity: 보유수량 (기본값: 1)
    :type quantity: int
    :param exit_available_quantity: 청산가능수량 (기본값: quantity)
    :type exit_available_quantity: int
    :param average_purchase_price: 평균매입가 (기본값: 68000)
    :type average_purchase_price: int
    :param purchase_value: 매입금액 (기본값: average_purchase_price * quantity)
    :type purchase_value: int
    :param loan_value: 대출금액 (기본값: 0)
    :type loan_value: int
    :param loan_date: 대출일 (기본값: None)
    :type loan_date: datetime.date
    :param expiration_date: 만기일 (기본값: None)
    :type expiration_date: datetime.date
    :param current_price: 현재가 (기본값: 68000)
    :type current_price: int
    :param commission: 수수료 (기본값: 0)
    :type commission: int
    :param tax: 세금 (기본값: 0)
    :type tax: int
    :param loan_interest: 대출이자 (기본값: 0)
    :type loan_interest: int
    :param current_value: 평가금액 (기본값: current_price * quantity)
    :type current_value: int
    :param current_pnl: 평가손익 (기본값: (current_price - average_purchase_price) * quantity -  commission - loan_interest)
    :type current_pnl: int
    :param current_pnl_pct: 수익률 (기본값: current_pnl / (average_purchase_price * quantity) * 100)
    :type current_pnl_pct: float

    :return: 포지션 객체
    :rtype: StockPosition

    """
    asset_code = kwargs.get('asset_code', '005930') # 삼성전자
    asset_name = kwargs.get('asset_name', '삼성전자')
    quantity = kwargs.get('quantity', 1)
    exit_available_quantity = kwargs.get('exit_available_quantity', quantity)
    average_purchase_price = kwargs.get('average_purchase_price', 68000)
    purchase_value = kwargs.get('purchase_value', average_purchase_price * quantity)
    loan_value = kwargs.get('loan_value', 0)
    loan_date = kwargs.get('loan_date', None)
    expiration_date = kwargs.get('expiration_date', None)
    current_price = kwargs.get('current_price', 68000)
    commission = kwargs.get('commission', 0)
    tax = kwargs.get('tax', 0)
    loan_interest = kwargs.get('load_interest', 0)
    current_value = kwargs.get('current_value', current_price * quantity)
    current_pnl = kwargs.get('current_pnl', (current_price - average_purchase_price) * quantity -  commission - loan_interest)
    current_pnl_pct = kwargs.get('current_pnl_pct', current_pnl / (average_purchase_price * quantity) * 100)

    return StockPosition(asset_code, asset_name, quantity, exit_available_quantity, average_purchase_price, purchase_value, loan_value, loan_date, expiration_date, current_price, current_value, current_pnl, current_pnl_pct, commission, tax, loan_interest)


