

import os
os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"

from pyworldquant.spot import Spot as Client
username = 'xxxxx@xxxx.com'
password = 'xxxxxx'
# HMAC: pass API key and secret
client = Client(username, password)

settings = {'name': 'USA3000',
              'settings': {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP3000",
                           "truncation": 0.03, "unitHandling": "VERIFY", "pasteurization": "ON", "region": "USA",
                           "language": "FASTEXPR", "decay": 18, "neutralization": "INDUSTRY", "visualization": False}}
regular = 'close'

payload = client.simulate(regular,settings)
print(payload)