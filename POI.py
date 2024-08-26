import os

from DataFolder.POI_titles import poi_title_list
from DataFolder.POI_expect import poi_expect_list


class POIChecker:
    def __init__(self, json_data):
        self.data = json_data
        self.cleaned_poi_titles = [self.clean_title(title) for title in poi_title_list]

    def clean_title(self, title):
        return title.replace("\n", "").replace(" ", "")

    def get_floor_name(self, floor):
        return floor["name"][0]["text"] if floor["name"] else "Unknown"

    def check_pois(self, map_id, file):
        not_found_items = []

        for floor in self.data["payload"]["floors"]:
            floor_name = self.get_floor_name(floor)
            
            for poi in floor["pois"]:
                if poi.get("layerGroupCode") != "Etc":
                    cleaned_title = self.clean_title(poi["title"])
                    
                    if cleaned_title not in self.cleaned_poi_titles:
                        not_found_items.append((floor_name, poi["id"], cleaned_title))

        if len(not_found_items) == 0:
            print("Pass: POI 타이틀 검수")
            return True
        
        else:
            self.not_in_POI_list(not_found_items, map_id)
            for i in not_found_items:
                file.write(f'\nFail: 미등록 POI 타이틀 : {i}')
            print(f'Fail: 미등록 POI 타이틀 : {not_found_items}')
            return False

    def check_empty_object_ids(self, file):
        empty_object_items = []

        for floor in self.data["payload"]["floors"]:
            floor_name = self.get_floor_name(floor)
            for poi in floor["pois"]:
                poi_id = poi.get("id")
                if poi.get("objectId") == "" and poi.get("layerGroupCode") != "Etc" and poi_id not in poi_expect_list:
                    empty_object_items.append((floor_name, poi_id, poi["title"]))

        if len(empty_object_items) == 0:
            print("Pass: POI & 오브젝트 미연결 검수")
            return True
        else:
            for item in empty_object_items:
                print(f'Fail: POI & 오브젝트 미연결 : {item}')
                file.write(f'\nFail: 미연결 POI 타이틀 : {item}')
            return False
        
    def not_in_POI_list(self, not_found_items, map_id):
        save_path = "/Users/dabeeo/KakaoWindow/kakao/AddPOITItle"
        file_name = os.path.join(save_path, f"{map_id}.txt")

        with open(file_name, 'w', encoding='utf-8') as file:
            for item in not_found_items:
                poi_title = item[2]
                file.write(f"\n{poi_title},")

