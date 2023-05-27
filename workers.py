from kivy.event import EventDispatcher
from kivy.properties import StringProperty
import platform
import os
import traceback

from elvesVsDwarves import elvesVsDwarves

class WorkerSignals(EventDispatcher):
    outputWrite = StringProperty()


class mainWorker():
    def __init__(self,
                 login: str,
                 password: str,
                 offer: bool,
                 bubble: bool,
                 gateSwitch: bool,
                 calendarRewards: bool,
                 eventRewards: bool,
                 vcs: str
                 ):
        super().__init__()
        self.signals = WorkerSignals()
        self.vcs = vcs
        self.login = login
        self.password = password
        self.offer = offer
        self.bubble = bubble
        self.closeGates = gateSwitch
        self.calendarRewards = calendarRewards
        self.eventRewards = eventRewards
        self.current_account = f"{login}:{password}"

    def run(self):
        try:
            client = elvesVsDwarves(self.vcs, self.signals)
            client.auth(self.login, self.password)
            client.signup()
            if self.offer:
                client.offer()
            if self.bubble:
                client.bubble()
            if self.closeGates:
                client.closeGates()
            if self.calendarRewards:
                client.claimCalendarReward()
            if self.eventRewards:
                client.claimEventReward()
        except Exception as ex:
            self.saveErrorData()
            client.saveErrorData()
            print(ex)
            print(traceback.format_exc())

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

    #def writeOutput(self, instance, value):
    #    self.signals.outputWrite.emit(value)

