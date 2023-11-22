import os, dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


EBEST_APP_KEY = os.getenv("EBEST_APP_KEY")

EBEST_APP_SECRET = os.getenv("EBEST_APP_SECRET")

KIS_APP_KEY = os.getenv('KIS_APP_KEY')

KIS_APP_SECRET = os.getenv('KIS_APP_SECRET')

JUPYTERHUB_API_TOKEN = os.getenv('JUPYTERHUB_API_TOKEN')

QUPYTER_API_URL = os.getenv('QUPYTER_API_URL', 'http://qupyter-nodeport.qupyter.svc.cluster.local/api')

WS_SERVER_URL = os.getenv("WS_SERVER_URL", "ws://ws-server-nodeport.qupyter.svc.cluster.local/ws")
""" Qupyter 실시간 데이터 수신 서버 주소 """