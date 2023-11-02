import random

from datetime import datetime
from qupyter.brokerage import StockOrder, StockPosition


def order(**kwargs) -> StockOrder:
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


