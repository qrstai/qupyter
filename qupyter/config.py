import os, dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


WS_SERVER_URL = os.getenv("WS_SERVER_URL", "ws://ws-server-nodeport.qupyter.svc.cluster.local/ws")
""" Qupyter 실시간 데이터 수신 서버 주소 """

