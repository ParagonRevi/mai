import os
import requests
import base64
import re
import json
import time
from urllib3.exceptions import MaxRetryError, NewConnectionError
from socket import gaierror
class Api:
    def __init__(self):
        imei = self.generate_imei()
        mobile_id = self.generateMobileid(imei)
        device_id = self.generate_device_id()
        manufacturer = self.generate_manufacturer()
        model = self.generate_model(manufacturer)
        self.session = requests.session()
        self.session.verify = False
        self.baseUrl = "http://www199.evdgame.com/ajax/"
        self.mobile_id = str(mobile_id)
        self.imei = str(imei)
        self.device_id = str(device_id)
        self.manufacturer = str(manufacturer)
        self.model = str(model)
        super().__init__()

    def auth(self, login, password):
        self.login = login
        self.password = password
        authParams = {
         'act': 'login',
         'email': login,
         'password': password,
         'udid': '4304d0cf9b054618',
         'm_iso': 'Linux', 
         'm_manufacturer': 'samsung',
         'm_model': 'SM-N975F',
         'm_language': 'en',
         'lang': 'en',
         'naid': 'QzDoTaGsXmT9veHe',
         'gcuid': '', 
         'gcunick': '',
         'mobileid': self.mobile_id,
         'platformid': '203',
         'become_user_id': '',
         'become_password': '', 
         'debug': '0',
         'gver': '16.6.1',
         'gameSlot': '51', 
         'race': '1',
         'gameid': '32',
         'm_osVer': '11',
         'newlang': 'en',
         'gameNumber': self.genTimestamp(),
         }
        authData = self.makeRequest('kabamId.php',authParams).json()
        self.authDataParser(authData)

    def signup(self):
        data = {
         'worldid': '199',
         'udid': 'cff5d8e9e17588f8',
         'unityDevId': '615854dddcb55109054c312eef107d41',
         'm_mac': '0e:ac:de:a7:96:1c',
         'm_iso': 'Linux',
         'm_manufacturer': self.manufacturer,
         'm_model': self.model,
         'm_language': 'en',
         'wifi': '1',
         'carrierName': 'Megafon',
         'mnc': '0',
         'mcc': '0',
         'openUDID': 'WIFIMAC:0e:ac:de:a7:96:1c',
         'client_lang': 'en',
         'm_deviceIFA': 'UNKNOWN',
         'm_deviceIFV': 'UNKNOWN',
         'limit_ad': 'UNKNOWN',
         'device_id': self.device_id,
         'os': 'Android',
         'OSVersion': '11',
         'app_version': '16.6.1',
         'm_deviceADID': '00000000-0000-0000-0000-000000000000',
         'u4': 'a6cd0cde119e2a1858377299f3a6839c',
         'imei': self.imei,
         'kabam_id': self.kabamId,
         'access_token': self.accessToken,
         'naid': self.naid,
         'gcuid': '',
         'gcunick': '',
         'mobileid': self.mobile_id,
         'platformid': '203',
         'become_user_id': '',
         'become_password': '',
         'debug': '0',
         'gver': '16.6.1',
         'gameSlot': '51',
         'race': '1',
         'gameid': '32',
         'm_osVer': '11',
         'newlang': 'en',
         'gameNumber': self.genTimestamp(),
         }
        signupEncData = self.makeRequest('signup.php', data)
        signupData = self.decryptResponse(signupEncData.text)
        jsonData = json.loads(signupData.decode('ascii'))
        if 'naid' in jsonData:
            self.naid = jsonData['naid']
        if 'mobileid' in jsonData:
            self.mobile_id = jsonData['mobileid']
        time.sleep(1)

        data = {
        'tvuid': self.tvuid,
        'lang': 'en',
        'initTime': '9350',
        'deviceModel': self.manufacturer + '%' + self.model,
        'systemMemorySize': '1999',
        'graphicsMemorySize': '512',
        'processorCount': '1',
        'kabam_id': self.kabamId,
        'access_token': self.accessToken,
        'naid': self.naid,
        'gcuid': '',
        'gcunick': '',
        'mobileid': self.mobile_id,
        'platformid': '203',
        'become_user_id': '',
        'become_password': '',
        'debug': '0',
        'gver': '16.6.1',
        'gameSlot': '15',
        'race': '1',
        'gameid': '32',
        'm_osVer': '11',
        'newlang': 'en',
        'gameNumber': self.genTimestamp(),
        }
        getSeedEncData = self.makeRequest('getSeed.php', data)
        getSeedData = self.decryptResponse(getSeedEncData.text)
        jsonData = json.loads(getSeedData.decode('ascii'))
        jsonData = {'seed': jsonData['seed']}
        chestIds, offerIds, limits, cityIds, bid_for_gates, kid_for_gates, totalGems, lvl = self.getSeedParser(getSeedData)
        self.chestIds = chestIds
        self.offerIds = offerIds
        self.limits = limits
        self.totalGems = int(totalGems)
        self.level = lvl
        self.cityIds = cityIds
        self.bid_for_gates = bid_for_gates
        self.kid_for_gates = kid_for_gates
        data = {
            'lang': 'en',
            'kabam_id': self.kabamId,
            'access_token': self.accessToken,
            'naid': self.naid,
            'gcuid': '',
            'gcunick': '',
            'mobileid': self.mobile_id,
            'platformid': '203',
            'become_user_id': '',
            'become_password': '',
            'debug': '0',
            'gver': '16.6.1',
            'gameSlot': '15',
            'race': '1',
            'gameid': '32',
            'm_osVer': '11',
            'newlang': 'en',
            'gameNumber': self.genTimestamp(),
        }
        showShopEncData = self.makeRequest('showShop.php', data)
        showShopData = json.loads(showShopEncData.text)
        i2115_value = int(showShopData['data']['inventory'].get('i2115', 0))
        i2116_value = int(showShopData['data']['inventory'].get('i2116', 0))
        inventoryMith = (i2116_value * 100) + (i2115_value * 50)
        totalMith = int(self.totalGems) + int(inventoryMith)
        self.totalMith = totalMith
        print("Total Mith for {}: {}".format(self.login, totalMith))
        self.saveMithData()
        #data = {
        #    'requestToAllianceId': '5290',
        #    'message': 'hi',
        #    'subject': 'hi',
        #    'kabam_id': self.kabamId,
        #    'access_token': self.accessToken,
        #    'naid': self.naid,
        #    'gcuid': '',
        #    'gcunick': '',
        #    'mobileid': self.mobile_id,
        #    'platformid': '203',
        #    'become_user_id': '',
        #    'become_password': '',
        #    'debug': '0',
        #    'gver': '16.6.1',
        #    'gameSlot': '150',
        #    'race': '1',
        #    'gameid': '32',
        #    'm_osVer': '11',
        #    'newlang': 'en',
        #    'gameNumber': self.genTimestamp(),
        #}
        #allianceLeaveEncData = self.makeRequest('allianceJoinRequest.php', data)

    def offer(self):
        if not self.chestIds and not self.offerIds:
            print('Free offer not found or claimed, skipping...')
        else:
            for i in range(len(self.chestIds)):
                data = {'chestId': str(self.chestIds[i]),
                        'offerId': str(self.offerIds[i]),
                        'kabam_id': self.kabamId,
                        'access_token': self.accessToken,
                        'naid': self.naid,
                        'gcuid': '',
                        'gcunick': '',
                        'mobileid': self.mobile_id,
                        'platformid': '203',
                        'become_user_id': '',
                        'become_password': '',
                        'debug': '0',
                        'gver': '16.6.1',
                        'gameSlot': '82',
                        'race': '1',
                        'gameid': '32',
                        'm_osVer': '11',
                        'newlang': 'en',
                        'gameNumber': self.genTimestamp(),
                        }
                for j in range(int(self.limits[i])):
                    time.sleep(1)
                    claimOfferData = self.makeRequest('claimOffer.php', data)
                    time.sleep(1)
            print(f'Free offer claimed')

    def closeGates(self):
        for i, cityId in enumerate(self.cityIds):
            data = {
                'cid': cityId,
                'state': '0',
                'tax': '0',
                'kid': self.kid_for_gates,
                'bid': self.bid_for_gates.get(cityId),
                'm_mac': '0e:ac:de:a7:96:1c',
                'm_iso': 'Linux',
                'm_model': 'self.model',
                'kabam_id': self.kabamId,
                'access_token': self.accessToken,
                'naid': self.naid,
                'gcuid': '',
                'gcunick': '',
                'mobileid': self.mobile_id,
                'platformid': '203',
                'become_user_id': '',
                'become_password': '',
                'debug': '0',
                'gver': '16.6.1',
                'gameSlot': '585',
                'race': '1',
                'gameid': '32',
                'm_osVer': '11',
                'newlang': 'en',
                'gameNumber': self.genTimestamp(),
            }
            openGatesData = self.makeRequest('gateSwitch.php', data)
            time.sleep(2)


    #    self.cid = cid
    #    self.mid = mid
    #    self.kid = kid
    #    time.sleep(2)

    #    def bossKill():
    #        def bossList(s):
    #            while Tene:
    #                data = {
    #                    'type': 'bossList',
    #                    'kabam_id': self.kabamId,
    #                    'access_token': self.accessToken,
    #                    'naid': self.naid,
    #                    'gcuid': '',
    #                    'gcunick': '',
    #                    'mobileid': self.mobile_id,
    #                    'platformid': '203',
    #                    'become_user_id': '',
    #                    'become_password': '',
    #                    'debug': '0',
    #                    'gver': '16.6.1',
    #                    'gameSlot': '51',
    #                    'race': '1',
    #                    'gameid': '32',
    #                    'm_osVer': '11',
    #                    'newlang': 'en',
    #                    'gameNumber': self.genTimestamp(),
    #                }
    #                bossListEncData = self.makeRequest('allianceBoss.php', data)
    #                bossListData = self.decryptResponse(bossListEncData.text)
    #                jsonData = json.loads(bossListData.decode('ascii'))
    #                boss_meets_criteria = False
    #                for boss in jsonData['data']:
    #                    if (boss['level'] == "250" and boss['alive_time'] != 0 and boss.get('activeAtkTime', 0) == 0 and
    #                            boss[
    #                                'killer'] == ""):
    #                        boss_meets_criteria = True
    #                        break
    #                if boss_meets_criteria:
    #                    break
    #                else:
    #                    time.sleep(3)
    #    data = {
    #            'cid': self.cid,
    #            'type': '11',
    #            'u101': '5000',
    #            'alRequestId': '0',
    #            'mapId': '500101',
    #            'levelId': '500101001',
    #            'mid': self.mid,
    #            'kid': self.kid,
    #            'chapterId': '500',
    #            'u121': '95000',
    #            'lang': 'en',
    #            'kabam_id': self.kabamId,
    #            'access_token': self.accessToken,
    #            'naid': self.naid,
    #            'gcuid': '',
    #            'gcunick': '',
    #            'mobileid': self.mobile_id,
    #            'platformid': '203',
    #            'become_user_id': '',
    #            'become_password': '',
    #            'debug': '0',
    #            'gver': '16.6.1',
    #            'gameSlot': '51',
    #            'race': '1',
    #            'gameid': '32',
    #            'm_osVer': '11',
    #            'newlang': 'en',
    #            'gameNumber': self.genTimestamp(),
    #        }
    #    bossKillData = self.makeRequest('marchAlliance.php', data)
    #    time.sleep(2)
    def bubble(self):
        data = {
             'iid': '901',
             'kabam_id': self.kabamId,
             'access_token': self.accessToken,
             'naid': self.naid,
             'gcuid': '',
             'gcunick': '',
             'mobileid': self.mobile_id,
             'platformid': '203',
             'become_user_id': '',
             'become_password': '',
             'debug': '0',
             'gver': '16.6.1',
             'gameSlot': '110',
             'race': '1',
             'gameid': '32',
             'm_osVer': '11',
             'newlang': 'en',
             'gameNumber': self.genTimestamp(),
            }
        bubbleData = self.makeRequest('doveOut.php', data)

    def claimCalendarReward(self):
        self.getCalendarData()
        self.claimDays()
        if self.day == 28:
            if len(self.chests):
                print('Getting calendar chests...')
                self.claimChests()
            else:
                print(f'All chests claimed')

    def getCalendarData(self):
        for i in range(3):
            data = {'lang': 'en',
                    'action': 'getCalendar',
                    'kabam_id': self.kabamId,
                    'access_token': self.accessToken,
                    'naid': self.naid,
                    'gcuid': '',
                    'gcunick': '',
                    'mobileid': self.mobile_id,
                    'platformid': '203',
                    'become_user_id': '',
                    'become_password': '',
                    'debug': '0',
                    'gver': '16.6.1',
                    'gameSlot': '32',
                    'race': '1',
                    'gameid': '32',
                    'm_osVer': '11',
                    'newlang': 'en',
                    'gameNumber': self.genTimestamp(),
                    }
            calendarEncData = self.makeRequest('signUpCalendar.php', data)
            calendarData = self.decryptResponse(calendarEncData.text)
            jsonData = json.loads(calendarData.decode('ascii'))
            if not jsonData['ok']:
                time.sleep(1)
            else:
                self.calendarParser(jsonData)
                return
        raise Exception("Error in getting calendar data, tried 3 times")
    
    def claimDays(self):
            data = {'lang': 'en',
                              'action': 'signupDaily',
                              'year': self.year,
                              'month': self.month,
                              'day': self.day,
                              'kabam_id': self.kabamId,
                              'access_token': self.accessToken,
                              'naid': self.naid,
                              'gcuid': '',
                              'gcunick': '',
                              'mobileid': self.mobile_id,
                              'platformid': '203',
                              'become_user_id': '',
                              'become_password': '',
                              'debug': '0',
                              'gver': '16.6.1',
                              'gameSlot': '32',
                              'race': '1',
                              'gameid': '32',
                              'm_osVer': '11',
                              'newlang': 'en',
                              'gameNumber': self.genTimestamp(),
                              }
            dailyClaimEncData = self.makeRequest('signUpCalendar.php',data)
            dailyClaimData = self.decryptResponse(dailyClaimEncData.text)
            time.sleep(1)

    def claimChests(self):
        for chest in self.chests:
            print(f'Getting chests for day : {chest}')
            data = {'lang': 'en',
                    'action': 'claimChest',
                    'chestSignedUpTotal': chest,
                    'kabam_id': self.kabamId,
                    'access_token': self.accessToken,
                    'naid': self.naid,
                    'gcuid': '',
                    'gcunick': '',
                    'mobileid': self.mobile_id,
                    'platformid': '203',
                    'become_user_id': '',
                    'become_password': '',
                    'debug': '0',
                    'gver': '16.6.1',
                    'gameSlot': '36',
                    'race': '1',
                    'gameid': '32',
                    'm_osVer': '11',
                    'newlang': 'en',
                    'gameNumber': self.genTimestamp(),
                    }
            chestEncData = self.makeRequest('signUpCalendar.php', data)
            chestData = self.decryptResponse(chestEncData.text)
            time.sleep(3)

    def claimEventReward(self):
        data = {'type': 'list',
                'lang': 'en',
                'kabam_id': self.kabamId,
                'access_token': self.accessToken,
                'naid': self.naid,
                'gcuid': '',
                'gcunick': '',
                'mobileid': self.mobile_id,
                'platformid': '203',
                'become_user_id': '',
                'become_password': '',
                'debug': '0',
                'gver': '16.6.1',
                'gameSlot': '93',
                'race': '1',
                'gameid': '32',
                'm_osVer': '11',
                'newlang': 'en',
                'gameNumber': self.genTimestamp(),
                }
        eventCenterEncData = self.makeRequest('eventcenter.php', data)
        eventCenterData = self.decryptResponse(eventCenterEncData.text)
        eventIds, spendEventIds = self.eventParser(eventCenterData)
        print('Getting event rewards...')
        for id in eventIds:
            data = {'type': 'claim',
                    'eventId': id,
                    'kabam_id': self.kabamId,
                    'access_token': self.accessToken,
                    'naid': self.naid,
                    'gcuid': '',
                    'gcunick': '',
                    'mobileid': self.mobile_id,
                    'platformid': '203',
                    'become_user_id': '',
                    'become_password': '',
                    'debug': '0',
                    'gver': '16.6.1',
                    'gameSlot': '96',
                    'race': '1',
                    'gameid': '32',
                    'm_osVer': '11',
                    'newlang': 'en',
                    'gameNumber': self.genTimestamp(),
                    }
            eventEncClaim = self.makeRequest('eventcenter.php', data)
            eventClaim = self.decryptResponse(eventEncClaim.text)
            time.sleep(1)
        if not len(eventIds):
            print('All the event rewards allready claimed, skipping...')
        else:
            print(f'All event rewards claimed')
        print('Getting spend event rewards...')
        for id in spendEventIds:
            for rewardIndex in range(3):
                data = {'type': 'claim',
                        'eventId': id,
                        'rewardIndex': str(rewardIndex),
                        'kabam_id': self.kabamId,
                        'access_token': self.accessToken,
                        'naid': self.naid,
                        'gcuid': '',
                        'gcunick': '',
                        'mobileid': self.mobile_id,
                        'platformid': '203',
                        'become_user_id': '',
                        'become_password': '',
                        'debug': '0',
                        'gver': '16.6.1',
                        'gameSlot': '96',
                        'race': '1',
                        'gameid': '32',
                        'm_osVer': '11',
                        'newlang': 'en',
                        'gameNumber': self.genTimestamp(),
                        }
                eventEncClaim = self.makeRequest('eventcenter.php', data)
                eventClaim = self.decryptResponse(eventEncClaim.text)
                time.sleep(1)

        if not len(spendEventIds):
            print('Alliance Mirlith Spend event rewards already claimed, skipping...')
        else:
            print(f'Alliance Mirlith Spend event rewards claimed')




    def makeRequest(self,method,data):
        reqData = {
            'data':self.encryptRequest(data),
            'vcs':'16.6.1',
            'signatrue': self.sig

        }

        try:
            response = self.session.post(f'{self.baseUrl}{method}', headers=self.baseHeaders, data=reqData)
            return response
        except json.decoder.JSONDecodeError:
            raise Exception("Error in decoding response json")
        except (requests.exceptions.ProxyError, MaxRetryError, NewConnectionError, gaierror):
            raise Exception("Lost connection to server, Inavild proxy")

