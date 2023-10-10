from typing import Callable, List
import pykrx
import websockets
import json
import time
import asyncio

from qupyter import config


def get_ticker_list():
    """
    Ticker 조회

    지원하는 종목 Ticker를 리스트로 반환합니다.
    (현재 KOSPI 상위 200개 종목만 지원)

    Returns
    -------
    list of str
        Ticker 목록.
    """
    tickers = pykrx.stock.get_index_portfolio_deposit_file("1028")
    return tickers


async def listen_trade_event(tickers: List[str], callback: Callable, stop_event: asyncio.Event = None):
    """
    실시간 체결 데이터 수신

    Parameters
    ----------
    tickers : list of str
        수신할 ticker 목록

    callback : Callable[[str], Future]
        수신한 데이터를 처리할 함수

    stop_event : asyncio.Event
        (Optional) 수신을 중지할 때 set()을 호출할 이벤트 객체
    """
    async with websockets.connect(config.WS_SERVER_URL) as ws:
        for ticker in tickers:
            await ws.send(json.dumps({
                "type": "subscribe",
                "topic": f"tick:{ticker}"
            }))
            await asyncio.sleep(0.01)

        while stop_event is None or not stop_event.is_set():
            data = await _recv_with_timeout(ws)
            if data is not None:
                await callback(data)

            await asyncio.sleep(0.01)


async def _recv_with_timeout(ws: websockets.WebSocketClientProtocol, timeout: int = 1) -> str:
        """ timeout 초 동안 수신을 대기하고 수신이 없으면 None을 반환한다 """
        try:
            message = await asyncio.wait_for(ws.recv(), timeout=timeout)
            return message
        except asyncio.TimeoutError:
            return None