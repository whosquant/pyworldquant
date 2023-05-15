from pyworldquant.api import API

class Spot(API):
    def __init__(self, api_key=None, api_secret=None, **kwargs):
        if "base_url" not in kwargs:
            kwargs["base_url"] = "https://api.worldquantbrain.com"
        super().__init__(api_key, api_secret, **kwargs)

    from pyworldquant.spot._simulate import login
    from pyworldquant.spot._simulate import simulate
    from pyworldquant.spot._simulate import simulate1
    from pyworldquant.spot._simulate import simulate2
    from pyworldquant.spot._simulate import brief_performance