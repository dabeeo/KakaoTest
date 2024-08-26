import json
import requests
from requests.auth import HTTPBasicAuth


class GetAceessToken:
    def __init__(self):
        self.access_token = None
        self.tokenHeader = None

    def call_token_API(self):
        url = "https://oauth.dabeeomaps.com/oauth/token"
        Access_Body = {
            "grant_type": "client_credentials",
            "username": "juhyeon",
            "password": "ekqldh12!@"
        }
        auth_username = 'reference_application'
        auth_password = 'dabeeo0228'

        response = requests.post(url, data=Access_Body, auth=HTTPBasicAuth(auth_username, auth_password))
        response_data = json.loads(response.text)
        self.access_token = response_data.get('access_token')
        self.tokenHeader = {'Authorization': f'Bearer {self.access_token}'}

        return self.access_token

    def call_QA_List(self):
        QA_list_url = "https://interworking-map-km.dabeeostudio.com/v1/qa/list"
        response = requests.get(QA_list_url, headers=self.tokenHeader)

        if response.status_code == 200:
            data = response.json()
            map_ids = [item["mapId"] for item in data.get("payload", [])]
            
            return map_ids
        else:
            return [] 

    def call_QA_done(self, targetMap):
        build_url = f"https://interworking-map-km.dabeeostudio.com/v1/qa/{targetMap}"
        response = requests.post(build_url, headers=self.tokenHeader)
        
        if response.status_code == 200:
            print("Done\n")
        else:
            print(response.status_code)

    def call_mapData(self, targetMap):
        mapData_api_url = f"https://api.dabeeomaps.com/v2/map/{targetMap}"
        
        MapData_Body = {
            "username": "juhyeon",
            "password": "ekqldh12!@"
        }

        response = requests.get(mapData_api_url, headers=self.tokenHeader, params=MapData_Body)
        
        return response
