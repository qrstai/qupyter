from datetime import datetime, timedelta
import json
import requests

from qupyter import config


class KIS:
    def __init__(self, test_trade: bool = None, is_corp: bool = False, account_type: str = None, account_number: str = None, product_number: str = None, app_key: str = None, app_secret: str = None, expire_date: str = None):

        self.test_trade = test_trade
        self.account_number = account_number
        self.product_number = product_number

        self._is_corp = is_corp
        self._account_type = account_type
        self._access_token = None
        self._token_valid_until = None
        self._session = None


        if app_key and app_secret:
            self._app_key = app_key
            self._app_secret = app_secret
            self._key_expire_date = expire_date

        elif config.KIS_APP_KEY and config.KIS_APP_SECRET:
            self._app_key = config.KIS_APP_KEY
            self._app_secret = config.KIS_APP_SECRET

        else:
            if test_trade == None:
                raise Exception('test_trade is not defined')
            if account_type == None:
                raise Exception('account_type is not defined')

            self._load_credentials(test_trade, account_type)

        if self._app_key is None or self._app_secret is None:
            raise Exception('API keys are not defined')

        self._check_key_expire_date()


    def _load_credentials(self, test_trade: bool, account_type: str):
        params = {
            'brokerage': 'kis',
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

        self._app_key = data.get('app_key')
        self._app_secret = data.get('app_secret')
        self._key_expire_date = data.get('expire_date')

        self.account_number = data.get('account_number')
        self.product_number = data.get('product_number')

        self._is_corp = data.get('is_corp')

        if self._is_corp:
            self._personal_secret_key = data.get('personal_secret_key')
            self._seq_no = data.get('seq_no')
            self._phone_number = data.get('phone_number')
            self._ip_addr = data.get('ip_addr')


    @property
    def host_url(self):
        if self.test_trade:
            return 'https://openapivts.koreainvestment.com:29443'
        else:
            return 'https://openapi.koreainvestment.com:9443'


    @property
    def session(self):
        if self._session is None or datetime.now() > self._token_valid_until:
            self.refresh_token()

        return self._session


    def refresh_token(self):
        self._session = requests.Session()
        self._session.headers.update(self.make_session_headers())


    def make_session_headers(self):
        if self._access_token is None or datetime.now() > self._token_valid_until:
            self._get_access_token()

        headers = {
            'content-type': 'application/json; charset=utf-8',
            'authorization': f'Bearer {self._access_token}',
            'appkey': self._app_key,
            'appsecret': self._app_secret,
            'custtype': 'B' if self._is_corp else 'P',
        }

        if self._is_corp:
            # 법인 계좌인 경우 필수
            headers.update({
                'personalseckey': self._personal_secret_key,  # 제휴사 회원 관리를 위한 고객식별키
                'seq_no': '01',  # 일련번호
                'phone_number': self._phone_number,  # 핸드폰번호 (숫자만; 하이픈 등 구분값 제거)
                'ip_addr': self._ip_addr,  # 접속 단말 공인 IP 주소
            })

        # 'gt_uid': '',  # 거래고유번호로 사용하므로 거래별로 unique해야 함 <= 호출시에 값을 부여할 것

        return headers


    def _get_access_token(self):
        headers = {
            'content-type': 'application/json',
        }

        body = {
            'grant_type': 'client_credentials',
            'appkey': self._app_key,
            'appsecret': self._app_secret,
        }

        r = requests.post(f"{self.host_url}/oauth2/tokenP", headers=headers, json=body)
        data = r.json()
        print(json.dumps(data, indent=4))

        self._access_token = data.get('access_token')

        if not self._access_token:
            raise Exception('Access token cannot be obtained. Check if API keys are valid.')
        else:
            self._token_valid_until = datetime.now() + timedelta(seconds=data.get('expires_in'))


    def _check_key_expire_date(self):
        if self._key_expire_date != None:
            try:
                key_expire_date = datetime.strptime(self._key_expire_date, '%Y%m%d')
                if key_expire_date - datetime.now() < timedelta(days=14):
                    print(f'KIS API key is too old. Expire date: {self._key_expire_date}')
            except ValueError:
                print(f'key_issue_date is invalid: {self._key_expire_date}')
