from urllib.parse import urlparse


from elvesVsDwarves.mixins.api import Api
from elvesVsDwarves.mixins.utils import Utils
from elvesVsDwarves.mixins.parsers import Parsers
from elvesVsDwarves.mixins.crypto import Crypto


class elvesVsDwarves(Api, Utils, Parsers, Crypto):
    def __init__(self,
                 version:str = '16.6.1',
                 signals:object = None
    ):
        super().__init__()
        self.version = version
        self.signals = signals
