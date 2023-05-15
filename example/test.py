from binance.spot import Spot as Client

import os
os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"


api_key = 'cxJ9PzHcAVrxHpiBFAax5bhcPNPsIqFkzCWk8eqEKT3L49lh49dihcZWuvt0pv5Q'
api_secret = 'S44YHp2HzVrRvpoXT9xUVfPbX4uFnS0rNhitJ866UPhhDMCavf0OVcu9Uuk1WGoO'
# HMAC: pass API key and secret
client = Client(api_key, api_secret)
print(client.account())



