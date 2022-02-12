from Singleton import Singleton
from SettingManager import SettingManager
import json
import jwt

class AuthManager(Singleton):
    def __init__(self):
        json_data = {}
        with open('Private', 'r') as private_file:
            json_data = json.load(private_file)

        if not json_data:
            print('[AuthManager][Init] fail reading private file')
        else:
            self.__access_key = json_data['acc']
            self.__secret_key = json_data['sec']
            print('[AuthManager][Init] success reading private file')
        return
    
    def get_auth_headers(self):
        payload = {
            'access_key': self.__access_key,
            'nonce': SettingManager.g_uuid,
        }

        jwt_token = jwt.encode(payload, self.__secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorize_token}
        return headers
