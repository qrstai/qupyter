# 증권사 API key 설정하기

Qupyter platform 에서는 증권사 API key를 암호화하여 안전하게 저장할 수 있는 방법을 제공합니다.
저장 된 API Key는 전략 실행 서버에 전달 되어 API 호출을 위한 token 발행을 위해 사용됩니다.


## 키 등록하기

1. `my-credentials.yaml` 파일을 생성하고 다음과 같이 채워 넣습니다.

```{note}
   파일 이름은 아무 이름이나 자유롭게 사용하시면 됩니다.
```

**이베스트증권**

```yaml
brokerage: ebest
app_key: <your-app-key>
app_secret: <your-app-secret>
environment: live
account_number: 123456789-12
expire_date: 20231231
market_type: stock
```

- brokerage - 증권사 식별자 입니다. `ebest` 로 입력합니다
- app_key, app_secret - API key 입니다. 이베스트 증권 OPEN API 사이트에서 발급받을 수 있습니다.
- environment - 실행환경을 의미합니다. 모의투자의 경우엔 `test`를 실전투자의 경우 `live`로 값을 설정합니다
- account_number - 계좌번호 입니다. 증권사 홈페이지 MTS나 HTS에서 확인이 가능합니다. `(계좌번호)-(상품코드 2자리)` 로 구성되어 있습니다.
- expire_date - 키 만료일자 입니다. 개인 사용자는 발급일로 부터 1년입니다. 2023년 11월 1일에 키를 발급 받으신 경우, 1년 후인 '20241101' 로 지정하시면 됩니다.
- market_type - 현재 증권 거래를 의미하는 `stock` 만 입력 가능합니다.

**한국투자증권**

```yaml
brokerage: kis
app_key: <your-app-key>
app_secret: <your-app-secret>
environment: live
account_number: 12345678-12
expire_date: 20231231
```

- brokerage - 증권사 식별자 입니다. `kis` 로 입력합니다.
- app_key, app_secret - API key 입니다. 한국투자증권 OPEN API 사이트에서 발급받을 수 있습니다.
- environment - 실행환경을 의미합니다. 모의투자의 경우엔 `test`를 실전투자의 경우 `live`로 값을 설정합니다.
- account_number - 계좌번호 입니다. 증권사 홈페이지 MTS나 HTS에서 확인이 가능합니다. `(계좌번호)-(상품코드 2자리)` 로 구성되어 있습니다.
- expire_date - 키 만료일자 입니다. 개인 사용자는 발급일로 부터 1년입니다. 2023년 11월 1일에 키를 발급 받으신 경우, 1년 후인 '20241101' 로 지정하시면 됩니다.

2. Qupyter platform 에서 터미널을 실행합니다.

3. 위에 `my-credentials.yaml` 파일을 생성한 위치에서 아래와 같이 실행합니다.

```bash
qup secret-set ./my-credentials.yaml
```

```{note}
키 등록이 완료되면 `my-credentials.yaml` 파일은 더 이상 필요하지 않으니 삭제하시면 됩니다.
```

## 등록 된 키 확인하기

터미널에서 `qup secret-list`를 실행하여 확인할 수 있습니다.

```text
jovyan@jupyter-qupyter:~$ qup secret-list
BROKERAGE       MARKET_TYPE     ENVIRONMENT EXPIRE_DATE
ebest           stock           test        20240201
ebest           stock           live        20240723
kis             multi           live        20240704
```
