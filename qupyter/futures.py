import pandas as pd
import boto3

def get_ticker_list():
    return ['10100', '10500']

def get_trade_event(ticker: str, date: str) -> pd.DataFrame:
    client = boto3.client('s3')

    key = f"{ticker}/{date}.csv"

    res = client.get_object(Bucket='qrst-kospi200-futures-data', Key=key)
    df = pd.read_csv(res['Body'])

    client.close()

    return df
