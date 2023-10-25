import pandas as pd
from typing import List, Dict

class StockBroker:
    """ 증권사 API를 사용하기 위한 클래스"""

    def get_price(self, asset_code: str) -> pd.DataFrame:
        """단일 종목 시세 조회

        :param asset_code: 종목코드
        :type asset_code: str

        :return: 종목 시세
        :rtype: pandas.DataFrame

        DataFrame에는 다음 필드들이 포함됩니다.

        * code: 종목코드
        * name: 종목명
        * current_price: 현재가
        * volume: 거래량
        * volume_nominal: 거래대금
        * open_price: 시가
        * high_price: 고가
        * low_price: 저가
        * max_price: 상한가
        * min_price: 하한가
        * market_capitalization: 시가총액
        * ask_price_1~5: 매도호가 1~5차
        * ask_volume_1~5: 매도호가수량 1~5차
        * bid_price_1~5: 매수호가 1~5차
        * bid_volume_1~5: 매수호가수량 1~5차
        * ask_volume_total: 매도호가 총 잔량
        * bid_volume_total: 매수호가 총 잔량

        :examples:

        .. code-block:: python

            >>> price_df = broker.get_price(asset_code='005930')
            >>> print(price_df)

                    name  current_price    volume  volume_nominal  open_price  high_price  ...  ask_price_5  bid_price_5  ask_volume_5  bid_volume_5  ask_volume_total  bid_volume_total
            code                                                                           ...
            005930  삼성전자          68000  10527625    718811000000       68800       68800  ...        68500        67600        107929         99315            554013           1069461

        """
        pass


    def get_price_for_multiple_stocks(self, asset_codes: List[str]) -> pd.DataFrame:
        """복수 종목 시세 조회.

        :param asset_codes: 종목코드 리스트
        :type asset_codes: List[str]

        :return: 종목 시세
        :rtype: pandas.DataFrame

        DataFrame에는 다음 필드들이 포함됩니다.

        * code: 종목코드
        * name: 종목명
        * current_price: 현재가
        * volume: 거래량
        * volume_nominal: 거래대금
        * open_price: 시가
        * high_price: 고가
        * low_price: 저가
        * max_price: 상한가
        * min_price: 하한가
        * ask_price_1: 1차 매도호가
        * bid_price_1: 1차 매수호가
        * ask_volume_total: 매도호가 총 잔량
        * bid_volume_total: 매수호가 총 잔량

        :examples:

        .. code-block:: python

            >>> price_df = broker.get_price_for_multiple_stocks(asset_codes=['005930', '000660'])
            >>> print(price_df)

                    name  current_price    volume  volume_nominal  open_price  high_price  ...  max_price  min_price  ask_price_1  bid_price_1  ask_volume_total  bid_volume_total
            code                                                                           ...
            005930  삼성전자          68000  10542622    719831000000       68800       68800  ...      89000      48000        68100        68000            554013           1069461
            005380   현대차         182000    373131     68135000000      182700      183700  ...     237500     128000       182100       182000              8070             45848

            [2 rows x 13 columns]
        """
        data = self.stock_broker.get_price_for_multiple_stocks(asset_codes=asset_codes)
        df = pd.DataFrame(data)
        df.set_index('code', inplace=True)
        return df


    def get_account(self) -> Dict:
        """계좌 정보 조회

        :return: 계좌 정보
        :rtype: Dict

        Dict에는 다음 필드들이 포함됩니다.

        * investable_cache: 현금 주문 가능 금액
        * asset_value: 주식 잔고 평가 금액
        * receivable_amount: 미수금
        * total_balance: 예탁자산총액
        * pnl_pct: 손익율
        * investment_principal: 투자원금
        * investment_pnl_amount: 투자손익금액
        * credit_order_amount: 신용담보주문금액
        * credit_orderable_amount: 신용주문가능금액
        * deposit: 예수금
        * substitute_amount: 대용금액
        * deposit_d1: D+1 예수금
        * deposit_d2: D+2 예수금
        * cash_receivables: 현금미수금액
        * cash_collateral: 증거금현금
        * substitute_collateral: 증거금대용
        * cheque_amount: 수표금액
        * substitute_orderable_amount: 대용주문가능금액
        * margin_rate_35_pct_orderable_amount: 증거금률 35% 주문 가능금액
        * margin_rate_50_pct_orderable_amount: 증거금률 50% 주문 가능금액
        * margin_rate_100_pct_orderable_amount: 증거금률 100% 주문가능금액
        * d1_overdraft_fee: D+1 연체변제소요금액
        * d2_overdraft_fee: D+2 연체변제소요금액
        * deposit_pledge_loan_amount: 예탁담보대출금액
        * credit_setting_collateral: 신용설정보증금
        * margin_loan_amount: 융자금액
        * original_pledge_amount: 원담보금액
        * subordinate_pledge_amount: 부담보금액
        * required_pledge_amount: 소요담보금액
        * original_pledge_shortage: 원담보부족금액
        * subordinate_pledge_shortage: 담보부족금액
        * additional_collateral_cash: 추가담보현금
        * unpaid_interest: 신용이자미납금액
        * other_loan_amount: 기타대여금액
        * d1_margin_call_amount: 익일추정반대매매금액
        * original_pledge_total_amount: 원담보합계금액
        * subordinate_pledge_total_amount: 부담보합계금액
        * credit_collateral_cash: 신용담보금현금
        * credit_collateral_substitute: 신용담보대용금액
        * additional_credit_collateral_cash: 추가신용담보현금
        * reused_credit_collateral_amount: 신용담보재사용금액
        * additional_credit_collateral_substitute: 추가신용담보대용
        * sellout_collateral_loan_amount: 매도대금담보대출금액
        * disposal_limit_amount: 처분제한금액

        """
        pass


    def create_order(self, asset_code: str, price: int, quantity: int, side: int):
        """신규 주문 생성

        :param asset_code: 종목코드
        :type asset_code: str

        :param price: 주문가격
        :type price: int

        :param quantity: 주문수량
        :type quantity: int

        :param side: 매매구분 (1: 매도, 2: 매수)
        :type side: int
        """
        self.stock_broker.create_order(
            asset_code=asset_code,
            price=price,
            quantity=quantity,
            side=side,
        )


    def update_order(self, org_order_id: int, asset_code: str, price: int, quantity: int):
        """정정 주문

        :param org_order_id: 원주문번호
        :type org_order_id: str

        :param asset_code: 종목코드
        :type asset_code: str

        :param price: 주문가격
        :type price: int

        :param quantity: 주문수량
        :type quantity: int
        """
        self.stock_broker.update_order(
            org_order_no=org_order_id,
            asset_code=asset_code,
            price=price,
            quantity=quantity,
        )


    def cancel_order(self, order_id: int, asset_code: str, quantity: int):
        """주문 취소

        :param order_id: 주문번호
        :type order_id: str

        :param asset_code: 종목코드
        :type asset_code: str

        :param quantity: 주문수량
        :type quantity: int
        """
        self.stock_broker.cancel_order(
            org_order_no=order_id,
            asset_code=asset_code,
            quantity=quantity,
        )


    def get_positions(self) -> List:
        """보유 포지션 조회

        :return: 보유 포지션
        :rtype: list of StockPosition
        """
        stock_positions = self.stock_broker.get_positions()

        return stock_positions


    def get_pending_orders(self) -> List:
        """미체결 주문내역 조회

        :return: 미체결 주문내역
        :rtype: list of StockOrder
        """
        stock_pending_orders = self.stock_broker.get_pending_orders()

        return stock_pending_orders


    def get_orderbook(self, asset_code: str):
        """ 최근 호가 데이터 획득 """
        return