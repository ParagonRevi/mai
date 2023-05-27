import base64
import hashlib
import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Crypto:
    def __init__(self):
        super().__init__()
        self.setCypherParams()

    def setCypherParams(self):
        tmpDESkey = "3sc3RLrpd17".encode('ascii')
        self.key = hashlib.sha256(tmpDESkey).digest()
        self.bs = 16
        self.iv = bytes(16)

    def cypherInit(self):
        self.cypher = AES.new(self.key, AES.MODE_CBC, self.iv)

    def encryptRequest(self, data):
        self.cypherInit()
        self.genGameKey(data)
        base64Data = base64.b64encode(urllib.parse.urlencode(data).encode('ascii'))
        self.sig = self.genSignature(base64Data)
        dataToEncode = self._pad(base64Data.decode())
        output = self.cypher.encrypt(dataToEncode.encode())
        encData = base64.b64encode(output)
        return encData

    def decryptResponse(self, enc):
        self.cypherInit()
        enc = base64.b64decode(enc)
        return self._unpad(self.cypher.decrypt(enc))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def genGameKey(self, reqData):
        lowerReqData = {k.lower(): v.lower() for k, v in reqData.items()}
        sortedReqData = {key: value for key, value in sorted(lowerReqData.items())}
        queryData = urllib.parse.unquote(urllib.parse.urlencode(sortedReqData)) + "20f6e2f8769fb66faf7e7daccf9d342e"
        reqData['gameKey'] = hashlib.md5(queryData.encode()).hexdigest()

    def genSignature(self, base64Data):
        base64Data = base64Data.decode('ascii')
        dataStr = base64Data.encode() + "04D64395-GA88-5E11-88EA-9D5E217C3FDC".encode()
        return hashlib.md5(dataStr).hexdigest()

    def getSHA(self, input):
        md = hashlib.sha256()
        md.update(input.encode('ascii'))
        return md.digest()