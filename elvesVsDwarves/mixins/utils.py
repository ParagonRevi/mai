from lxml import etree
import platform
import string
import os
import hashlib
import random
import time
import os.path
from _datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Utils:
    def __init__(self):
        super().__init__()
        self.genHeaders()

    def genHeaders(self):
        self.baseHeaders = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Unity-Version': '2017.4.40c1',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0.0; SM-G965N Build/QP1A.190711.020)',
            'Host': 'www199.evdgame.com',
            'Connection': 'close',
        }

    def generate_manufacturer(self):
        manufacturers = ['samsung']
        return random.choice(manufacturers)

    def generate_model(self, manufacturer):
        models = {
            'samsung': ['SM-G960F', 'SM-G965F', 'SM-G970F', 'SM-G973F', 'SM-G975F', 'SM-G980F',
                        'SM-G985F', 'SM-G986F', 'SM-G988F', 'SM-G991B', 'SM-G996B', 'SM-G998B',
                        'SM-G892A', 'SM-G892U', 'SM-G930F', 'SM-G935F', 'SM-G950F', 'SM-G955F',
                        'SM-G960U', 'SM-G965U', 'SM-G970U', 'SM-G973U', 'SM-G975U', 'SM-G981U',
                        'SM-G986U', 'SM-G988U', 'SM-G991U', 'SM-G996U','SM-A325F', 'SM-A325U',
                        'SM-G991B', 'SM-G996B', 'SM-G998B', 'SM-G980F', 'SM-G975U', 'SM-G998U'
                        'SM-G985F', 'SM-G988F', 'SM-A715F', 'SM-A715U', 'SM-A525F', 'SM-A525U',
                        'SM-N970F', 'SM-N975F', 'SM-N976F', 'SM-N770F', 'SM-N971F', 'SM-N976B',
                        'SM-N980F', 'SM-N985F', 'SM-N986B', 'SM-N986F', 'SM-A015F', 'SM-A105F',
                        'SM-A107F', 'SM-A202F', 'SM-A205F', 'SM-A207F', 'SM-A905F', 'SM-A907F',
                        'SM-A215F', 'SM-A217F', 'SM-A225F', 'SM-A227F', 'SM-A305F', 'SM-A307F',
                        'SM-A315F', 'SM-A317F', 'SM-A325F', 'SM-A327F', 'SM-A405F', 'SM-A407F',
                        'SM-A415F', 'SM-A417F', 'SM-A425F', 'SM-A427F', 'SM-A505F', 'SM-A507F',
                        'SM-A515F', 'SM-A517F', 'SM-A525F', 'SM-A527F', 'SM-A605F', 'SM-A607F',
                        'SM-A705F', 'SM-A707F', 'SM-A715F', 'SM-A717F', 'SM-A725F', 'SM-A727F',
                        'SM-A805F', 'SM-A807F', 'SM-A815F', 'SM-A817F', 'SM-A825F', 'SM-A827F',
                        'SM-A905F', 'SM-A907F', 'SM-G960F', 'SM-G965F', 'SM-G970F', 'SM-G973F',
                        'SM-G985F', 'SM-G986F', 'SM-G988F', 'SM-G991B', 'SM-G996B', 'SM-G998B',
                        'SM-G892A', 'SM-G892U', 'SM-G930F', 'SM-G935F', 'SM-G950F', 'SM-G955F',
                        'SM-G960U', 'SM-G965U', 'SM-G970U', 'SM-G973U'],
        }
        return random.choice(models[manufacturer])

    def generate_imei(self):
        """
        The function generates a random 15-digit number
        """
        return ''.join(str(random.randint(0, 9)) for _ in range(15))

    def generateMobileid(self, imei):
        hash_value = hashlib.md5(imei.encode('utf-8')).hexdigest()
        mobile_id = hash_value[:32]
        return mobile_id

    def generate_device_id(self):
        device_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return device_id

    def saveMithData(self):
        # Определение текущей операционной системы
        current_platform = platform.system()

        # Определите путь к папке документов в зависимости от операционной системы
        if current_platform == 'Windows':
            documents_path = os.path.expanduser("~/Documents")
        elif current_platform == 'Android':
            documents_path = os.path.expanduser("~/storage/emulated/0/Documents")
        else:
            raise NotImplementedError("Unsupported platform: " + current_platform)

        # Создайте папку EVDBot, если она не существует
        evdbot_path = os.path.join(documents_path, "EVDBot")
        if not os.path.exists(evdbot_path):
            os.makedirs(evdbot_path)
        if self.allianceName == 'Time Capsule':
            xml_file_path = os.path.join(evdbot_path, "TimeCapsule.xml")
        elif self.allianceName == 'Majesty':
            xml_file_path = os.path.join(evdbot_path, "Majesty.xml")
        elif self.totalMith > 5000:
            xml_file_path = os.path.join(evdbot_path, "MithOver5k.xml")
        elif self.totalMith > 3000:
            xml_file_path = os.path.join(evdbot_path, "Mith4k.xml")
        else:
            xml_file_path = os.path.join(evdbot_path, "Mith.xml")

        # Создайте или откройте файл XML
        if os.path.isfile(xml_file_path):
            root = etree.parse(xml_file_path).getroot()
        else:
            root = etree.Element('root')

        # Проверьте, есть ли элемент с self.login в XML-файле
        for user in root.findall('user'):
            if user.find('login').text == self.login:
                # Обновить значения self.level и self.totalMith
                user.find('nickname').text = str(self.nickname)
                user.find('level').text = str(self.level)
                user.find('allianceName').text = str(self.allianceName)
                user.find('totalMith').text = str(self.totalMith)
                break
        else:
            # Добавить новый элемент в конец XML-файла
            user = etree.SubElement(root, 'user')
            login = etree.SubElement(user, 'login')
            login.text = self.login
            nickname = etree.SubElement(user, 'nickname')
            nickname.text = self.nickname
            level = etree.SubElement(user, 'level')
            level.text = str(self.level)
            allianceName = etree.SubElement(user, 'allianceName')
            allianceName.text = str(self.allianceName)
            totalMith = etree.SubElement(user, 'totalMith')
            totalMith.text = str(self.totalMith)

        # Записать XML-файл на диск
        et = etree.ElementTree(root)
        et.write(xml_file_path, encoding='UTF-8', pretty_print=True)

    def setTokens(self,authData):
        self.accessToken = authData.get('access_token',None)
        self.kabamId =  authData.get('kabam_id',None)
        self.naid =  authData.get('naid',None)
        self.tvuid = authData.get('tvuid',None)
        self.authCode = authData.get('code', None)
        
    def genTimestamp(self):
        millisecond = datetime.now()
        timestamp = int(time.mktime(millisecond.timetuple()))
        return str(timestamp)

    def saveErrorData(self):
        # Определение текущей операционной системы
        current_platform = platform.system()

        # Определение пути к файлу в зависимости от операционной системы
        if current_platform == 'Windows':
            file_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'errorAccs.txt')
        elif current_platform == 'Android':
            file_path = os.path.join('~/storage/emulated/0/Documents/EVDBot', 'errorAccs.txt')
        else:
            raise NotImplementedError("Unsupported platform: " + current_platform)

        # Запись данных в файл
        with open(file_path, 'a') as file:
            file.write(f'{self.login}:{self.password}\n')
            
    #def writeOutput(self, message):
    #    self.signals.outputWrite.emit(f'{self.login}: {message}')



