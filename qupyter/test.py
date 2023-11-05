"""
qupyter 전략 단위 테스트를 위한 Mock 객체들을 정의합니다.

아래와 같은 방법으로 사용할 수 있습니다.

:examples:

.. code-block:: python

    import asyncio
    from qupyter import test
    from qupyter.brokerage.ebest import EBestStockBroker

    def trade_func(account_info, pending_orders, positions, stock_broker):
        # 사용자 전략 코드 작성
        # ...

    if __name__ == '__main__':
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

        result = trade_func(account_info, pending_orders, positions, broker)
        print(result)


"""

import random

from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

import pandas as pd
from qupyter.brokerage import StockOrder, StockPosition, StockBroker


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


class MockStockBroker(StockBroker):
    def __init__(self):
        self.prices = {}
        self.historical_minute_datas = {}
        self.historical_daily_datas = {}
        self.account_info = {}

    def set_price(self, asset_code: str, **kwargs):
        """ Mock 가격 데이터 설정

        :param asset_code: 종목코드
        :type asset_code: str
        :param kwargs: 설정 할 가격 데이터
        :type kwargs: Dict

        :examples:

        .. code-block:: python

            mock_broker.set_price('005930', current_price=70000, max_price=82560)
        """
        self.prices[asset_code] = kwargs

    def get_price(self, asset_code) -> pd.DataFrame:
        data = {
            'code': asset_code,
            'name': asset_code,
            'current_price': 68000,
            'volume': 10527625,
            'volume_nominal': 718811000000,
            'open_price': 68800,
            'high_price': 68800,
            'low_price': 68000,
            'max_price': 82560,
            'min_price': 55040,
            'market_capitalization': 510000000000000,
            'ask_price_1': 68500,
            'ask_volume_1': 107929,
            'bid_price_1': 67600,
            'bid_volume_1': 99315,
            'ask_price_2': 68600,
            'ask_volume_2': 113,
            'bid_price_2': 67500,
            'bid_volume_2': 100,
            'ask_price_3': 68700,
            'ask_volume_3': 100,
            'bid_price_3': 67400,
            'bid_volume_3': 100,
            'ask_price_4': 68800,
            'ask_volume_4': 100,
            'bid_price_4': 67300,
            'bid_volume_4': 100,
            'ask_price_5': 68900,
            'ask_volume_5': 100,
            'bid_price_5': 67200,
            'bid_volume_5': 100,
            'ask_volume_total': 554013,
            'bid_volume_total': 1069461,
        }

        if asset_code in self.prices:
            data.update(self.prices[asset_code])

        df = pd.DataFrame([data])
        df.set_index('code', inplace=True)
        return df


    def get_price_for_multiple_stocks(self, asset_codes: List[str]) -> pd.DataFrame:
        dataset = []

        for asset_code in asset_codes:
            dataset.append(self.get_price(asset_code))

        df = pd.DataFrame(dataset)
        df.set_index('code', inplace=True)
        return df


    def set_historical_minute_data(self, asset_code: str, values: List[Dict|int]):
        """
        Mock 분봉 데이터 설정

        :param asset_code: 종목코드
        :type asset_code: str
        :param values: 설정 할 분봉 데이터
        :type values: List[Dict|int]

        :examples:

        .. code-block:: python

            >>> from qupyter.test import MockStockBroker
            >>> from datetime import date
            >>> mock_broker = MockStockBroker()
            >>> mock_broker.set_historical_minute_data('005930', [
            ...     {'open': 70000, 'high': 70000, 'low': 70000, 'close': 70000, 'volume': 0, 'volume_nominal': 0},
            ...     {'open': 70000, 'high': 71000, 'low': 70000, 'close': 71000, 'volume': 0, 'volume_nominal': 0},
            ...     {'open': 71000, 'high': 72000, 'low': 70000, 'close': 72000, 'volume': 0, 'volume_nominal': 0},
            ...     {'open': 72000, 'high': 72000, 'low': 70000, 'close': 70000, 'volume': 0, 'volume_nominal': 0},
            ... ])
            >>> mock_broker.get_historical_minute_data('005930', interval=1, first_date=date(2023, 11, 2))
                                open   high    low  close  volume  volume_nominal
            datetime
            2023-11-02 09:05:00  70000  70000  70000  70000       0               0
            2023-11-02 09:06:00  70000  70000  70000  70000       0               0
            2023-11-02 09:07:00  70000  70000  70000  70000       0               0
            2023-11-02 09:08:00  70000  70000  70000  70000       0               0
            2023-11-02 09:09:00  70000  70000  70000  70000       0               0
            ...                    ...    ...    ...    ...     ...             ...
            2023-11-03 15:15:00  70000  70000  70000  70000       0               0
            2023-11-03 15:16:00  70000  70000  70000  70000       0               0
            2023-11-03 15:17:00  70000  71000  70000  71000       0               0
            2023-11-03 15:18:00  71000  72000  70000  72000       0               0
            2023-11-03 15:19:00  72000  72000  70000  70000       0               0

            [750 rows x 6 columns]

            >>> mock_broker.set_historical_minute_data('005380', [182000, 183000, 184000])
            >>> mock_broker.get_historical_minute_data('005380', first_date=date(2023, 11, 2))
                                open    high     low   close  volume  volume_nominal
            datetime
            2023-11-02 09:05:00  182000  182000  182000  182000       0               0
            2023-11-02 09:06:00  182000  182000  182000  182000       0               0
            2023-11-02 09:07:00  182000  182000  182000  182000       0               0
            2023-11-02 09:08:00  182000  182000  182000  182000       0               0
            2023-11-02 09:09:00  182000  182000  182000  182000       0               0
            ...                     ...     ...     ...     ...     ...             ...
            2023-11-03 15:15:00  182000  182000  182000  182000       0               0
            2023-11-03 15:16:00  182000  182000  182000  182000       0               0
            2023-11-03 15:17:00  182000  182000  182000  182000       0               0
            2023-11-03 15:18:00  183000  183000  183000  183000       0               0
            2023-11-03 15:19:00  184000  184000  184000  184000       0               0

            [750 rows x 6 columns]
        """
        if isinstance(values, list):
            if len(values) == 0:
                raise ValueError('values should not be empty')

            dataset = []

            for value in values:
                if type(value) == int:
                    if value < 0:
                        raise ValueError('value should not be negative')

                    dataset.append({
                        'open': value,
                        'high': value,
                        'low': value,
                        'close': value,
                        'volume': 0,
                        'volume_nominal': 0,
                    })

                elif isinstance(value, dict):
                    allowed_keys = ['open', 'high', 'low', 'close', 'volume', 'volume_nominal']
                    for key in value.keys():
                        if key not in allowed_keys:
                            raise ValueError('value should be one of {}'.format(allowed_keys))

                    dataset.append({
                        'open': value.get('open', 0),
                        'high': value.get('high', 0),
                        'low': value.get('low', 0),
                        'close': value.get('close', 0),
                        'volume': value.get('volume', 0),
                        'volume_nominal': value.get('volume_nominal', 0),
                    })

                else:
                    raise ValueError('value should be int or dict')

            self.historical_minute_datas[asset_code] = dataset
        else:
            raise ValueError('values should be list')


    def is_open_market_time(self, dt: datetime) -> bool:
        is_open_day = self.is_open_market_day(dt)
        is_closed_period = (dt.hour < 9 ) or (dt.hour == 9 and dt.minute < 5) or (dt.hour > 15) or (dt.hour == 15 and dt.minute >= 20)

        return is_open_day and not is_closed_period


    def is_open_market_day(self, d: datetime.date) -> bool:
        return d.weekday() not in [5, 6]


    def get_historical_minute_data(self, asset_code: str, interval: int = 1, first_date: datetime.date = None, last_date: datetime.date = None) -> pd.DataFrame:
        result_list = []

        if not first_date:
            first_date = datetime.now().date()
        if not last_date:
            last_date = datetime.now().date()

        if first_date and last_date:
            if first_date > last_date:
                raise ValueError('조회 시작일자는 조회 마지막일자 이후일 수 없습니다.')

        current_time = datetime.combine(first_date, datetime.min.time())
        last_time = datetime.combine(last_date, datetime.max.time())

        custom_dataset = []
        if asset_code in self.historical_minute_datas:
            custom_dataset = self.historical_minute_datas[asset_code]

        while current_time <= last_time:
            current_time = current_time + timedelta(minutes=interval)

            if not self.is_open_market_time(current_time):
                continue

            result_list.append({
                'datetime': current_time,
                'open': 0,
                'high': 0,
                'low': 0,
                'close': 0,
                'volume': 0,
                'volume_nominal': 0,
            })

        if len(custom_dataset) > 0:
            if len(custom_dataset) > len(result_list):
                custom_dataset = custom_dataset[-len(result_list):]

            for i in range(len(result_list)):
                result_list[i].update(custom_dataset[0])

            for i in range(len(custom_dataset)):
                idx = len(result_list) - len(custom_dataset) + i
                result_list[idx].update(custom_dataset[i])

        df = pd.DataFrame(result_list)
        df.set_index('datetime', inplace=True)
        return df


    def set_historical_daily_data(self, asset_code: str, values: List[Dict|int]):
        """
        Mock 일봉 데이터 설정

        :param asset_code: 종목코드
        :type asset_code: str
        :param values: 설정 할 일봉 데이터
        :type values: List[Dict|int]

        :examples:

        .. code-block:: python

            >>> from qupyter.test import MockStockBroker
            from datetime import date
            >>> from datetime import date
            >>> mock_broker = MockStockBroker()

            # 최근 4일치 데이터 설정
            >>> mock_broker.set_historical_daily_data('005930', [
            ...     {'open': 70000, 'high': 70000, 'low': 70000, 'close': 70000, 'volume': 0, 'volume_nominal': 0},
            ...     {'open': 70000, 'high': 71000, 'low': 70000, 'close': 71000, 'volume': 0, 'volume_nominal': 0},
            ...     {'open': 71000, 'high': 72000, 'low': 70000, 'close': 72000, 'volume': 0, 'volume_nominal': 0},
            ...     {'open': 72000, 'high': 72000, 'low': 70000, 'close': 70000, 'volume': 0, 'volume_nominal': 0},
            ... ])

            >>> mock_broker.get_historical_daily_data('005930', first_date=date(2023, 10, 25))
                        open   high    low  close  volume  volume_nominal
            date
            2023-10-26  70000  70000  70000  70000       0               0
            2023-10-27  70000  70000  70000  70000       0               0
            2023-10-30  70000  70000  70000  70000       0               0
            2023-10-31  70000  70000  70000  70000       0               0
            2023-11-01  70000  71000  70000  71000       0               0
            2023-11-02  71000  72000  70000  72000       0               0
            2023-11-03  72000  72000  70000  70000       0               0

            # 최근 3일치 데이터 설정 (open, high, low, close 모두 하나의 값으로 설정)
            >>> mock_broker.set_historical_daily_data('005380', [182000, 184000, 186000])

            >>> mock_broker.get_historical_daily_data('005380', first_date=date(2023, 10, 25))
                        open    high     low   close  volume  volume_nominal
            date
            2023-10-26  182000  182000  182000  182000       0               0
            2023-10-27  182000  182000  182000  182000       0               0
            2023-10-30  182000  182000  182000  182000       0               0
            2023-10-31  182000  182000  182000  182000       0               0
            2023-11-01  182000  182000  182000  182000       0               0
            2023-11-02  184000  184000  184000  184000       0               0
            2023-11-03  186000  186000  186000  186000       0               0
        """
        if isinstance(values, list):
            if len(values) == 0:
                raise ValueError('values should not be empty')

            dataset = []

            for value in values:
                if type(value) == int:
                    if value < 0:
                        raise ValueError('value should not be negative')

                    dataset.append({
                        'open': value,
                        'high': value,
                        'low': value,
                        'close': value,
                        'volume': 0,
                        'volume_nominal': 0,
                    })

                elif isinstance(value, dict):
                    allowed_keys = ['open', 'high', 'low', 'close', 'volume', 'volume_nominal']
                    for key in value.keys():
                        if key not in allowed_keys:
                            raise ValueError('value should be one of {}'.format(allowed_keys))

                    dataset.append({
                        'open': value.get('open', 0),
                        'high': value.get('high', 0),
                        'low': value.get('low', 0),
                        'close': value.get('close', 0),
                        'volume': value.get('volume', 0),
                        'volume_nominal': value.get('volume_nominal', 0),
                    })

                else:
                    raise ValueError('value should be int or dict')

            self.historical_daily_datas[asset_code] = dataset
        else:
            raise ValueError('values should be list')


    def get_historical_daily_data(self, asset_code: str, adjusted_price: bool = False, first_date: datetime.date = None, last_date: datetime.date = None) -> pd.DataFrame:
        result_list = []

        if not first_date:
            first_date = datetime.now().date()
        if not last_date:
            last_date = datetime.now().date()

        current_date = first_date
        last_date = last_date

        custom_dataset = []
        if asset_code in self.historical_daily_datas:
            custom_dataset = self.historical_daily_datas[asset_code]

        while current_date <= last_date:
            current_date += timedelta(days=1)
            if not self.is_open_market_day(current_date):
                continue

            result_list.append({
                'date': current_date,
                'open': 0,
                'high': 0,
                'low': 0,
                'close': 0,
                'volume': 0,
                'volume_nominal': 0,
            })

        if len(custom_dataset) > 0:
            if len(custom_dataset) > len(result_list):
                custom_dataset = custom_dataset[-len(result_list):]

            for i in range(len(result_list)):
                result_list[i].update(custom_dataset[0])

            for i in range(len(custom_dataset)):
                idx = len(result_list) - len(custom_dataset) + i
                result_list[idx].update(custom_dataset[i])

        df = pd.DataFrame(result_list)
        df.set_index('date', inplace=True)
        return df

    def set_account(self, **kwargs):
        """
        Mock 계좌 정보 설정

        :param kwargs: 설정 할 계좌 정보
        :type kwargs: Dict

        :examples:

        .. code-block:: python

            >>> broker.set_account(investable_cash=1000000)
            >>> broker.get_account()
            {'investable_cash': 1000000, 'asset_value': 0, 'receivable_amount': 0, 'total_balance': 0, 'pnl_pct': 0, 'investment_principal': 0, 'investment_pnl_amount': 0, 'credit_order_amount': 0, 'credit_orderable_amount': 0, 'deposit': 0, 'substitute_amount': 0, 'deposit_d1': 0, 'deposit_d2': 0, 'cash_receivables': 0, 'cash_collateral': 0, 'substitute_collateral': 0, 'cheque_amount': 0, 'substitute_orderable_amount': 0, 'margin_rate_35_pct_orderable_amount': 0, 'margin_rate_50_pct_orderable_amount': 0, 'margin_rate_100_pct_orderable_amount': 0, 'd1_overdraft_fee': 0, 'd2_overdraft_fee': 0, 'deposit_pledge_loan_amount': 0, 'credit_setting_collateral': 0, 'margin_loan_amount': 0, 'original_pledge_amount': 0, 'subordinate_pledge_amount': 0, 'required_pledge_amount': 0, 'original_pledge_shortage': 0, 'subordinate_pledge_shortage': 0, 'additional_collateral_cash': 0, 'unpaid_interest': 0, 'other_loan_amount': 0, 'd1_margin_call_amount': 0, 'original_pledge_total_amount': 0, 'subordinate_pledge_total_amount': 0, 'credit_collateral_cash': 0, 'credit_collateral_substitute': 0, 'additional_credit_collateral_cash': 0, 'reused_credit_collateral_amount': 0, 'additional_credit_collateral_substitute': 0, 'sellout_collateral_loan_amount': 0, 'disposal_limit_amount': 0}

        """
        self.account_info = kwargs

    def get_account(self) -> Dict:
        res = {
            'investable_cash': 0,  # 현금주문가능금액
            'asset_value': 0,  # 잔고평가금액
            'receivable_amount': 0,  # 미수금액
            'total_balance': 0,  # 예탁자산총액
            'pnl_pct': 0,  # 손익율
            'investment_principal': 0,  # 투자원금
            'investment_pnl_amount': 0,  # 투자손익금액
            'credit_order_amount': 0,  # 신용담보주문금액
            'credit_orderable_amount': 0,  # 신용주문가능금액
            'deposit': 0,  # 예수금
            'substitute_amount': 0,  # 대용금액
            'deposit_d1': 0,  # D+1 예수금
            'deposit_d2': 0,  # D+2 예수금
            'cash_receivables': 0,  # 현금미수금액
            'cash_collateral': 0,  # 증거금현금
            'substitute_collateral': 0,  # 증거금대용
            'cheque_amount': 0,  # 수표금액
            'substitute_orderable_amount': 0,  # 대용주문가능금액
            'margin_rate_35_pct_orderable_amount': 0,  # 증거금률 35% 주문 가능금액
            'margin_rate_50_pct_orderable_amount': 0,  # 증거금률 50% 주문 가능금액
            'margin_rate_100_pct_orderable_amount': 0,  # 증거금률 100% 주문가능금액
            'd1_overdraft_fee': 0,  # D+1 연체변제소요금액
            'd2_overdraft_fee': 0,  # D+2 연체변제소요금액
            'deposit_pledge_loan_amount': 0,  # 예탁담보대출금액
            'credit_setting_collateral': 0,  # 신용설정보증금
            'margin_loan_amount': 0,  # 융자금액
            'original_pledge_amount': 0,  # 원담보금액
            'subordinate_pledge_amount': 0,  # 부담보금액
            'required_pledge_amount': 0,  # 소요담보금액
            'original_pledge_shortage': 0,  # 원담보부족금액
            'subordinate_pledge_shortage': 0,  # 담보부족금액
            'additional_collateral_cash': 0,  # 추가담보현금
            'unpaid_interest': 0,  # 신용이자미납금액
            'other_loan_amount': 0,  # 기타대여금액
            'd1_margin_call_amount': 0,  # 익일추정반대매매금액
            'original_pledge_total_amount': 0,  # 원담보합계금액
            'subordinate_pledge_total_amount': 0,  # 부담보합계금액
            'credit_collateral_cash': 0,  # 신용담보금현금
            'credit_collateral_substitute': 0,  # 신용담보대용금액
            'additional_credit_collateral_cash': 0,  # 추가신용담보현금
            'reused_credit_collateral_amount': 0,  # 신용담보재사용금액
            'additional_credit_collateral_substitute': 0,  # 추가신용담보대용
            'sellout_collateral_loan_amount': 0,  # 매도대금담보대출금액
            'disposal_limit_amount': 0,  # 처분제한금액
        }

        res.update(self.account_info)
        return res


def validate_trade_func_result(result: List[Tuple[str, int, int]]):
    """ trade_func 의 리턴값 검증

    :param result: trade_func 의 리턴값
    :type result: List[Tuple[str, int, int]]

    """
    if result == None:
        return
    if not isinstance(result, list):
        raise ValueError('orderlist should be list')

    for item in result:
        if not isinstance(item, tuple):
            raise ValueError('orderlist item should be tuple')
        if len(item) != 3:
            raise ValueError('orderlist item should have 3 elements')

        code = item[0]
        price = item[1]
        quantity = item[2]

        if not isinstance(code, str):
            raise ValueError('code should be str')

        if not isinstance(price, int):
            raise ValueError('price should be int')

        if price < 0:
            raise ValueError('price should not be negative')

        if not isinstance(quantity, int):
            raise ValueError('quantity should be int')

        if quantity <= 0:
            raise ValueError('quantity should be positive')


def validate_handle_pending_orders_result(result: List[Tuple[str, int, int|None, int]]):
    """
    handle_pending_orders 의 리턴값 검증

    :param result: handle_pending_orders 의 리턴값
    :type result: List[Tuple[str, int, int|None, int]]

    """
    if result == None:
        return
    if not isinstance(result, list):
        raise ValueError('result should be list')
    if len(result) == 0:
        return

    for item in result:
        if not isinstance(item, tuple):
            raise ValueError('result item should be tuple')
        if len(item) != 4:
            raise ValueError('result item should have 4 elements')

        code = item[0]
        order_id = item[1]
        price = item[2]
        quantity = item[3]

        if not isinstance(code, str):
            raise ValueError('code should be str')

        if not isinstance(order_id, int):
            raise ValueError('order_id should be int')

        if price != None and not isinstance(price, int):
            raise ValueError('price should be int or None')

        if not isinstance(quantity, int):
            raise ValueError('quantity should be int')

        if quantity > 0 and price == None:
            raise ValueError('price should be specified when quantity > 0')


