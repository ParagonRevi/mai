import json


class Parsers:
    def __init__(self):
        super().__init__()

    def authDataParser(self,authData):
        if 'error_description' in authData and authData['error_description'] == 'Неправильный логин или пароль':
            raise WrongAuthCredientals(f"Login or password is incorrect\nLogin : {self.username}\nPassword : {self.password}\n")
        if 'access_token' in authData:
            self.setTokens(authData)
            print('Authorized successfully')
        else:
            print('Error in auth')
            print(authData)

    def calendarParser(self,jsonData):
        signUpCalendar = jsonData['signUpCalendar']
        daysDetails = signUpCalendar['signData']['daysDetail']
        self.totalDays = len(daysDetails)
        self.existingChests = [k.strip('i') for k,v in signUpCalendar['chestsList'].items()]
        self.claimedChests = signUpCalendar['signData']['claimChestDetail']
        self.chests = [chest for chest in self.existingChests if int(chest) not in self.claimedChests]
        self.year = signUpCalendar['year']
        self.month = signUpCalendar['month']
        self.day = signUpCalendar['day']

    def eventParser(self,eventsData):
        jsonData = json.loads(eventsData.decode('ascii'))
        eventIds = []
        spendEventIds = []
        self.events = jsonData['events']
        for event in self.events:
            if int(event['prize']) == 1:
                eventIds.append(event['eventId'])
            if int(event['prize']) != 0 and event['name'] == 'Alliance Mirlith Spend':
                spendEventIds.append(event['eventId'])
        return eventIds, spendEventIds

    def getSeedParser(self, jsonData):
        chestId = []
        offerId = []
        limit = []
        data = json.loads(jsonData.decode('ascii'))
        cityId = list(data['seed']['cityBuff'].keys())
        bid_for_gates = {}
        kid_for_gates = ''
        totalGems = 0
        # Ниже мы сохраняем значение ключа "totalGems" из элемента "player" в "seed"
        if 'seed' in data and 'player' in data['seed'] and 'totalGems' in data['seed']['player']:
            totalGems = int(data['seed']['player']['totalGems'])
        #проверяем есть ли бесплатный offer(работает не всегда корректно)
        for activity in data['seed']['activity'].values():
            if isinstance(activity, dict) and 'offer' in activity:
                offer = activity['offer']
                if isinstance(offer, dict) and offer.get('box'):
                    for box in offer['box']:
                        if box.get('price') == '0':
                            chestId.append(box['chestId'])
                            offerId.append(offer['offerId'])
                            limit.append(box['limit'])
        #сохраняем уровень аккаунта
        if 'seed' in data and 'allianceDiplomacies' in data['seed']:
            self.allianceName = data['seed']['allianceDiplomacies'].get('allianceName', '')
        else:
            self.allianceName = ''

        if 'seed' in data and 'xp' in data['seed'] and 'lvl' in data['seed']['xp']:
            lvl = data['seed']['xp']['lvl']
        for city in cityId:
            city_buildings = data['seed']['buildings'].get(f"city{city}")
            if city_buildings is not None:
                pos0 = city_buildings.get("pos0")
                if pos0 is not None:
                    bid_for_gates[city] = pos0[-1]

        for key in data['seed']['knights']:
            if key.startswith('city') and key.endswith(tuple(cityId)):
                last_key = list(data['seed']['knights'][key].keys())[-1]
                kid_for_gates = ''.join(filter(str.isdigit, last_key))
        self.nickname = data['seed']['player']['name']

        chestId = list(set(chestId))
        offerId = list(set(offerId))
        limit = list(set(limit))
        cityId = list(set(cityId))

        return chestId, offerId, limit, cityId, bid_for_gates, kid_for_gates, totalGems, lvl








