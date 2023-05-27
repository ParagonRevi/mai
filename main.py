from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from plyer import filechooser
from kivy.utils import platform
from kivymd.toast import toast
from kivy.properties import StringProperty
from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import mainthread

import threading
import platform

from concurrent.futures import ThreadPoolExecutor
from workers import mainWorker

KV = '''
#:import CustomOverFlowMenu __main__.CustomOverFlowMenu
MDScreen:
    MDNavigationLayout:
        MDScreenManager:
            MDScreen:
                MDBoxLayout:
                    orientation: 'vertical'
                    MDBottomNavigation:
                        panel_color: "#eeeaea"
                        selected_color_background: "red"
                        text_color_active: "black"

                        MDBottomNavigationItem:
                            name: 'Accounts'
                            text: 'Accounts'
                            icon: 'account-group'
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDScrollView:
                                    bar_width: "15dp"
                                    MDBoxLayout:
                                        size_hint_y: None
                                        height: self.minimum_height
                                        orientation: 'vertical'
                                        MDLabel:
                                            text: app.accountsInput
                                            size_hint_y: None
                                            height: self.texture_size[1]
                                            text_size: self.width, None
                                            font_size: '13sp'
                                            padding: 15, 0
                            MDTopAppBar:
                                title: "Accounts"
                                id: account_top_app_bar
                                use_overflow: True
                                overflow_cls: CustomOverFlowMenu()
                                pos_hint: {"top": 1}
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
                                right_action_items: [["account-plus", lambda x: app.addFromFile()]]
                        MDBottomNavigationItem:
                            name: 'Output'
                            text: 'Output'
                            icon: 'application-outline'
                            MDBoxLayout:
                                orientation: 'vertical'
                                MDScrollView:
                                    bar_width: "15dp"
                                    MDBoxLayout:
                                        size_hint_y: None
                                        height: self.minimum_height
                                        orientation: 'vertical'
                                        MDLabel:
                                            text: app.accountsInput
                                            size_hint_y: None
                                            height: self.texture_size[1]
                                            text_size: self.width, None
                                            font_size: '13sp'
                                            padding: 15, 0
                            MDTopAppBar:
                                title: "Output"
                                id: output_top_app_bar
                                use_overflow: True
                                overflow_cls: CustomOverFlowMenu()
                                pos_hint: {"top": 1}
                                left_action_items: [['menu', lambda x: nav_drawer.set_state("open")], ]


        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            padding: 50, 50, 50, 50
            ContentNavigationDrawer:
                orientation: 'vertical'
                MDBoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .9}
                    size_hint: None, None
                    width: dp(300)
                    orientation: 'horizontal'
                    MDCheckbox:
                        id: offer
                        pos_hint: {'right': 0.5, 'center_y': .9}
                    MDLabel:
                        text: "Claim free offer"
                        font_size: "14sp"
                        pos_hint: {'right': 0.5, 'center_y': .9}

                MDBoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .85}
                    size_hint: None, None
                    width: dp(300)
                    orientation: 'horizontal'
                    MDCheckbox:
                        id: calendarRewards
                        pos_hint: {'right': 0.5, 'center_y': .85}
                    MDLabel:
                        text: "Claim calendar rewards"
                        font_size: "14sp"
                        pos_hint: {'right': 0.5, 'center_y': .85}

                MDBoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: None, None
                    width: dp(300)
                    orientation: 'horizontal'
                    MDCheckbox:
                        id: eventRewards
                        pos_hint: {'right': 0.5, 'center_y': .8}
                    MDLabel:
                        text: "Claim event rewards"
                        font_size: "14sp"
                        pos_hint: {'x': 0, 'center_y': .8}

                MDBoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .75}
                    size_hint: None, None
                    width: dp(300)
                    orientation: 'horizontal'
                    MDCheckbox:
                        id: bubble
                        pos_hint: {'right': 0.5, 'center_y': .75}
                    MDLabel:
                        text: "Bubble"
                        font_size: "14sp"
                        pos_hint: {'right': 0.5, 'center_y': .75}
                MDBoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .7}
                    size_hint: None, None
                    width: dp(300)
                    orientation: 'horizontal'
                    MDCheckbox:
                        id: gateSwitch
                        pos_hint: {'right': 0.5, 'center_y': .7}
                    MDLabel:
                        text: "Close gates"
                        font_size: "14sp"
                        pos_hint: {'x': 0.5, 'center_y': .7}

                MDBoxLayout:
                    pos_hint: {'x': 0.5, 'center_y': .5}
                    width: dp(500)
                    orientation: 'horizontal'
                    MDTextField:
                        id: gameVersionInput
                        hint_text: "Game version"
                        mode: "fill"
                        pos_hint: {'x': 0.5, 'center_y': .5}


                MDRaisedButton:
                    text: "Run"
                    md_bg_color: "red"
                    pos_hint: {'center_x': 1, 'center_y': .2}
                    on_release: app.runBot()


            MDBoxLayout:



'''


class CustomOverFlowMenu(MDDropdownMenu):
    # In this class you can set custom properties for the overflow menu.
    pass


class ContentNavigationDrawer(MDBoxLayout):
    pass


class EVDBot(MDApp):
    accountsInput = StringProperty()

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

    def callback(self, instance_action_top_appbar_button):
        print(instance_action_top_appbar_button)

    def addFromFile(self):
        if platform == 'win':
            # Для Windows используется метод filechooser.open_file() из библиотеки KivyMD
            filters = [('Text Files', '*.txt')]
            path = filechooser.open_file(filters=filters)
            if path:
                selected_file = path[0]
                with open(selected_file, 'r') as file:
                    self.accountsList = file.read().splitlines()
                toast(f'Selected file: {selected_file}')
            else:
                toast('No file selected')

        elif platform == 'android':
            # Для Android также используется метод filechooser.open_file() из библиотеки KivyMD
            filters = [
                {
                    'title': 'Text Files',
                    'patterns': ['*.txt'],
                },
            ]
            path = filechooser.open_file(filters=filters)
            if path:
                selected_file = path[0]
                with open(selected_file, 'r') as file:
                    self.accountsList = file.read().splitlines()
                toast(f'Selected file: {selected_file}')
            else:
                toast('No file selected')

        else:
            # Если операционная система не поддерживается, выведите сообщение об ошибке
            toast('Unsupported platform')
        self.accountsInput = "\n".join(str(accountsList) for accountsList in self.accountsList)

    def runWorkers(self):
        print('Starting threads...')
        max_threads = 100
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for acc in self.scriptdata:
                login, password = acc['account'].split(':')
                worker = mainWorker(login=login, password=password, offer=acc['offer'], bubble=acc['bubble'],
                                    gateSwitch=acc['gateSwitch'], calendarRewards=acc['calendarRewards'],
                                    eventRewards=acc['eventRewards'], vcs=acc['vcs'])
                worker.writeOutput = self.updateOutput
                executor.submit(worker.run)
            num_threads = threading.active_count()
            print("Количество активных потоков:", num_threads)

    def runBot(self):
        self.offer = False
        self.bubble = False
        self.closeGates = False
        self.calendarRewards = False
        self.eventRewards = False
        self.version = '16.6.1'
        if self.root.ids.gameVersionInput.text:
            self.version = self.root.ids.gameVersionInput.text
        if self.root.ids.offer.active:
            self.offer = True
        if self.root.ids.calendarRewards.active:
            self.calendarRewards = True
        if self.root.ids.eventRewards.active:
            self.eventRewards = True
        if self.root.ids.bubble.active:
            self.bubble = True
        if self.root.ids.gateSwitch.active:
            self.closeGates = True
        self.scriptdata = []
        for i in range(len(self.accountsList)):
            self.scriptdata.append(
                {
                    'account': self.accountsList[i],
                    'offer': self.offer,
                    'bubble': self.bubble,
                    'gateSwitch': self.closeGates,
                    'calendarRewards': self.calendarRewards,
                    'eventRewards': self.eventRewards,
                    'vcs': self.version
                }
            )
        print(self.scriptdata)
        self.runWorkers()

    @mainthread
    def updateOutput(self, instance, value):
        self.outputWidget.append(value)


EVDBot().run()