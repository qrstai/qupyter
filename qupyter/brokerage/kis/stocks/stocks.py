import asyncio
import datetime
from decimal import Decimal
import json
import time
import httpx

from requests import HTTPError

from qupyter.brokerage.kis.core import KIS
from qupyter.brokerage.models import StockOrder, StockPosition
from qupyter.brokerage.utils.market_schedule import get_market_schedule
from typing import Dict, List, Tuple

from qupyter.brokerage.utils.retry import async_retry, retry


class KISStocks(KIS):
    def __init__(self, test_trade: bool, account_number: str, product_code: str, **kwargs):
        super().__init__(test_trade, account_number, product_code, **kwargs)

    @retry(HTTPError, delay=0.1)
    def request_with_retry(self, method: str, url: str, headers: dict = None, params: dict = None, body: dict = None, return_headers: bool = False) -> Dict | Tuple[Dict, Dict]:
        r = self.session.request(method=method, url=url, headers=headers, params=params, json=body)
        body = r.json()
        if r.status_code != 200:
            if body.get('rt_cd') in ['EGW00121', 'EGW00123']: # 만료된 토큰
                self.refresh_token()
            else:
                print('KIS API response error:', body)

            r.raise_for_status()

        if return_headers:
            headers = r.headers
            return body, headers
        else:
            return body

    def post_with_retry(self, url: str, headers: dict, body: dict, return_headers: bool = False) -> Dict | Tuple[Dict, Dict]:
        return self.request_with_retry(method='POST', url=url, headers=headers, body=body, return_headers=return_headers)

    def get_with_retry(self, url: str, headers: dict, params: dict, return_headers: bool = False) -> Dict | Tuple[Dict, Dict]:
        return self.request_with_retry(method='GET', url=url, headers=headers, params=params, return_headers=return_headers)


    @async_retry(httpx.HTTPStatusError, delay=0.3, silently=False)
    async def async_request_with_retry(self, method: str, url: str, headers: dict = None, params: dict = None, body: dict = None, return_headers: bool = False):
        async with httpx.AsyncClient() as client:
            r = await client.request(method=method, url=url, headers=headers, params=params, json=body)
            body = r.json()
            if r.status_code != 200:
                if body.get('rt_cd') in ['EGW00121', 'EGW00123']:
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

    async def _async_get_quote_info(self, asset_code: str):
        url = f'{self.host_url}/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn'

        headers = self.make_session_headers()
        headers.update({
            'tr_id': 'FHKST01010200',
        })

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': asset_code,
        }

        data = await self.async_request_with_retry(method='get', url=url, headers=headers, params=params)

        output1 = data.get('output1', {})

        res = {
            'ask_price_1': int(output1.get('askp1', 0)),  # 1차 매도호가
            'bid_price_1': int(output1.get('bidp1', 0)),  # 1차 매수호가
            'ask_volume_1': int(output1.get('askp_rsqn1', 0)),  # 1차 매도호가수량
            'bid_volume_1': int(output1.get('bidp_rsqn1', 0)),  # 1차 매수호가수량
            'ask_price_2': int(output1.get('askp2', 0)),  # 2차 매도호가
            'bid_price_2': int(output1.get('bidp2', 0)),  # 2차 매수호가
            'ask_volume_2': int(output1.get('askp_rsqn2', 0)),  # 2차 매도호가수량
            'bid_volume_2': int(output1.get('bidp_rsqn2', 0)),  # 2차 매수호가수량
            'ask_price_3': int(output1.get('askp3', 0)),  # 3차 매도호가
            'bid_price_3': int(output1.get('bidp3', 0)),  # 3차 매수호가
            'ask_volume_3': int(output1.get('askp_rsqn3', 0)),  # 3차 매도호가수량
            'bid_volume_3': int(output1.get('bidp_rsqn3', 0)),  # 3차 매수호가수량
            'ask_price_4': int(output1.get('askp4', 0)),  # 4차 매도호가
            'bid_price_4': int(output1.get('bidp4', 0)),  # 4차 매수호가
            'ask_volume_4': int(output1.get('askp_rsqn4', 0)),  # 4차 매도호가수량
            'bid_volume_4': int(output1.get('bidp_rsqn4', 0)),  # 4차 매수호가수량
            'ask_price_5': int(output1.get('askp5', 0)),  # 5차 매도호가
            'bid_price_5': int(output1.get('bidp5', 0)),  # 5차 매수호가
            'ask_volume_5': int(output1.get('askp_rsqn5', 0)),  # 5차 매도호가수량
            'bid_volume_5': int(output1.get('bidp_rsqn5', 0)),  # 5차 매수호가수량
            'ask_volume_total': int(output1.get('total_askp_rsqn', 0)),  # 총 매도호가수량
            'bid_volume_total': int(output1.get('total_bidp_rsqn', 0)),  # 총 매수호가수량
        }

        return res

    def _get_quote_info(self, asset_code: str):
        url = f'{self.host_url}/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn'

        headers = {
            'tr_id': 'FHKST01010200',
        }

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': asset_code,
        }

        data = self.get_with_retry(url=url, headers=headers, params=params)

        output1 = data.get('output1', {})

        res = {
            'ask_price_1': int(output1.get('askp1', 0)),  # 1차 매도호가
            'bid_price_1': int(output1.get('bidp1', 0)),  # 1차 매수호가
            'ask_volume_1': int(output1.get('askp_rsqn1', 0)),  # 1차 매도호가수량
            'bid_volume_1': int(output1.get('bidp_rsqn1', 0)),  # 1차 매수호가수량
            'ask_price_2': int(output1.get('askp2', 0)),  # 2차 매도호가
            'bid_price_2': int(output1.get('bidp2', 0)),  # 2차 매수호가
            'ask_volume_2': int(output1.get('askp_rsqn2', 0)),  # 2차 매도호가수량
            'bid_volume_2': int(output1.get('bidp_rsqn2', 0)),  # 2차 매수호가수량
            'ask_price_3': int(output1.get('askp3', 0)),  # 3차 매도호가
            'bid_price_3': int(output1.get('bidp3', 0)),  # 3차 매수호가
            'ask_volume_3': int(output1.get('askp_rsqn3', 0)),  # 3차 매도호가수량
            'bid_volume_3': int(output1.get('bidp_rsqn3', 0)),  # 3차 매수호가수량
            'ask_price_4': int(output1.get('askp4', 0)),  # 4차 매도호가
            'bid_price_4': int(output1.get('bidp4', 0)),  # 4차 매수호가
            'ask_volume_4': int(output1.get('askp_rsqn4', 0)),  # 4차 매도호가수량
            'bid_volume_4': int(output1.get('bidp_rsqn4', 0)),  # 4차 매수호가수량
            'ask_price_5': int(output1.get('askp5', 0)),  # 5차 매도호가
            'bid_price_5': int(output1.get('bidp5', 0)),  # 5차 매수호가
            'ask_volume_5': int(output1.get('askp_rsqn5', 0)),  # 5차 매도호가수량
            'bid_volume_5': int(output1.get('bidp_rsqn5', 0)),  # 5차 매수호가수량
            'ask_volume_total': int(output1.get('total_askp_rsqn', 0)),  # 총 매도호가수량
            'bid_volume_total': int(output1.get('total_bidp_rsqn', 0)),  # 총 매수호가수량
        }

        return res


    def _get_price_info(self, asset_code: str):
        url = f'{self.host_url}/uapi/domestic-stock/v1/quotations/inquire-price'

        headers = {
            'tr_id': 'FHKST01010100',
        }

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': asset_code,
        }

        data = self.get_with_retry(url=url, headers=headers, params=params)

        output = data.get('output', {})

        res = {
            'code': asset_code,  # 종목코드
            'current_price': int(output.get('stck_prpr', 0)),  # 현재가
            'volume': int(output.get('acml_vol', 0)),  # 누적거래량
            'volume_nominal': int(output.get('acml_tr_pbmn', 0)),  # 누적거래대금 (단위: 원)
            'open_price': int(output.get('stck_oprc', 0)),  # 시가
            'high_price': int(output.get('stck_hgpr', 0)),  # 고가
            'low_price': int(output.get('stck_lwpr', 0)),  # 저가
            'max_price': int(output.get('stck_mxpr', 0)),  # 상한가
            'min_price': int(output.get('stck_llam', 0)),  # 하한가
            'market_capitalization': int(output.get('hts_avls', 0)) * 100_000_000,  # 시가총액 (단위: 억원)
        }

        return res

    async def _async_get_price_info(self, asset_code: str):
        url = f'{self.host_url}/uapi/domestic-stock/v1/quotations/inquire-price'

        headers = self.make_session_headers()
        headers.update({
            'tr_id': 'FHKST01010100',
        })

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': asset_code,
        }

        data = await self.async_request_with_retry(method='GET', url=url, headers=headers, params=params)

        output = data.get('output', {})

        res = {
            'code': asset_code,  # 종목코드
            'current_price': int(output.get('stck_prpr', 0)),  # 현재가
            'volume': int(output.get('acml_vol', 0)),  # 누적거래량
            'volume_nominal': int(output.get('acml_tr_pbmn', 0)),  # 누적거래대금 (단위: 원)
            'open_price': int(output.get('stck_oprc', 0)),  # 시가
            'high_price': int(output.get('stck_hgpr', 0)),  # 고가
            'low_price': int(output.get('stck_lwpr', 0)),  # 저가
            'max_price': int(output.get('stck_mxpr', 0)),  # 상한가
            'min_price': int(output.get('stck_llam', 0)),  # 하한가
            'market_capitalization': int(output.get('hts_avls', 0)) * 100_000_000,  # 시가총액 (단위: 억원)
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



    async def async_get_price(self, asset_code: str):
        """ 단일 종목 시세 조회 """

        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        results = await asyncio.gather(*[
            self._async_get_price_info(asset_code=asset_code),
            self._async_get_quote_info(asset_code=asset_code),
        ])

        price_info = results[0]
        quote_info = results[1]

        price_info.update(quote_info)

        return price_info


    def get_price_for_multiple_stocks(self, asset_codes: List[str]):
        async def _chunked_request():
            group_size = 15
            copied = asset_codes.copy()
            result = []

            while len(copied) > 0:
                chunk = copied[:group_size]
                copied = copied[group_size:]

                st = time.time()
                result += await asyncio.gather(*[self.async_get_price(asset_code) for asset_code in chunk])
                elapsed = time.time() - st

                if len(copied) > 0:
                    sleep_time = max(0.01, 1.05 - elapsed)
                    await asyncio.sleep(sleep_time)

            return result


        event_loop = asyncio.get_event_loop()
        task = event_loop.create_task(_chunked_request())
        result = event_loop.run_until_complete(task)

        return result


    def get_today_minute_data(self, asset_code: str):
        """당일 분봉 데이터 조회
        NOTE 한 번의 호출에 최대 30건까지 확인 가능합니다.
        """
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        url = f'{self.host_url}/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice'

        request_time = datetime.datetime.now().replace(second=0, microsecond=0)

        market_schedule = get_market_schedule()
        market_open_time = datetime.datetime.combine(request_time.date(), market_schedule.open_time)

        headers = {
            'tr_id': 'FHKST03010200',
            'tr_cont': '',
        }

        params = {
            'FID_ETC_CLS_CODE': '',
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': asset_code,
            'FID_PW_DATA_INCU_YN': 'N',
        }

        make_call = True

        data = []

        while make_call:
            params['FID_INPUT_HOUR_1'] = request_time.strftime('%H%M%S')  # 조회 시작시간 (HHMMSS)

            res_data = self.get_with_retry(url=url, headers=headers, params=params)
            output2 = res_data.get('output2', [])

            for item in output2:
                item_time = datetime.datetime.strptime(f"{item['stck_bsop_date']} {item['stck_cntg_hour']}", '%Y%m%d %H%M%S')
                data.append({
                    'time': f'{item_time.year}-{item_time.month}-{item_time.day} {item_time.hour}:{item_time.minute}:{item_time.second}',
                    'open': int(item.get('stck_oprc', 0)),
                    'high': int(item.get('stck_hgpr', 0)),
                    'low': int(item.get('stck_lwpr', 0)),
                    'close': int(item.get('stck_prpr', 0)),
                    'volume': int(item.get('cntg_vol', 0)),
                })

            if len(output2) == 0:
                make_call = False
                break

            last_item = output2[-1]
            last_item_time = datetime.datetime.strptime(f"{last_item['stck_bsop_date']} {last_item['stck_cntg_hour']}", '%Y%m%d %H%M%S')
            request_time = last_item_time - datetime.timedelta(minutes=1)

            if request_time < market_open_time:
                make_call = False
                break

        return data


    def get_historical_daily_data(self, asset_code: str, adjusted_price: bool = False, first_date: datetime.date = None, last_date: datetime.date = None):
        """과거 일봉 데이터 조회
        :param str asset_code: 종목코드
        :param bool adjusted_price: 수정주가여부
        :param date first_date: 조회 시작일자 (`None`일 경우 당일 조회)
        :param date last_date: 조회 종료일자 (`None`인 경우 당일 조회)

        NOTE 한 번의 호출에 최대 100건까지 확인 가능
        """
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        url = f'{self.host_url}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice'

        headers = {
            'tr_id': 'FHKST03010100',
        }

        params = {
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': asset_code,
            'FID_PERIOD_DIV_CODE': 'D',
            'FID_ORG_ADJ_PRC': '0' if adjusted_price else '1',  # 0: 수정주가, 1: 원주가
        }

        if not first_date:
            first_date = datetime.datetime.now().date()

        if not last_date:
            last_date = datetime.datetime.now().date()

        interval_days  = 100
        num_intervals = (last_date - first_date).days // interval_days + 1
        date_intervals = []
        for i in range(num_intervals):
            interval_first_date = first_date + datetime.timedelta(days=i * interval_days)
            interval_last_date = first_date + datetime.timedelta(days=(i+1) * interval_days - 1)

            # ensure interval_last_date does not exceed the last_date
            interval_last_date = min(interval_last_date, last_date)

            date_intervals.append((interval_first_date, interval_last_date))

        data = []
        for interval in date_intervals:
            params['FID_INPUT_DATE_1'] = interval[0].strftime('%Y%m%d')  # 조회 시작일자 (YYYYMMDD)
            params['FID_INPUT_DATE_2'] = interval[1].strftime('%Y%m%d')  # 조회 종료일자 (YYYYMMDD)

            res_data = self.get_with_retry(url=url, headers=headers, params=params)
            output2 = res_data.get('output2', [])

            _data = []
            for item in output2:
                _date = item.get('stck_bsop_date')
                _item = {
                    'date': f'{_date[:4]}-{_date[4:6]}-{_date[6:]}',  # 날짜
                    'open': int(item.get('stck_oprc', 0)),  # 시가
                    'high': int(item.get('stck_hgpr', 0)),  # 고가
                    'low': int(item.get('stck_lwpr', 0)),  # 저가
                    'close': int(item.get('stck_clpr', 0)),  # 종가
                    'volume': int(item.get('acml_vol', 0)),  # 거래량
                    'volume_nominal': int(item.get('acml_tr_pbmn', 0)),  # 거래대금 (단위: 원)
                }
                _data.append(_item)

            _data.reverse()
            data.extend(_data)

        return data


    # ----------------------------------------------------------------------------------------------------
    # 계좌 관련
    # ----------------------------------------------------------------------------------------------------

    def get_account(self):
        """ 계좌 정보 조회 """

        balance = self._get_balance()

        # 한투 API 에 주문가능현금을 직접 얻을 수 있는 API가 없어
        # 주문 가능 수량을 얻는 API를 통해 간접적으로 얻는다.
        affordable = self._get_affordable_quantity('069500')

        asset_value = int(balance.get('scts_evlu_amt', 0))
        total_balance = int(balance.get('tot_evlu_amt', 0))
        investable_cash = int(affordable.get('ord_psbl_cash', 0))

        res = {
            'investable_cash': investable_cash,
            'asset_value': asset_value,
            'total_balance': total_balance,
            'broker_data': balance
        }

        return res

    def _get_balance(self):
        url = f'{self.host_url}/uapi/domestic-stock/v1/trading/inquire-balance'

        headers = {
            'tr_id': 'VTTC8434R' if self.test_trade else 'TTTC8434R',
        }

        params = {
            'CANO': self.account_number,
            'ACNT_PRDT_CD': self.product_code,
            'AFHR_FLPR_YN': 'N',
            'OFL_YN': '',
            'INQR_DVSN': '02',
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'N',
            'FNCG_AMT_AUTO_RDPT_YN': 'N',
            'PRCS_DVSN': '00',
            'CTX_AREA_FK100': '',
            'CTX_AREA_NK100': '',
        }

        broker_data = self.get_with_retry(url, headers=headers, params=params)

        output2 = broker_data.get('output2', [])

        if len(output2) == 1:
            res = output2[0]


        else:
            res = {}

        return res

    def _get_affordable_quantity(self, asset_code: str):
        url = f"{self.host_url}/uapi/domestic-stock/v1/trading/inquire-psbl-order"
        headers = {
            "tr_id": "VTTC8908R" if self.test_trade else "TTTC8908R",
            "tr_cont": "",
        }
        params = {
            "CANO": self.account_number,
            "ACNT_PRDT_CD": self.product_code,
            "PDNO": asset_code,
            "ORD_UNPR": "",
            "ORD_DVSN": "01",
            "CMA_EVLU_AMT_ICLD_YN": "N",
            "OVRS_ICLD_YN": "N"
        }

        r = self.get_with_retry(url=url, headers=headers, params=params)
        if r['rt_cd'] != '0':
            raise Exception(f"{r['rt_cd']}: {r['msg1']}")

        return r['output']


    def _create_stock_position(self, json_dict: dict) -> StockPosition:
        return StockPosition(
            asset_code=json_dict.get('pdno'), # 종목코드
            asset_name=json_dict.get('prdt_name'), # 종목명
            quantity=int(json_dict.get('hldg_qty', 0)), # 잔고수량
            exit_available_quantity=int(json_dict.get('ord_psbl_qty', 0)), # 청산가능수량
            average_purchase_price=Decimal(json_dict.get('pchs_avg_pric', 0)), # 평균단가
            purchase_value=int(json_dict.get('pchs_amt', 0)), # 매입금액
            loan_value=int(json_dict.get('loan_amt', 0)), # 대출금액
            loan_date=json_dict.get('loan_dt'), # 대출일자
            expiration_date=json_dict.get('expd_dt'), # 만기일자
            current_price=int(json_dict.get('prpr', 0)), # 현재가
            current_value=int(json_dict.get('evlu_amt', 0)), # 평가금액
            current_pnl=int(json_dict.get('evlu_pfls_amt', 0)), # 평가손익, 응답에 값이 없어 나중에 채워줘야 함.
            current_pnl_pct=json_dict.get('evlu_pfls_rt'), # 수익율, 응답에 값이 없어 나중에 채워줘야 함.
            commission=0, # 수수료, 응답에 값이 없어 나중에 채워줘야 함.
            tax=0,
            loan_interest=0, # 신용이자, 응답에 값이 없어 나중에 채워줘야 함.
        )

    def get_positions(self, exclude_empty_positions: bool):
        """ 보유 포지션 목록 조회
        NOTE (한국투자증권 API 명세서 발췌)
        - 실전계좌의 경우, 한 번의 호출에 최대 50건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.
        - 모의계좌의 경우, 한 번의 호출에 최대 20건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.

        TODO
        - StockPosition에서 키값 참조하는 부분 수정하고 프로덕션에 맞추기
        """

        url = f'{self.host_url}/uapi/domestic-stock/v1/trading/inquire-balance'

        make_call = True

        headers = {
            'tr_id': 'VTTC8434R' if self.test_trade else 'TTTC8434R',
            'tr_cont': '',
        }

        params = {
            'CANO': self.account_number,
            'ACNT_PRDT_CD': self.product_code,
            'AFHR_FLPR_YN': 'N',
            'OFL_YN': '',
            'INQR_DVSN': '02',
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'N',
            'FNCG_AMT_AUTO_RDPT_YN': 'N',
            'PRCS_DVSN': '00',
            'CTX_AREA_FK100': '',
            'CTX_AREA_NK100': '',
        }

        positions: List[StockPosition] = []

        while make_call:
            res_data, res_header = self.get_with_retry(url=url, headers=headers, params=params, return_headers=True)

            output1 = res_data.get('output1', [])
            for item in output1:
                position = self._create_stock_position(item)

                # 전량 매도한 경우 D+2 결제 상태를 무시하고 보유 포지션 반환값에 포함하지 않을 경우
                if exclude_empty_positions and position.quantity == 0:
                    continue

                positions.append(position)

            # 연속조희 여부
            tr_cont = res_header.get('tr_cont')
            if tr_cont == 'F' or tr_cont == 'M':
                headers['tr_cont'] = 'N'
                params['CTX_AREA_FK100'] = res_data.get('ctx_area_fk100')
                params['CTX_AREA_NK100'] = res_data.get('ctx_area_nk100')
            else:
                make_call = False
                break

        return positions


    def _create_stock_order(self, json_dict: dict) -> StockOrder:
        filled_amount = int(json_dict.get('tot_ccld_amt', 0)) # 총체결수량
        filled_qty = int(json_dict.get('tot_ccld_qty', 0)) # 총체결금액
        filled_price = filled_amount // filled_qty if filled_qty > 0 else 0
        order_time = datetime.datetime.strptime(json_dict.get('ord_tmd'), '%H%M%S').time() # 주문시각
        today = datetime.datetime.today().date()

        return StockOrder(
            order_id=int(json_dict.get('odno')), # 주문번호
            asset_code=json_dict.get('pdno'), # 종목코드
            trade_type=int(json_dict.get('sll_buy_dvsn_cd')), # 매도매수구분코드 01:매도, 02:매수
            quantity=int(json_dict.get('ord_qty')), # 주문수량
            price=int(json_dict.get('ord_unpr')), # 주문단가
            filled_quantity=filled_qty, # 체결수량
            filled_price=filled_price, # 체결단가
            pending_quantity=int(json_dict.get('psbl_qty', 0)), # 미체결수량
            order_time=datetime.datetime.combine(today, order_time), # 주문시간
            order_method='unknown', # 주문방법
            current_price=0, # 현재가, 응답에 값이 없어 나중에 채워줘야 함.
        )

    def get_pending_orders(self):
        """
        미체결 주문 내역 조회
        NOTE (한국투자증권 API 명세서 발췌)
        - 모의투자 미지원
        - 한 번의 호출에 최대 50건까지 확인 가능하며, 이후의 값은 연속조회를 통해 확인하실 수 있습니다.
        """

        if not self.test_trade:
            url = f'{self.host_url}/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl'

            make_call = True

            headers = {
                'tr_id': 'TTTC8036R',
                'tr_cont': '',
            }

            params = {
                'CANO': self.account_number,
                'ACNT_PRDT_CD': self.product_code,
                'CTX_AREA_FK100': '',
                'CTX_AREA_NK100': '',
                'INQR_DVSN_1': '1',  # 0: 조회순서, 1: 주문순
                'INQR_DVSN_2': '0',
            }

            pending_orders: List = []


            while make_call:
                res_data, res_header = self.get_with_retry(url=url, headers=headers, params=params, return_headers=True)
                output = res_data.get('output', [])
                for item in output:
                    pending_orders.append(self._create_stock_order(item))


                # 연속조희 여부
                tr_cont = res_header.get('tr_cont')
                if tr_cont == 'F' or tr_cont == 'M':
                    headers['tr_cont'] = 'N'
                    params['CTX_AREA_FK100'] = res_data.get('ctx_area_fk100')
                    params['CTX_AREA_NK100'] = res_data.get('ctx_area_nk100')
                else:
                    make_call = False
                    break

            # 현재가 조회
            asset_codes = list(set([order.asset_code for order in pending_orders]))
            price_dict = {}
            for asset_code in asset_codes:
                data = self._get_price_info(asset_code)
                price_dict[asset_code] = data.get('current_price', 0)

            pending_orders_dict = {}
            for order in pending_orders:
                order.current_price = price_dict.get(order.asset_code, 0)

                if order.asset_code in pending_orders_dict:
                    pending_orders_dict[order.asset_code].append(order)
                else:
                    pending_orders_dict[order.asset_code] = [order]

            result = []
            for k, v in pending_orders_dict.items():
                result.append((k, v))
            return result

        else:
            return []


    # ----------------------------------------------------------------------------------------------------
    # 주문 관련
    # ----------------------------------------------------------------------------------------------------

    def create_order(self, asset_code: str, price: int, quantity: int, side: int, order_type: str = '00', order_condition: str = '0', credit_type: str = '000'):
        """
        NOTE
        [주문구분]
        00 : 지정가
        01 : 시장가
        02 : 조건부지정가
        03 : 최유리지정가
        04 : 최우선지정가
        05 : 장전 시간외 (08:20~08:40)
        06 : 장후 시간외 (15:30~16:00)
        07 : 시간외 단일가(16:00~18:00)
        08 : 자기주식
        09 : 자기주식S-Option
        10 : 자기주식금전신탁
        11 : IOC지정가 (즉시체결,잔량취소)
        12 : FOK지정가 (즉시체결,전량취소)
        13 : IOC시장가 (즉시체결,잔량취소)
        14 : FOK시장가 (즉시체결,전량취소)
        15 : IOC최유리 (즉시체결,잔량취소)
        16 : FOK최유리 (즉시체결,전량취소)

        TODO 주문구분 값은 Qupyter가 제공하는 키값으로 매핑할 것

        """
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        url = f'{self.host_url}/uapi/domestic-stock/v1/trading/order-cash'

        if self.test_trade:
            tr_id = 'VTTC0802U' if side == 1 else 'VTTC0801U'
        else:
            tr_id = 'TTTC0802U' if side == 1 else 'TTTC0801U'

        headers = {
            'tr_id': tr_id,
        }

        body = {
            'CANO': self.account_number,
            'ACNT_PRDT_CD': self.product_code,
            'PDNO': asset_code,
            'ORD_DVSN': order_type,  # 주문구분
            'ORD_QTY': str(quantity),  # 주문주식수
            'ORD_UNPR': str(price),  # 주문단가
        }

        res_data, res_header = self.post_with_retry(url=url, headers=headers, body=body, return_headers=True)

        print(res_header)
        print(res_data)


    def update_order(self, org_order_no: int, asset_code: str, price: int, quantity: int, order_type: str = '00', order_condition: str = '0'):
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        url = f'{self.host_url}/uapi/domestic-stock/v1/trading/order-rvsecncl'

        headers = {
            'tr_id': 'VTTC0803U' if self.test_trade else 'TTTC0803U',
        }

        body = {
            'CANO': self.account_number,
            'ACNT_PRDT_CD': self.product_code,
            'KRX_FWDG_ORD_ORGNO': '',  # 한국거래소전송주문조직번호 (주문시 한국투자증권 시스템에서 지정된 영업점코드) - "" (Null 값 설정)
            'ORGN_ODNO': str(org_order_no),  # 원주문번호
            'ORD_DVSN': order_type,  # 주문구분
            'RVSE_CNCL_DVSN_CD': '01',  # 정정취소구분코드 (01: 정정, 02: 취소)
            'ORD_QTY': str(quantity),  # 주문수량
            'ORD_UNPR': str(price),  # 주문단가 (정정 => 1주당 가격 / 취소 => "0" 설정)
            'QTY_ALL_ORD_YN': 'N',  # 잔량전부주문여부 (Y: 잔량전부, N: 잔량일부)
        }

        res_data, res_header = self.post_with_retry(url=url, headers=headers, body=body, return_headers=True)

        print(res_header)
        print(res_data)


    def cancel_order(self, org_order_no: int, asset_code: str, quantity: int, order_type: str = '00'):
        if len(asset_code) > 6:
            asset_code = asset_code[1:]

        url = f'{self.host_url}/uapi/domestic-stock/v1/trading/order-rvsecncl'

        headers = {
            'tr_id': 'VTTC0803U' if self.test_trade else 'TTTC0803U',
        }

        body = {
            'CANO': self.account_number,
            'ACNT_PRDT_CD': self.product_code,
            'KRX_FWDG_ORD_ORGNO': '',  # 한국거래소전송주문조직번호 (주문시 한국투자증권 시스템에서 지정된 영업점코드) - "" (Null 값 설정)
            'ORGN_ODNO': str(org_order_no),  # 원주문번호
            'ORD_DVSN': order_type,  # 주문구분
            'RVSE_CNCL_DVSN_CD': '02',  # 정정취소구분코드 (01: 정정, 02: 취소)
            'ORD_QTY': str(quantity),  # 주문수량
            'ORD_UNPR': '0',  # 주문단가 (정정 => 1주당 가격 / 취소 => "0" 설정)
            'QTY_ALL_ORD_YN': 'N',  # 잔량전부주문여부 (Y: 잔량전부, N: 잔량일부)
        }

        res_data, res_header = self.post_with_retry(url=url, headers=headers, body=body, return_headers=True)

        print(res_header)
        print(res_data)
