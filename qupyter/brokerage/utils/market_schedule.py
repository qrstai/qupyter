from dataclasses import dataclass
import datetime
from typing import Optional

import requests

from qupyter import config

@dataclass
class MarketSchedule:
    """ 장 운영 정보

    :param date: 날짜
    :type date: datetime.date
    :param market_type: 시장 구분
    :type market_type: str
    :param is_full_day_closed: 장 운영 여부
    :type is_full_day_closed: bool
    :param open_time: 장 시작 시간
    :type open_time: Optional[datetime.time]
    :param close_time: 장 종료 시간
    :type close_time: Optional[datetime.time]
    :param reason: 장 운영 여부가 False인 경우, 장 운영이 중단된 이유
    :type reason: Optional[str]
    """
    date: datetime.date
    market_type: str
    is_full_day_closed: bool
    open_time: Optional[datetime.time]
    close_time: Optional[datetime.time]
    reason: Optional[str]


def get_market_schedule(date: datetime.date = datetime.datetime.today().date()) -> MarketSchedule:
    """
    주어진 날짜에 대한 장 운영 정보를 반환합니다.

    :param date: 조회할 날짜
    :date type: datetime.date
    :return: 장 운영 정보
    :rtype: MarketSchedule
    """

    r = requests.get(config.QUPYTER_API_URL + '/market-schedule', params={'date': date.strftime('%Y%m%d')})
    r.raise_for_status()

    data = r.json()

    open_time = data.get('open_time')
    if open_time:
        open_time = datetime.datetime.strptime(open_time, '%H:%M').time()

    close_time = data.get('close_time')
    if close_time:
        close_time = datetime.datetime.strptime(close_time, '%H:%M').time()


    return MarketSchedule(
        date=datetime.datetime.strptime(data['date'], '%Y%m%d').date(),
        market_type=data['market_type'],
        is_full_day_closed=data['is_full_day_closed'],
        open_time=open_time,
        close_time=close_time,
        reason=data.get('reason'),
    )



