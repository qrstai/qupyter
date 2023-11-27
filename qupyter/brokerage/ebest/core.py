from datetime import datetime, timedelta
import os
import requests

from qupyter import config


class EBest:
    def __init__(self, test_trade: bool = None, account_type: str = None, app_key: str = None, app_secret: str = None, expire_date: str = None):

        if app_key and app_secret:
            self._app_key = app_key
            self._app_secret = app_secret
            self._key_expire_date = expire_date

        elif config.EBEST_APP_KEY and config.EBEST_APP_SECRET:
            self._app_key = config.EBEST_APP_KEY
            self._app_secret = config.EBEST_APP_SECRET

        else:
            if test_trade == None:
                raise Exception('test_trade is not defined.')
            if account_type == None:
                raise Exception('account_type is not defined.')

            self._load_credentials(test_trade, account_type)

        if self._app_key == None or self._app_secret == None:
            raise Exception('API keys are required.')

        self._check_key_expire_date()
        self._session = None


    @property
    def host_url(self):
        return 'https://openapi.ebestsec.co.kr:8080'


    @property
    def session(self):
        if self._session == None or datetime.now() > self._token_valid_until:
            self.refresh_token()

        return self._session


    def refresh_token(self):
        self._get_access_token()

        self._session = requests.Session()
        self._session.headers.update({
            'content-type': 'application/json; charset=UTF-8',
            'authorization': f'Bearer {self._access_token}'
        })


    def get_access_token(self):
        if self._access_token == None or datetime.now() > self._token_valid_until:
            self.refresh_token()

        return self._access_token


    def _load_credentials(self, test_trade: bool, account_type: str):
        params = {
            'brokerage': 'ebest',
            'market_type': account_type,
            'test_trade': test_trade,
        }
        headers = {
            'Authorization': f'Bearer {config.JUPYTERHUB_API_TOKEN}'
        }

        r = requests.get(config.QUPYTER_API_URL + '/brokerage-secret', params=params, headers=headers)

        if r.status_code != 200:
            raise Exception(f"fail to get brokerage credentials from qupyter server: {r.status_code} {r.text}")

        data = r.json()
        self.secret_id = data.get('id')
        self._app_key = data.get('app_key')
        self._app_secret = data.get('app_secret')
        self._key_expire_date = data.get('expire_date')


    def _get_access_token(self):
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

        body = {
            'grant_type': 'client_credentials',
            'appkey': self._app_key,
            'appsecretkey': self._app_secret,
            'scope': 'oob',
        }

        r = requests.post(f"{self.host_url}/oauth2/token", headers=headers, data=body)
        data = r.json()
        self._access_token = data.get('access_token')

        if not self._access_token:
            raise Exception('Access token cannot be obtained. Check if API keys are valid.')
        else:
            expired_at = datetime.now() + timedelta(seconds=data.get('expires_in'))
            # 이베스트는 expires_in 값과 관계 없이 매일 오전 7시에 키를 초기화 시킨다.
            # https://openapi.ebestsec.co.kr/howto-use - 03.접근토큰 발급 탭 참고
            forced_expire_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)

            self._token_valid_until = min(expired_at, forced_expire_time)


    def _check_key_expire_date(self):
        if self._key_expire_date != None:
            try:
                key_expire_date = datetime.strptime(self._key_expire_date, '%Y%m%d')
                if key_expire_date - datetime.now() < timedelta(days=14):
                    print(f'EBest API key is too old. Expire date: {self._key_expire_date}')
            except ValueError:
                print(f'key_issue_date is invalid: {self._key_expire_date}')