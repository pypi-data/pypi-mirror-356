from .services.ui import UI
from .services.resources.student import Student
from .services.init_message_bridge import InitMessageBridge
from .services.helper import Helper as SimtrainSdkHelper


class SimtrainEcoMiniAppStreamlitSdk:
    def __init__(self):
        InitMessageBridge()
        self.ui = UI()
        self.student = Student()
        self.helper = SimtrainSdkHelper
