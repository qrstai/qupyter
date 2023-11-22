# Change Log

## [0.1.0] - 2023-11-23

한국 투자 증권 API 를 추가했습니다. 증권사 별 제공하는 데이터 서로 상이하여 불가피하게 StockBroker와 StockPosition 에도 변경이 있습니다.

### Added

* 한국투자증권 API 지원 - qupyter.brokerage.kis.KISStockBroker
* StockBroker.get_today_minute_data - 당일 분봉 조회 함수 추가

### Changed

* StockBroker.get_account - 결과 Dict 의 구성 요소 변경
  * 다음 3개의 필드만 정제되어 포함됩니다 — investable_cash, asset_value, total_balance
  * 나머지 증권사 API 결과 데이터는 broker_data 라는 필드에 dict 형태로 그대로 담겨서 반환됩니다.
* StockBroker.get_historical_minute_data 제거
  * 한투의 경우 과거 분봉 데이터를 제공하지 않아, 공통 StockBroker 인터페이스에서 제거되었습니다.
* StockPosition - tax, loan_interest, commission 필드 제거
  * 한투에서 정보를 제공하지 않아 모델에서 제거되었습니다.
* StockOrder - order_method 필드 제거
  * 한투에서 정보를 제공하지 않아 모델에서 제거되었습니다.

### Fixed

* EBestStockBroker.get_positions 응답에서 CMA RP 종목 필터링
* EBestStockBroker.get_pending_orders 응답에 trade_type 잘못된 값 수정
