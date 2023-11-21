from dataclasses import dataclass
from decimal import Decimal
import datetime
from typing import List, Dict, Optional


@dataclass
class StockOrder:
    """미체결 주문에 대한 class.

    :param order_id: 주문번호
    :type order_id: int
    :param asset_code: 종목코드
    :type asset_code: str
    :param trade_type: 매매구분 (1: 매도, 2: 매수)
    :type trade_type: int
    :param quantity: 주문수량
    :type quantity: int
    :param price: 주문가격
    :type price: int
    :param filled_quantity: 체결수량
    :type filled_quantity: int
    :param filled_price: 체결가격
    :type filled_price: int
    :param pending_quantity: 미체결잔량
    :type pending_quantity: int
    :param order_time: 주문시간
    :type order_time: datetime.datetime
    :param order_method: 주문매체
    :type order_method: str
    :param current_price: 현재가
    :type current_price: int
    """
    order_id: int
    asset_code: str
    trade_type: int
    quantity: int
    price: int
    filled_quantity: int
    filled_price: int
    pending_quantity: int
    order_time: datetime.datetime
    order_method: str
    current_price: int


@dataclass
class StockPosition:
    '''보유 포지션에 대한 클래스

    :param asset_code: 종목코드
    :type asset_code: str
    :param asset_name: 종목명
    :type asset_name: str
    :param quantity: 잔고수량
    :type quantity: int
    :param exit_available_quantity: 매도가능수량
    :type exit_available_quantity: int
    :param average_purchase_price: 평균단가
    :type average_purchase_price: int
    :param purchase_value: 매입금액
    :type purchase_value: int
    :param loan_value: 대출금액
    :type loan_value: int
    :param loan_date: 대출일자
    :type loan_date: Optional[datetime.date]
    :param expiration_date: 만기일자
    :type expiration_date: Optional[datetime.date]
    :param current_price: 현재가
    :type current_price: int
    :param current_value: 평가금액
    :type current_value: int
    :param current_pnl: 평가손익
    :type current_pnl: int
    :param current_pnl_pct: 수익율
    :type current_pnl_pct: Decimal
    :param commission: 수수료
    :type commission: int
    :param tax: 세금
    :type tax: int
    :param loan_interest: 신용이자
    :type loan_interest: int
    '''
    asset_code: str
    asset_name: str
    quantity: int
    exit_available_quantity: int
    average_purchase_price: int
    purchase_value: int
    loan_value: int
    loan_date: Optional[datetime.date]
    expiration_date: Optional[datetime.date]
    current_price: int
    current_value: int
    current_pnl: int
    current_pnl_pct: Decimal
    commission: int
    tax: int
    loan_interest: int

