import pandas as pd

from datetime import datetime
from qupyter.brokerage import StockBroker, StockOrder, StockPosition
from qupyter.brokerage.kis.stocks.stocks import KISStocks
from typing import List, Dict, Tuple


class KISStockBroker(StockBroker):
    """
    한국투자증권 StockBroker 구현체
    """

    def __init__(self, test_trade: bool, **kwargs):
        self.api = KISStocks(test_trade, **kwargs)


    def get_price(self, asset_code: str) -> pd.DataFrame:
        data = self.api.get_price(asset_code=asset_code)
        df = pd.DataFrame([data])
        df.set_index('code', inplace=True)
        return df


    def get_price_for_multiple_stocks(self, asset_codes: List[str]) -> pd.DataFrame:
        data = self.api.get_price_for_multiple_stocks(asset_codes=asset_codes)
        df = pd.DataFrame(data)
        df.set_index('code', inplace=True)
        return df


    def get_today_minute_data(self, asset_code) -> pd.DataFrame:
        data = self.api.get_today_minute_data(asset_code=asset_code)
        data.reverse()
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        return df


    def get_historical_daily_data(self, asset_code: str, adjusted_price: bool = False, first_date: datetime.date = None, last_date: datetime.date = None) -> pd.DataFrame:
        if first_date and last_date:
            if first_date > last_date:
                raise ValueError('조회 시작일자는 조회 마지막일자 이후일 수 없습니다.')
            elif first_date == last_date:
                raise ValueError('조회 시작일자와 조회 마지막일자는 같을 수 없습니다.')

        if not first_date and not last_date:
            raise ValueError('당일 조회는 get_price() 메서드를 사용해주세요.')

        data = self.api.get_historical_daily_data(asset_code=asset_code, adjusted_price=adjusted_price, first_date=first_date, last_date=last_date)

        if len(data) == 0:
            raise ValueError('조회 시작일자와 조회 마지막일자는 영업일이여야 합니다.')

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        return df


    def get_account(self) -> Dict:
        data = self.api.get_account()
        return data


    def create_order(self, asset_code: str, price: int, quantity: int, side: int):
        self.api.create_order(
            asset_code=asset_code,
            price=price,
            quantity=quantity,
            side=side,
        )


    def update_order(self, org_order_id: int, asset_code: str, price: int, quantity: int):
        self.api.update_order(
            org_order_no=org_order_id,
            asset_code=asset_code,
            price=price,
            quantity=quantity,
        )


    def cancel_order(self, order_id: int, asset_code: str, quantity: int):
        self.api.cancel_order(
            org_order_no=order_id,
            asset_code=asset_code,
            quantity=quantity,
        )


    def get_positions(self, exclude_empty_positions: bool = True) -> List[StockPosition]:
        stock_positions = self.api.get_positions(exclude_empty_positions)

        return stock_positions


    def get_pending_orders(self) -> List[Tuple[str, List[StockOrder]]]:
        stock_pending_orders = self.api.get_pending_orders()

        return stock_pending_orders
