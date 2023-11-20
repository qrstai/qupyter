# 전략 실행 하기

Qupyter platform 에 전략을 배포하기 전 `qup run` 커맨드를 사용하여 로컬 환경에서 미리 실행해 볼 수 있습니다.

```{note}
배포 전 테스트를 위한 도구로 실행 후 최대 10분간만 동작합니다.
```

## 사용 방법

작성한 전략 소스코드가 있는 위치에서 `qup run <파일 이름>`으로 실행합니다.

```bash
(base) jovyan@jupyter-qupyter:~/5min_breakout$ qup run ./5min_breakout.py
2023-11-02 14:13:16.018177 [EXECUTOR] Call on_initialize hook
New day. 2023-11-02
-       market_open_time: 09:00:00
-  user_market_open_time: 09:05:00
- user_market_close_time: 15:15:00
-      market_close_time: 15:20:00
-               interval: 60 seconds
-           start_margin: 300 seconds
-             end_margin: 300 seconds

2023-11-02 14:13:18.474280 [EXECUTOR] Call trade_func hook
```

## 실행 종료

실행 중 멈추고 싶으면 `Ctrl` + `C` 를 누르시면 됩니다.

```bash
(base) jovyan@jupyter-qupyter:~/5min_breakout$ qup run ./5min_breakout.py
2023-11-02 14:17:34.151357 [EXECUTOR] Call on_initialize hook
New day. 2023-11-02
-       market_open_time: 09:00:00
-  user_market_open_time: 09:05:00
- user_market_close_time: 15:15:00
-      market_close_time: 15:20:00
-               interval: 60 seconds
-           start_margin: 300 seconds
-             end_margin: 300 seconds

# ->> Ctrl + C 누름
^CGot keyboard interrupt. stop loop
(base) jovyan@jupyter-qupyter:~/5min_breakout$
```

