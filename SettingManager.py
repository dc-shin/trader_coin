import uuid
from enum import Enum

class SettingManager:
    g_uuid = str(uuid.uuid4())
    
    @staticmethod
    def checkHttpCode(class_name, func_name, code):
        result = 'fail' if code != 200 else 'success'
        print('[{}][{}] {}. code: {}'.format(class_name, func_name, result, code))
        return code == 200