# 증권사 API key 설정하기

Qupyter platform 에서는 증권사 API key를 암호화하여 안전하게 저장할 수 있는 방법을 제공합니다.
저장 된 API Key는 전략 실행 서버에 전달 되어 API 호출을 위한 token 발행을 위해 사용됩니다.


## 키 등록하기

1. `my-credentials.yaml` 파일을 생성하고 다음과 같이 채워 넣습니다.

```yaml
app_key: <your-app-key>
app_secret: <your-app-secret>
environment: live
issue_date: 20231018
market_type: stock
```

- app_key, app_secret - API key 입니다. 이베스트 증권 OPEN API 사이트에서 발급받을 수 있습니다.
- environment - 실행환경을 의미합니다. 모의투자의 경우엔 `test`를 실전투자의 경우 `live`로 값을 설정합니다
- valid_until - 키 만료일자 입니다. 증권사에서 키 발행 시 나타난 값을 입력합니다.
- market_type - 현재 증권 거래를 의미하는 `stock` 만 입력 가능합니다.

2. Qupyter platform 에서 터미널을 실행합니다.

3. 위에 `my-credentials.yaml` 파일을 생성한 위치에서 아래와 같이 실행합니다.

```bash
qup secret-set ./my-credentials.yaml
```

## 등록 된 키 확인하기

터미널에서 `qup secret-list`를 실행하여 확인할 수 있습니다.

```
jovyan@jupyter-kghoon:~$ qup secret-list
MARKET_TYPE     ENVIRONMENT ISSUE_DATE
stock           live        20230730
```