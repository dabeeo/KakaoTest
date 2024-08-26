class AttributeChecker:
    def __init__(self, json_data, common_facility):
        self.data = json_data
        self.attribute_data = common_facility

    def get_floor_name(self, floor):
        return floor["name"][0]["text"] if floor["name"] else "Unknown"

    def clean_title(self, s):
        return s.replace(" ", "").replace("\n", "")

    def find_attribute_codes(self, file):
        all_passed = True
        file.write('\n')

        for floor in self.data["payload"]["floors"]:
            floor_name = self.get_floor_name(floor)
            objects = {obj["id"]: obj for obj in floor.get("objects", [])}
            
            for poi in floor.get("pois", []):
                if poi.get("layerGroupCode") == "Etc":
                    continue  # "Etc"로 표시된 POI는 검사에서 제외

                object_id = poi.get("objectId")
                poi_title_cleaned = self.clean_title(poi.get("title", ""))
                
                if object_id and object_id in objects:
                    attribute_code = objects[object_id].get("attributeCode", "Unknown")
                    title_exists_in_facility = False
                    key_matches_attribute_code = False

                    for facility in self.attribute_data.values():
                        if poi_title_cleaned in [self.clean_title(title) for title in facility["title"]]:
                            title_exists_in_facility = True
                            if attribute_code in facility["key"]:
                                key_matches_attribute_code = True
                            break

                    if not title_exists_in_facility:
                        print(f'메타데이터 추가: 층: {floor_name}, POI: {poi["id"]}, 타이틀: "{poi_title_cleaned}"\n')
                        # file.write(f'메타데이터 추가 데이터: {floor_name}, POI: {poi["id"]}, 타이틀: "{poi_title_cleaned}"\n')

                    elif key_matches_attribute_code:
                        print(f'Pass: 층: {floor_name}, POI: {poi["id"]}, 타이틀: "{poi_title_cleaned}"\n')
                        # file.write(f'Pass: {floor_name}, POI: {poi["id"]}, 타이틀: "{poi_title_cleaned}"\n')

                    else:
                        # print(f'Fail: 층: {floor_name}, POI: {poi["id"]}, 타이틀: "{poi_title_cleaned}", Attribute: {attribute_code}\n')
                        file.write(f'Fail: Atrribute 매칭 : {floor_name}, POI: {poi["id"]}, 타이틀: "{poi_title_cleaned}", Attribute: {attribute_code}\n')
                        all_passed = False

        return all_passed
