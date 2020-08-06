from enum import Enum

class CallBacksTexts(Enum):
    icq = ("icq", "ICQ")
    agent = ("agent", "Агент")
    myteam = ("myteam", "Myteam")
    linux_64_site = ("linux64Site", "Linux x64 Site")
    linux_64_update = ("linux64Update", "Linux x64 Update")
    linux_64_store = ("linux64Store", "Linux x64 Store")
    linux_32_site = ("linux32Site", "Linux x32 Site")
    linux_32_update = ("linux32Update", "Linux x32 Update")
    linux_32_store = ("linux32Store", "Linux x32 Store")
    macos_site = ("macOSSite", "macOS Site")
    macos_update = ("macOSUpdate", "macOS Update")
    macos_store = ("macOSStore", "macOS Store")
    windows_site = ("windowsSite", "Windows Site")
    windows_update = ("windowsUpdate", "Windows Update")
    beta = ("beta", 'Бета')
    release = ("release", 'Релиз')
    back = ("back", "Упс")
    error = "error"

class Texts(Enum):
    myteam_release_additional = "https://hb.bizmrg.com/myteam-www/mac/x64/myteam.dmg"

class State(Enum):
    untested = 'untested'
    tested = 'tested'
    failed = 'failed'
    unsuitable = 'unsuitable'

class BaseUpdate:

    def __init__(self, product):
        self.type_updatе = ''
        self.product = product
        self.platforms = {}
        self.platforms[CallBacksTexts.linux_32_site] = State.untested
        self.platforms[CallBacksTexts.linux_32_store] = State.untested
        self.platforms[CallBacksTexts.linux_32_update] = State.untested
        self.platforms[CallBacksTexts.linux_64_site] = State.untested
        self.platforms[CallBacksTexts.linux_64_store] = State.untested
        self.platforms[CallBacksTexts.linux_64_update] = State.untested
        self.platforms[CallBacksTexts.macos_site] = State.untested
        self.platforms[CallBacksTexts.macos_store] = State.untested
        self.platforms[CallBacksTexts.macos_update] = State.untested
        self.platforms[CallBacksTexts.windows_site] = State.untested
        self.platforms[CallBacksTexts.windows_update] = State.untested

    def description(self):
        result = self.product.value[1]
        for platform, state in self.platforms.items():
            if state == State.tested:
                result += '\n☑️ ' + platform.value[1]
        return result

    def is_ready(self):
        for platform, state in self.platforms.items():
            if state == State.untested or state == State.failed:
                return False
        return True

    def get_buttons(self):
        mass_buttons = []
        for platform, state in self.platforms.items():
            if state == State.untested:
                button = [{"text": platform.value[1],
                           "callbackData": platform.value[0] + self.type_update.value[0] + self.product.value[0]}]
                mass_buttons.append(button)
            elif state == State.failed:
                button = [{"text": platform.value[1],
                           "callbackData": platform.value[0] + self.type_update.value[0] + self.product.value[0], "style": "attention"}]
                mass_buttons.append(button)
        button_back = [{"text": 'Назад',
                        "callbackData": CallBacksTexts.back.value[0] + self.type_update.value[0]}]
        mass_buttons.append(button_back)
        return mass_buttons




class Beta(BaseUpdate):

    def __init__(self, product):
        super().__init__(product)
        self.type_update = CallBacksTexts.beta
        self.platforms[CallBacksTexts.linux_32_site] = State.unsuitable
        self.platforms[CallBacksTexts.linux_32_store] = State.unsuitable
        self.platforms[CallBacksTexts.linux_32_update] = State.unsuitable
        self.platforms[CallBacksTexts.linux_64_store] = State.unsuitable
        self.platforms[CallBacksTexts.macos_store] = State.unsuitable

        if self.product == CallBacksTexts.agent:
            self.platforms[CallBacksTexts.linux_64_update] = State.unsuitable
            self.platforms[CallBacksTexts.windows_update] = State.unsuitable
            self.platforms[CallBacksTexts.macos_update] = State.unsuitable

class Release(BaseUpdate):

    def __init__(self, product):
        super().__init__(product)
        self.type_update = CallBacksTexts.release
        self.platforms[CallBacksTexts.macos_store] = State.unsuitable

        if self.product == CallBacksTexts.myteam:
            self.platforms[CallBacksTexts.linux_64_store] = State.unsuitable
            self.platforms[CallBacksTexts.linux_32_store] = State.unsuitable