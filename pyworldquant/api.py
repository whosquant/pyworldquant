import json
from json import JSONDecodeError
import logging
import requests
from .__version__ import __version__


# from binance.error import ClientError, ServerError
# from binance.lib.utils import get_timestamp
# from binance.lib.utils import cleanNoneValue
# from binance.lib.utils import encoded_string
# from binance.lib.utils import check_required_parameter
# from binance.lib.authentication import hmac_hashing, rsa_signature

class API(object):
    """API base class
    Keyword Args:
        base_url (str, optional): the API base url, useful to switch to testnet, etc. By default it's https://api.worldquantbrain.com
        timeout (int, optional): the time waiting for server response, number of seconds. https://docs.python-requests.org/en/master/user/advanced/#timeouts
        show_limit_usage (bool, optional): whether return limit usage(requests and/or orders). By default, it's False
        show_header (bool, optional): whether return the whole response header. By default, it's False
    """

    def __init__(
        self,
        username=None,
        password=None,
        base_url=None,
        timeout=None,
    ):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.timeout = timeout
        self.show_limit_usage = False
        self.show_header = False
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "pyworldquant/" + __version__,
            }
        )
        self._logger = logging.getLogger(__name__)
        self.login()
        return



