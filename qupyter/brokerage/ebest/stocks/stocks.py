import datetime
from decimal import Decimal
import json
import time

from typing import Dict, List, Tuple

from requests import HTTPError
from qupyter.brokerage.ebest.core import EBest
from qupyter.brokerage.models import StockOrder
from qupyter.brokerage.models import StockPosition
from qupyter.brokerage.utils.limit_calls import CallLimiter, limit_calls
from qupyter.brokerage.utils.retry import retry



class EBestStocks(EBest):
    def __init__(self, test_trade: bool, **kwargs):
        super().__init__(test_trade=test_trade, account_type='stock', **kwargs)

    @retry(HTTPError)
    def post_with_retry(self, url: str, headers: Dict, body: Dict, return_headers: bool = False) -> Dict | Tuple[Dict, Dict]:
        r = self.session.post(url, headers=headers, json=body)
        body = r.json()
        if r.status_code != 200:
            print(body)
            if body.get('rsp_cd') == 'IGW00121': # 유효하지 않은 토큰
                self.refresh_token()

            r.raise_for_status()

        if return_headers:
            headers = r.headers
            return body, headers
        else:
            return body


    # ----------------------------------------------------------------------------------------------------
    # 시세 관련
    # ----------------------------------------------------------------------------------------------------
    @limit_calls(max_calls=3, scope='t1101')
    def _get_quote_info(self, asset_code: str):
        url = f'{self.host_url}/stock/market-data'
        tr_cd = 't1101'

        headers = {
            'tr_cd': tr_cd,
            'tr_cont': 'N',
        }

        body = {
            f'{tr_cd}InBlock': {
                'shcode': asset_code,  # 단축코드
            }
        }

        data = self.post_with_retry(url, headers, body)
        out_block = data.get(f'{tr_cd}OutBlock')

        res = {
            'ask_price_1': out_block.get('offerho1'),  # 1차 매도호가
            'bid_price_1': out_block.get('bidho1'),  # 1차 매수호가
            'ask_volume_1': out_block.get('offerrem1'),  # 1차 매도호가수량
            'bid_volume_1': out_block.get('bidrem1'),  # 1차 매수호가수량
            'ask_price_2': out_block.get('offerho2'),  # 2차 매도호가
            'bid_price_2': out_block.get('bidho2'),  # 2차 매수호가
            'ask_volume_2': out_block.get('offerrem2'),  # 2차 매도호가수량
            'bid_volume_2': out_block.get('bidrem2'),  # 2차 매수호가수량
            'ask_price_3': out_block.get('offerho3'),  # 3차 매도호가
            'bid_price_3': out_block.get('bidho3'),  # 3차 매수호가
            'ask_volume_3': out_block.get('offerrem3'),  # 3차 매도호가수량
            'bid_volume_3': out_block.get('bidrem3'),  # 3차 매수호가수량
            'ask_price_4': out_block.get('offerho4'),  # 4차 매도호가
            'bid_price_4': out_block.get('bidho4'),  # 4차 매수호가
            'ask_volume_4': out_block.get('offerrem4'),  # 4차 매도호가수량
            'bid_volume_4': out_block.get('bidrem4'),  # 4차 매수호가수량
            'ask_price_5': out_block.get('offerho5'),  # 5차 매도호가
            'bid_price_5': out_block.get('bidho5'),  # 5차 매수호가
            'ask_volume_5': out_block.get('offerrem5'),  # 5차 매도호가수량
            'bid_volume_5': out_block.get('bidrem5'),  # 5차 매수호가수량
            'ask_volume_total': out_block.get('offer'),  # 총 매도호가수량
            'bid_volume_total': out_block.get('bid'),  # 총 매수호가수량
        }

        return res


    @limit_calls(max_calls=2, scope='t1102')
    def _get_price_info(self, asset_code: str):
        url = f'{self.host_url}/stock/market-data'
        tr_cd = 't1102'

        headers = {
            'tr_cd': tr_cd,
            'tr_cont': 'N',
        }

        body = {
            f'{tr_cd}InBlock': {
                'shcode': asset_code,  # 단축코드
            }
        }

        data = self.post_with_retry(url, headers, body)
        out_block = data.get(f'{tr_cd}OutBlock')

        res = {
            'code': asset_code,  # 종목코드
            'name': out_block.get('hname'),  # 한글명
            'current_price': int(out_block.get('price', 0)),  # 현재가
            'volume': out_block.get('volume'),  # 누적거래량
            'volume_nominal': out_block.get('value') * 1_000_000,  # 누적거래대금 (단위: 백만원)
            'open_price': out_block.get('open'),  # 시가
            'high_price': out_block.get('high'),  # 고가
            'low_price': out_block.get('low'),  # 저가
            'max_price': out_block.get('uplmtprice'),  # 상한가
            'min_price': out_block.get('dnlmtprice'),  # 하한가
            'market_capitalization': out_block.get('total') * 1_000_000,  # 시가총액 (단위: 백만원)
        }

        return res


    def get_price(self, asset_code: str):
        """ 단일 종목 시세 조회 """
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        price_info = self._get_price_info(asset_code=asset_code)
        quote_info = self._get_quote_info(asset_code=asset_code)

        price_info.update(quote_info)

        return price_info


    def get_price_for_multiple_stocks(self, asset_codes: List[str] = []):
        """ 복수 종목 시세 조회 """
        url = f'{self.host_url}/stock/market-data'
        tr_cd = 't8407'

        headers = {
            'tr_cd': tr_cd,
            'tr_cont': 'N',
        }

        batch_size = 50
        batches = [asset_codes[i:i+batch_size] for i in range(0, len(asset_codes), batch_size)]

        res = []

        for batch in batches:
            CallLimiter().wait_limit_rate(max_calls=2, scope='t8407')
            asset_codes_seq = ''
            for asset_code in batch:
                if len(asset_code) > 6:
                    asset_code = asset_code[1:]
                asset_codes_seq += asset_code

            body = {
                f'{tr_cd}InBlock': {
                    'nrec': len(batch),  # 건수 (최대 50개까지)
                    'shcode': asset_codes_seq,  # 단축코드
                }
            }

            data = self.post_with_retry(url, headers, body)
            out_block_1 = data.get(f'{tr_cd}OutBlock1')

            for item in out_block_1:
                _item = {
                    'code': item.get('shcode'),  # 종목코드
                    'name': item.get('hname'),  # 종목명
                    'current_price': item.get('price'),  # 현재가
                    'volume': item.get('volume'),  # 누적거래량
                    'volume_nominal': item.get('value') * 1_000_000,  # 누적거래대금 (단위: 백만원)
                    'open_price': item.get('open'),  # 시가
                    'high_price': item.get('high'),  # 고가
                    'low_price': item.get('low'),  # 저가
                    'max_price': item.get('uplmtprice'),  # 상한가
                    'min_price': item.get('dnlmtprice'),  # 하한가
                    'ask_price_1': item.get('offerho'),  # 매도호가
                    'bid_price_1': item.get('bidho'),  # 매수호가
                    'ask_volume_total': item.get('totofferrem'),  # 총매도잔량
                    'bid_volume_total': item.get('totbidrem'),  # 총매수잔량
                }
                res.append(_item)

        return res


    def get_today_minute_data(self, asset_code: str):
        return self.get_historical_minute_data(asset_code, first_date=datetime.date.today())


    def get_historical_minute_data(self, asset_code: str, interval: int = 1, first_date: datetime.date = None, last_date: datetime.date = None):
        """과거 분봉 데이터 조회

        :param asset_code: 종목코드
        :type asset_code: str

        :param interval: 단위(n분)
        :type interval: int

        :param first_date: 조회 시작일자 (None일 경우 당일 조회)
        :type first_date: datetime.date

        :param date last_date: 조회 종료일자 (None인 경우 당일 조회)
        :type last_date: datetime.date

        :return: 분봉 데이터
        :rtype: pandas.DataFrame

        DataFrame에는 다음 필드들이 포함됩니다.

        - datetime (str): 일자 및 시간
        - open (int): 시가
        - high (int): 고가
        - low (int): 저가
        - close (int): 종가
        - volume (int): 거래량
        - volume_nominal (int): 거래대금 (단위: 백만원).

        :examples:

        .. code-block:: python

            >>> df = broker.get_historical_minute_data(asset_code='005930', interval=1, first_date=datetime.date(2023, 10, 25), last_date=datetime.date(2023, 10, 26))
            >>> print(df)

                                  open   high    low  close  volume  volume_nominal
            datetime
            2023-10-25 09:01:00  68800  68800  68500  68700  513985     35345000000
            2023-10-25 09:02:00  68600  68700  68600  68700   46971      3226000000
            2023-10-25 09:03:00  68600  68800  68600  68700   68890      4733000000
            2023-10-25 09:04:00  68700  68700  68500  68600  121569      8343000000
            2023-10-25 09:05:00  68500  68700  68500  68600   57472      3942000000
        """
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        if not first_date:
            first_date = datetime.datetime.now().date()

        if not last_date:
            last_date = datetime.datetime.now().date()

        first_date_str = first_date.strftime('%Y%m%d')
        last_date_str = last_date.strftime('%Y%m%d')

        url = f'{self.host_url}/stock/chart'
        tr_cd = 't8412'

        cts_date = ' '
        cts_time = ' '
        tr_cont = 'N'
        tr_cont_key = None

        res = []

        while True:
            CallLimiter().wait_limit_rate(max_calls=2, scope='t8412')

            headers = {
                'tr_cd': tr_cd,
                'tr_cont': tr_cont,
            }

            if tr_cont_key:
                headers['tr_cont_key'] = tr_cont_key

            body = {
                f'{tr_cd}InBlock': {
                    'shcode': asset_code,
                    'ncnt': interval,
                    'sdate': first_date_str,
                    'edate': last_date_str,
                    'cts_date': cts_date,
                    'cts_time': cts_time,
                    'comp_yn': 'N',
                }
            }

            data, r_headers = self.post_with_retry(url, headers, body, return_headers=True)

            tr_cont = r_headers.get('tr_cont')
            tr_cont_key = r_headers.get('tr_cont_key')

            out_block = data.get(f'{tr_cd}OutBlock')
            cts_date = out_block.get('cts_date', '').strip()
            cts_time = out_block.get('cts_time', '').strip()

            out_block_1 = data.get(f'{tr_cd}OutBlock1', [])
            out_block_1.reverse()

            for item in out_block_1:
                _date = item.get('date')
                _time = item.get('time')
                dt_str = f'{_date[:4]}-{_date[4:6]}-{_date[6:]} {_time[:2]}:{_time[2:4]}:{_time[4:]}'

                _item = {
                    'datetime': dt_str,  # 날짜 & 시간
                    'open': item.get('open'),  # 시가
                    'high': item.get('high'),  # 고가
                    'low': item.get('low'),  # 저가
                    'close': item.get('close'),  # 종가
                    'volume': item.get('jdiff_vol'),  # 거래량
                    'volume_nominal': item.get('value') * 1_000_000,  # 거래대금 (단위: 백만원)
                }
                res.append(_item)

            if tr_cont == 'N' or (cts_date == '' and cts_time == ''):
                break

        return res


    def get_historical_daily_data(self, asset_code: str, adjusted_price: bool = False, first_date: datetime.date = None, last_date: datetime.date = None):
        """과거 일봉 데이터 조회
        :param str asset_code: 종목코드
        :param bool adjusted_price: 수정주가여부
        :param date first_date: 조회 시작일자 (`None`일 경우 당일 조회)
        :param date last_date: 조회 종료일자 (`None`인 경우 당일 조회)
        """
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        if not first_date:
            first_date = datetime.datetime.now().date()

        if not last_date:
            last_date = datetime.datetime.now().date()

        first_date_str = first_date.strftime('%Y%m%d')
        last_date_str = last_date.strftime('%Y%m%d')

        url = f'{self.host_url}/stock/chart'
        tr_cd = 't8410'

        cts_date = ' '
        cts_time = ' '
        tr_cont = 'N'
        tr_cont_key = None

        res = []

        while True:
            CallLimiter().wait_limit_rate(max_calls=1, scope='t8410')

            headers = {
                'tr_cd': tr_cd,
                'tr_cont': tr_cont,
            }

            if tr_cont_key:
                headers['tr_cont_key'] = tr_cont_key

            body = {
                f'{tr_cd}InBlock': {
                    'shcode': asset_code,
                    'gubun': '2',
                    'sujung': 'Y' if adjusted_price else 'N',
                    'sdate': first_date_str,
                    'edate': last_date_str,
                    'cts_date': cts_date,
                    'cts_time': cts_time,
                    'comp_yn': 'N',
                }
            }

            data, r_headers = self.post_with_retry(url, headers, body, return_headers=True)

            tr_cont = r_headers.get('tr_cont')
            tr_cont_key = r_headers.get('tr_cont_key')

            out_block = data.get(f'{tr_cd}OutBlock')
            cts_date = out_block.get('cts_date', '').strip()
            cts_time = out_block.get('cts_time', '').strip()

            out_block_1 = data.get(f'{tr_cd}OutBlock1', [])
            out_block_1.reverse()

            for item in out_block_1:
                _date = item.get('date')
                dt_str = f'{_date[:4]}-{_date[4:6]}-{_date[6:]}'

                _item = {
                    'date': dt_str,  # 날짜
                    'open': item.get('open'),  # 시가
                    'high': item.get('high'),  # 고가
                    'low': item.get('low'),  # 저가
                    'close': item.get('close'),  # 종가
                    'volume': item.get('jdiff_vol'),  # 거래량
                    'volume_nominal': item.get('value') * 1_000_000,  # 거래대금 (단위: 백만원)
                }
                res.append(_item)

            if tr_cont == 'N' or (cts_date == '' and cts_time == ''):
                break

        return res


    # ----------------------------------------------------------------------------------------------------
    # 계좌 관련
    # ----------------------------------------------------------------------------------------------------
    @limit_calls(max_calls=1, scope='CSPAQ12200')
    def get_account(self):
        """ 계좌 정보 조회 """
        url = f'{self.host_url}/stock/accno'
        tr_cd = 'CSPAQ12200'

        headers = {
            'tr_cd': tr_cd,
            'tr_cont': 'N',
        }

        body = {
            f'{tr_cd}InBlock1': {
                'BalCreTp': '0',  # 잔고생성구분
            }
        }

        data = self.post_with_retry(url, headers, body)

        out_block_2 = data.get(f'{tr_cd}OutBlock2')
        if out_block_2 is None:
            print(f"{tr_cd} response:", data)
            raise Exception(f"Fail to get account info")

        res = {
            'investable_cash': out_block_2.get('MnyOrdAbleAmt'),  # 현금주문가능금액
            'asset_value': out_block_2.get('BalEvalAmt'),  # 잔고평가금액
            'total_balance': out_block_2.get('DpsastTotamt'),  # 예탁자산총액
            'broker_data': out_block_2,
        }

        return res


    def _create_stock_position_from_json(self, json_dict: Dict) -> StockPosition:
        asset_code = json_dict.get('expcode')  # 종목번호
        asset_name = json_dict.get('hname')  # 종목명
        quantity = int(json_dict.get('janqty'))  # 잔고수량
        exit_available_quantity = int(json_dict.get('mdposqt'))  # 매도가능수량
        average_purchase_price = int(json_dict.get('pamt'))  # 평균단가
        purchase_value = int(json_dict.get('mamt'))  # 매입금액
        loan_value = int(json_dict.get('sinamt'))  # 대출금액
        loan_date = json_dict.get('loandt')  # 대출일자
        expiration_date = json_dict.get('lastdt')  # 만기일자
        current_price = int(json_dict.get('price'))  # 현재가
        current_value = int(json_dict.get('appamt'))  # 평가금액
        current_pnl = int(json_dict.get('dtsunik'))  # 평가손익
        current_pnl_pct = Decimal(json_dict.get('sunikrt'))  # 수익율
        commission = int(json_dict.get('fee'))  # 수수료
        tax = int(json_dict.get('tax'))  # 세금
        loan_interest = int(json_dict.get('sininter'))  # 신용이자

        loan_date = datetime.datetime.strptime(loan_date, '%Y%m%d').date() if loan_date != '' else None
        expiration_date = datetime.datetime.strptime(expiration_date, '%Y%m%d').date() if expiration_date != '' else None

        return StockPosition(
            asset_code=asset_code,
            asset_name=asset_name,
            quantity=quantity,
            exit_available_quantity=exit_available_quantity,
            average_purchase_price=average_purchase_price,
            purchase_value=purchase_value,
            loan_value=loan_value,
            loan_date=loan_date,
            expiration_date=expiration_date,
            current_price=current_price,
            current_value=current_value,
            current_pnl=current_pnl,
            current_pnl_pct=current_pnl_pct,
            commission=commission,
            tax=tax,
            loan_interest=loan_interest,
        )


    @limit_calls(max_calls=2, scope='CSPAQ12300')
    def get_positions(self, exclude_empty_positions: bool):
        """ 보유 포지션 목록 조회 """

        url = f'{self.host_url}/stock/accno'
        tr_cd = 't0424'

        cts_expcode = ' '
        positions: List[StockPosition] = []

        while True:
            if cts_expcode.strip() == '':
                headers = {
                    'tr_cd': tr_cd,
                    'tr_cont': 'N',
                }
            else:
                headers = {
                    'tr_cd': tr_cd,
                    'tr_cont': 'Y',
                    'tr_cont_key': cts_expcode,
                }

            body = {
                f'{tr_cd}InBlock': {
                    'prcgb': '1',  # 1: 평균단가, 2: BEP단가
                    'chegb': '0',  # 0: 결제기준잔고, 2: 체결기준(잔고가 0이 아닌 종목만 조회)
                    'dangb': '0',  # 0: 정규장, 1: 시장외단일가
                    'charge': '1',  # 0: 제비용미포함, 1: 제비용포함
                    'cts_expcode': cts_expcode,  # 처음 조회시에는 Space, 연속 조회시에 이전 조회한 OutBlock의 cts_expcode 값으로 설정
                }
            }

            data = self.post_with_retry(url, headers, body)

            if f'{tr_cd}OutBlock' in data:
                out_block = data.get(f'{tr_cd}OutBlock')
                cts_expcode = out_block.get('cts_expcode', '')

                out_block_1 = data.get(f'{tr_cd}OutBlock1', [])
                for item in out_block_1:
                    position = self._create_stock_position_from_json(item)

                    if exclude_empty_positions and position.quantity == 0:
                        continue

                    if item.get('jonggb') == '9' or item.get('expcode').startswith('CMA'):
                        continue

                    positions.append(position)

                if cts_expcode.strip() == '':
                    break

            else:
                break

        return positions

    def _create_stock_order_from_json(self, json_dict: Dict) -> StockOrder:
        order_id = int(json_dict.get('ordno'))  # 주문번호
        asset_code = json_dict.get('expcode')  # 종목번호
        trade_type = json_dict.get('medosu')  # 구분
        quantity = int(json_dict.get('qty'))  # 주문수량
        price = int(json_dict.get('price'))  # 주문가격
        filled_quantity = int(json_dict.get('cheqty'))  # 체결수량
        filled_price = int(json_dict.get('cheprice'))  # 체결가격
        pending_quantity = int(json_dict.get('ordrem'))  # 미체결잔량
        order_time = json_dict.get('ordtime')  # 주문시간
        order_method = json_dict.get('ordermtd')  # 주문매체
        current_price = int(json_dict.get('price1'))  # 현재가

        if '매수' in trade_type:
            trade_type = 2
        elif '매도' in trade_type:
            trade_type = 1
        else:
            # NOTE 발생되지 않아야하는 케이스 (type hint를 int에 맞추기 위하여 추가됨)
            trade_type = 0

        today_str = datetime.datetime.now().strftime('%Y%m%d')
        order_time = datetime.datetime.strptime(f'{today_str} {order_time[:6]}', '%Y%m%d %H%M%S')

        return StockOrder(
            order_id=order_id,
            asset_code=asset_code,
            trade_type=trade_type,
            quantity=quantity,
            price=price,
            filled_quantity=filled_quantity,
            filled_price=filled_price,
            pending_quantity=pending_quantity,
            order_time=order_time,
            order_method=order_method,
            current_price=current_price,
        )


    @limit_calls(max_calls=1, scope='CSPAQ13700')
    def get_pending_orders(self):
        """ 미체결 주문 내역 조회 """

        url = f'{self.host_url}/stock/accno'
        tr_cd = 't0425'

        cts_ordno = ' '
        # pending_orders: List[StockOrder] = []
        pending_orders_dict = {}

        while True:
            if cts_ordno.strip() == '':
                headers = {
                    'tr_cd': tr_cd,
                    'tr_cont': 'N',
                }
            else:
                headers = {
                    'tr_cd': tr_cd,
                    'tr_cont': 'Y',
                    'tr_cont_key': cts_ordno,
                }

            body = {
                f'{tr_cd}InBlock': {
                    'expcode': '',  # 종목번호; 전체 조회인 경우 빈 값 (i.e. "")
                    'chegb': '2',  # 체결구분; 0: 전체, 1: 체결, 2: 미체결
                    'medosu': '0',  # 매매구분; 0: 전체, 1: 매도, 2: 매수
                    'sortgb': '2',  # 1: 주문번호 역순, 2: 주문번호 순
                    'cts_ordno': cts_ordno,  # 처음 조회시에는 Space, 연속 조회시에 이전 조회한 OutBlock의 cts_ordno 값으로 설정
                }
            }

            data = self.post_with_retry(url, headers, body)

            if f'{tr_cd}OutBlock' in data:
                out_block = data.get(f'{tr_cd}OutBlock')
                cts_ordno = out_block.get('cts_ordno', '')

                out_block_1 = data.get(f'{tr_cd}OutBlock1', [])
                for item in out_block_1:
                    order = self._create_stock_order_from_json(item)
                    # pending_orders.append(order)

                    if order.asset_code in pending_orders_dict:
                        pending_orders_dict[order.asset_code].append(order)
                    else:
                        pending_orders_dict[order.asset_code] = [order]

                if cts_ordno.strip() == '':
                    break

            else:
                break

        pending_orders = []
        for k, v in pending_orders_dict.items():
            pending_orders.append((k, v))

        return pending_orders



    # ----------------------------------------------------------------------------------------------------
    # 주문 관련
    # ----------------------------------------------------------------------------------------------------
    @limit_calls(max_calls=10, scope='CSPAT00601')
    def create_order(self, asset_code: str, price: int, quantity: int, side: int, order_type: str = '00', order_condition: str = '0', credit_type: str = '000'):
        url = f'{self.host_url}/stock/order'
        tr_cd = 'CSPAT00601'

        headers = {
            'tr_cd': tr_cd,
            'tr_cont': 'N',
        }

        body = {
            f'{tr_cd}InBlock1': {
                'IsuNo': asset_code,  # 주식/ETF: A+종목코드, ELW: J+종목코드, ETN: Q+종목코드
                'OrdQty': quantity,  # 주문수량
                'OrdPrc': price,  # 주문가
                'BnsTpCode': '2' if side == 1 else '1',  # 1: 매도, 2: 매수
                'OrdprcPtnCode': order_type,  # 호가유형코드; 00: 지정가, 03: 시장가, 05: 조건부지정가, 06: 최유리지정가, 07: 최우선지정가, 61: 장개시전시간외종가, 81: 시간외종가, 82: 시간외단일가
                'OrdCndiTpCode': order_condition,  # 주문조건구분; 0: 없음, 1: IOC, 2: FOK
                'MgntrnCode': credit_type,  # 신용거래코드; 000: 보통, 003: 유통/자기융자신규, 005: 유통대주신규, 007: 자기대주신규, 101: 유통융자상환, 103: 자기융자상환, 105: 유통대주상환, 107: 자기대주상환, 180: 예탁담보대출상환(신용)
                'LoanDt': '',  # 대출일
            }
        }

        data = self.post_with_retry(url, headers, body)
        print(data)


    @limit_calls(max_calls=3, scope='CSPAT00701')
    def update_order(self, org_order_no: int, asset_code: str, price: int, quantity: int, order_type: str = '00', order_condition: str = '0'):
        url = f'{self.host_url}/stock/order'
        tr_cd = 'CSPAT00701'

        headers = {
            'tr_cd': tr_cd,
            'tr_cont': 'N',
        }

        body = {
            f'{tr_cd}InBlock1': {
                'OrgOrdNo': org_order_no,  # 원주문번호
                'IsuNo': asset_code,  # 주식/ETF: A+종목코드, ELW: J+종목코드, ETN: Q+종목코드
                'OrdQty': quantity,  # 주문수량
                'OrdPrc': price,  # 주문가
                'OrdprcPtnCode': order_type,  # 호가유형코드; 00: 지정가, 03: 시장가, 05: 조건부지정가, 06: 최유리지정가, 07: 최우선지정가, 61: 장개시전시간외종가, 81: 시간외종가, 82: 시간외단일가
                'OrdCndiTpCode': order_condition,  # 주문조건구분; 0: 없음, 1: IOC, 2: FOK
            }
        }

        data = self.post_with_retry(url, headers, body)
        print(data)


    @limit_calls(max_calls=3, scope='CSPAT00801')
    def cancel_order(self, org_order_no: int, asset_code: str, quantity: int):
        url = f'{self.host_url}/stock/order'
        tr_cd = 'CSPAT00801'

        headers = {
            'tr_cd': tr_cd,
            'tr_cont': 'N',
        }

        body = {
            f'{tr_cd}InBlock1': {
                'OrgOrdNo': org_order_no,  # 원주문번호
                'IsuNo': asset_code,  # 주식/ETF: A+종목코드, ELW: J+종목코드, ETN: Q+종목코드
                'OrdQty': quantity,  # 주문수량
            }
        }

        data = self.post_with_retry(url, headers, body)
        print(data)

        return


    @limit_calls(max_calls=3, scope='t1101')
    def get_orderbook(self, asset_code: str):
        return self._get_quote_info(asset_code)
