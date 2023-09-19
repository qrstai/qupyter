import pandas as pd
import boto3

def get_ticker_list():
    """
    Ticker 조회

    Ticker를 리스트로 반환합니다.

    Returns
    -------
    list of str
        선물 Ticker 목록.
    """
    return ['10100', '10500']


def get_trade_event(ticker: str, date: str) -> pd.DataFrame:
    """
    거래 이벤트 조회

    지정한 Ticker와 날짜에 해당하는 거래 이벤트를 조회합니다.

    Parameters
    ----------
    ticker : str
        Ticker symbol.

    date : str
        Date in YYYYMMDD format.

    Returns
    -------
    pandas.DataFrame
        거래 이벤트 데이터
    """
    client = boto3.client('s3')

    key = f"{ticker}/{date}.csv"

    res = client.get_object(Bucket='qrst-kospi200-futures-data', Key=key)
    df = pd.read_csv(res['Body'])

    client.close()

    return df
