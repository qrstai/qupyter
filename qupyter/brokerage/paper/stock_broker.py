import pandas as pd
import datetime as dtm
import pykrx
import qupyter.config as c
import requests

from typing import Dict, List, Tuple
from qupyter.brokerage import StockBroker
from qupyter.brokerage.utils.retry import retry


class PaperStockBroker(StockBroker):
    def get_price(self, asset_code: str) -> pd.DataFrame:
        data = self.request_with_retry(method='GET', url=f'{c.QUPYTER_API_URL}/paper-trading/prices', params={ 'codes': asset_code })
        print(data)
        df = pd.DataFrame(data)
        df.set_index('code', inplace=True)
        return df

    def get_price_for_multiple_stocks(self, asset_codes: List[str]) -> pd.DataFrame:
        data = self.request_with_retry(method='GET', url=f'{c.QUPYTER_API_URL}/paper-trading/prices', params={ 'codes': ','.join(asset_codes) })
        df = pd.DataFrame(data)
        df.set_index('code', inplace=True)
        return df

    def get_today_minute_data(self, asset_code: str) -> pd.DataFrame:
        data = self.request_with_retry(method='GET', url=f'{c.QUPYTER_API_URL}/paper-trading/candles/minutes', params={ 'code': asset_code })
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S')
        df.set_index('time', inplace=True)
        return df

    def get_historical_daily_data(self, asset_code: str, adjusted_price: bool = False, first_date: dtm.date = None, last_date: dtm.date = None) -> pd.DataFrame:
        if first_date is None:
            first_date = dtm.date.today()
        if last_date is None:
            last_date = dtm.date.today()

        df = pykrx.stock.get_market_ohlcv(
            first_date.strftime('%Y%m%d'),
            last_date.strftime('%Y%m%d'),
            asset_code,
        )

        df.rename(columns={'시가': 'open', '고가': 'high', '저가': 'low', '종가': 'close', '거래량': 'volume'}, inplace=True)
        df.rename_axis('date', inplace=True)
        df.drop(columns=['등락률'], inplace=True)

        return df

    def get_account(self) -> Dict:
        return {
            'investable_cash': 500000000,
            'asset_value': 0,
            'total_balance': 500000000,
        }

    @retry(requests.HTTPError, delay=0.1)
    def request_with_retry(self, method: str, url: str, headers: dict = None, params: dict = None, body: dict = None, return_headers: bool = False) -> Dict | Tuple[Dict, Dict]:
        r = requests.request(method=method, url=url, headers=headers, params=params, json=body)
        if r.status_code != 200:
            print('Qupyter API response error:', r.text)
            r.raise_for_status()

        body = r.json()
        if return_headers:
            headers = r.headers
            return body, headers
        else:
            return body