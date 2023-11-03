from typing import Dict, List, Tuple

from qupyter.brokerage import StockBroker, StockOrder, StockPosition


async def on_initiailze() -> Dict:
    '''사용자 전략 초기화.

    사용자 전략 실행 시 처음 한번 실행되는 함수입니다. 필요한 초기화 작업을 수행하고 실행주기, 손/익절 조건등의 설정 값을 반환하도록 작성합니다.

    :return: 사용자 전략 설정 값. 다음 필드들을 포함할 수 있습니다.

        - interval (int): 매수/매도 주기 (초)
        - stop_loss_config (Dict): 손절 조건 설정
        - take_profit_config (Dict): 익절 조건 설정
        - open_market_time_margin (int): 거래 시작 시간 조정 (초)
        - close_market_time_margin (int): 거래 마감 시간 조정 (초)
        - test_trade (bool): 모의 투자 여부 (default: False)

    :rtype: Dict

    :examples:

    .. code-block:: python

        async def on_initialize() {
            # ...do-something

            # 사용자 설정을 반환합니다
            config = {
              'interval': 60, # 전략 실행 주기(초). 기본값: 1분

              'stop_loss_config': { # 손절 조건 등록 (optional)
                'A005930': -0.1 # 삼성전자 종목을 평단가 대비 -10% 손실인 경우 손절
              },

              'take_profit_config': { # 익절 조건 (optional)
                'A005930': 0.1 # 삼성전자 종목을 평단가 대비 10% 이상 수익인 경우 익절
              },

              'open_market_time_margin': 300, # 거래 시작 시간 조정 (초). 기본값 300(5분)
              'close_market_time_margin': 300, # 거래 마감 시간 조정 (초). 기본값 300(5분)
            }

            return config
        }
    '''
    pass


async def on_market_open(account_info: Dict, pending_orders: List[StockOrder], positions: List[StockPosition], broker: StockBroker) -> List[Tuple[str, int, int]]:
    '''매일 거래 시작 시 가장 먼저 1회 호출 됩니다.

    이 hook은 당일 장 거래 시작 시간 (보통 9시, 수능일은 10시)에
    사용자가 설정 한 open_market_time_margin 초를 더한 시간입니다.

    예를 들어 사용자가 open_market_time_margin을 300(5분)으로 설정한 경우,
    9시 5분에 on_market_open이 호출됩니다.

    :param account_info: 계좌 정보. :func:`StockBroker.get_account()<qupyter.brokerage.StockBroker.get_account>` 의 반환 값과 동일합니다.
    :type account_info: Dict

    :param pending_orders: 미체결 주문 리스트
    :type pending_orders: List of StockOrder

    :param positions: 보유 종목 리스트
    :type positions: List of StockPosition

    :param broker: 주식 거래를 위한 객체
    :type broker: StockBroker

    :return: 거래 할 종목 리스트. 종목 코드, 거래 수량, 지정 가격을 반환합니다.
                매수 인 경우 양수, 매도 인 경우 음수로 수량을 설정합니다.
    :rtype: List[Tuple[str, int, int]]

    :examples:

    .. code-block:: python

        async def on_market_open(account_info: Dict, pending_orders: List, positions: List, broker: StockBroker) -> List[Tuple[str, int, int]]:
            asset_codes = list(map(lambda x: x.asset_code, positions)))
            price_df = broker.get_price_for_multiple_stocks(asset_codes)

            # 보유 중인 수량 전량 매도
            return list(map(lambda x: (x.asset_code, -x.quantity, x.price), positions))
    '''
    pass


async def on_market_close(account_info: Dict, pending_orders: List[StockOrder], positions: List[StockPosition], broker: StockBroker) -> List[Tuple[str, int, int]]:
    '''매일 거래 종료 시 마지막에 1회 호출 됩니다.

    이 hook이 호출되고 나면 해당일에는 더이상 trade_func 가 호출되지 않습니다.

    이 hook이 호출되는 시간은 당일 장 종료 전 동시 호가 시작 시간 (보통 3시 20분) 에서 사용자가 설정한 close_market_time_margin 초를 뺀 시간입니다. 예를 들어 사용자가 close_market_time_margin을 600(10분)으로 설정한 경우, 3시 10분에 on_market_close hook이 호출됩니다.

    .. warning::
      - 당일 동시 호가 시작 이후에 전략이 새로 배포되거나 업데이트 된 경우 이 hook은 호출되지 않습니다.
      - 이 hook이 호출되고 실제 동시호가 시작 시간 전에 전략을 업데이트하게 되면 이 hook은 다시 호출됩니다.


    :param account_info: 계좌 정보. :func:`StockBroker.get_account()<qupyter.brokerage.StockBroker.get_account>` 의 반환 값과 동일합니다.
    :type account_info: Dict

    :param pending_orders: 미체결 주문 리스트
    :type pending_orders: List of StockOrder

    :param positions: 보유 종목 리스트
    :type positions: List of StockPosition

    :param broker: 주식 거래를 위한 객체
    :type broker: StockBroker

    :return: 거래 할 종목 리스트. 종목 코드, 거래 수량, 지정 가격을 반환합니다.
                매수 인 경우 양수, 매도 인 경우 음수로 수량을 설정합니다.
    :rtype: List[Tuple[str, int, int]]

    :examples:

    .. code-block:: python

        async def on_market_close(account_info: Dict, pending_orders: List, positions: List, broker: StockBroker) -> List[Tuple[str, int, int]]:
            asset_codes = list(map(lambda x: x.asset_code, positions)))
            price_df = broker.get_price_for_multiple_stocks(asset_codes)

            # 보유 중인 수량 전량 매도
            return list(map(lambda x: (x.asset_code, -x.quantity, x.price), positions))
    '''
    pass


async def trade_func(account_info: Dict, pending_orders: List[StockOrder], positions: List[StockPosition], broker: StockBroker) -> List[Tuple[str, int, int]]:
    '''사용자 전략 코드를 구현합니다.

    설정 된 주기마다 호출 되고 매매지시가 필요한 경우 응답으로 전달합니다.

    :param account_info: 계좌 정보. :func:`StockBroker.get_account()<qupyter.brokerage.StockBroker.get_account>` 의 반환 값과 동일합니다.
    :type account_info: Dict

    :param pending_orders: 미체결 주문 리스트
    :type pending_orders: List of StockOrder

    :param positions: 보유 종목 리스트
    :type positions: List of StockPosition

    :param broker: 주식 거래를 위한 객체
    :type broker: StockBroker

    :return: 거래 할 종목 리스트. 종목 코드, 거래 수량, 지정 가격을 반환합니다.
                매수 인 경우 양수, 매도 인 경우 음수로 수량을 설정합니다.
    :rtype: List[Tuple[str, int, int]]

    :examples:

    .. code-block:: python

        async def trade_func(account_info: Dict, pending_orders: List, positions: List, broker: StockBroker) -> List[Tuple[str, int, int]]:
            # 사용자 전략 코드 작성
            # ...

            return [
                ( '005930', 69100, 13 ), # 삼성전자 13주를 69100원에 매수
                ( '252670', 2800, -1 ), # KODEX 200 선물 인버스2X 1주를 2800원에 매도
            ]
    '''
    pass


async def handle_pending_orders(pending_orders: List[Tuple[str, List[StockOrder]]]):
    '''미체결 주문을 확인하고 정정/취소 할 내역을 반환합니다.

    .. note::
        이 hook을 구현하지 않은 경우의 기본 동작은 미체결 주문을 모두 취소하는 것입니다.

    **전량/일부취소**

    취소 지시는 가격은 None으로 지정하고, 취소하고자 하는 수량(최대 '잔량'과 같거나 적은 수량)을 지정합니다.
    수량은 음수로 지정합니다.

    .. code-block:: python

        # 남은 수량 전량 취소
        return [( order.asset_code, order.order_id, None, -order.pending_quantity ) for order in pending_orders]

    **정정**

    정정은 기존 주문 수량 최대까지만 가능합니다. (그 이상은 추가 매수이기 때문에 새로운 주문을 발행해야 합니다)
    가격은 필수로 지정해야 합니다.
    수량은 양수로 지정합니다.

    .. code-block:: python

        # 가격을 현재가로 변경하고, 남은 수량 전량 정정
        return [( order.asset_code, order.order_id, order.current_price, order.pending_quantity ) for order in pending_orders]



    :param pending_orders: 미체결 주문 리스트
    :type pending_orders: List of Tuple (종목코드, 주문목록)

    :return: 정정/취소 할 내역을 담은 리스트. 각 내역은 종목코드, 주문 ID, 가격, 수량을 반환합니다.
    :rtype: List[Tuple[str, int, int, int]]

    '''
    pass

