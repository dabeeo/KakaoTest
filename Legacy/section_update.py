import json
import requests
from requests.auth import HTTPBasicAuth

""" 토큰 발행 코드 """
bodys={
    "grant_type": "client_credentials",
    "username": "juhyeon",
    "password": "ekqldh12!@"
}

url = f"https://oauth.dabeeomaps.com/oauth/token"

auth_username = 'reference_application'
auth_password = 'dabeeo0228'

# POST 요청 수행 (기본 인증 추가)
response = requests.post(url, data=bodys, auth=HTTPBasicAuth(auth_username, auth_password))

# 응답 내용 출력
response_data = json.loads(response.text)

# "access_token" 추출 및 저장
access_token = response_data.get('access_token')

# Bearer Token을 사용한 인증 설정
headers = {
    'Authorization': f'Bearer {access_token}'
}

body_data = {
    "username": "juhyeon",  # 실제 사용자 이름으로 변경
    "password": "ekqldh12!@"   # 실제 비밀번호로 변경
}


result_json = {
    "maps": []
}

# Bearer Token 인증 헤더 (실제 토큰으로 교체 필요)
headers_data = {'Authorization': f'Bearer {access_token}'}

# 각 mapID에 대해 API 요청 수행 및 결과 저장
mapID = "MP-t4yfisdhfc4z0435"
url = f'https://api.dabeeomaps.com/v2/map/{mapID}'

response = requests.get(url, headers=headers_data, data=body_data)
if response.status_code == 200:
    data = response.json()
    print(f'{mapID} is Done')

    map_info = {
        'MapID': data.get('payload', {}).get('id'),
        'name': data.get('payload', {}).get('name'),
        'LEVELs': []
    }

    # 'LEVELs' 정보 추출
    for floor in data['payload'].get('floors', []):
        for section in floor.get('sections', []):
            if section.get('title') == 'LEVEL':
                section_info = {
                    'id': section.get('id'),
                    'size': section.get('size'),
                    'position': section.get('position'),
                    'layerGroupCode': section.get('layerGroupCode')
                }
                map_info['LEVELs'].append(section_info)

    result_json['maps'].append(map_info)
else:
    print(f'{mapID}is Fail')
# 결과를 JSON 파일로 저장
with open('123.json', 'w', encoding='utf-8') as file:
    json.dump(result_json, file, ensure_ascii=False, indent=4)

# 파일 내용을 읽어서 출력할 때도 UTF-8 인코딩 사용
with open('123.json', 'r', encoding='utf-8') as file:
    print(file.read())
