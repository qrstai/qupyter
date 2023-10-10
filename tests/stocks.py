import unittest, asyncio
from qupyter.stocks import listen_trade_event

class StocksTests(unittest.IsolatedAsyncioTestCase):
    async def test_listen_trade_event(self):
        tickers = ['035720', '005930']

        stop_event = asyncio.Event()
        task = asyncio.create_task(listen_trade_event(tickers, lambda x: print(x), stop_event))

        await asyncio.sleep(5)
        stop_event.set()

        await task
        print('done')

