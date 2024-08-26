class MapValidator:
    def __init__(self, json_data, map_context):
        self.data = json_data
        self.map_context = {entry["MapID"]: entry["LayerGroup"] for entry in map_context}

    def get_floor_name(self, floor):
        return floor["name"][0]["text"] if floor["name"] else "Unknown"

    def validate_layer_group_code(self, file):
        map_id = self.data["payload"]["id"]

        layer_groups = self.map_context.get(map_id, [""])  # 기본값으로 [""] 설정

        # MapContext에서 LayerGroup이 ""이면 검증을 수행하지 않음
        if layer_groups == [""]:
            print(f"Pass: {map_id} 레이어 그룹 코드가 없으므로 스킵합니다.")
            return True

        fail = False

        for floor in self.data["payload"]["floors"]:
            floor_name = self.get_floor_name(floor)

            for item_type in ["objects", "sections", "pois"]:
                
                for item in floor.get(item_type, []):
                    layer_group_code = item.get("layerGroupCode", "")  # 기본값을 ""로 설정
                    item_id = item.get("id", "Unknown")

                    # LayerGroup에 특정 값이 있고 layerGroupCode가 빈 문자열이거나 해당 값이 LayerGroup에 포함되지 않은 경우, "Etc"는 무시
                    if layer_group_code != "Etc" and (not layer_group_code or layer_group_code not in layer_groups):
                        print(f"Fail: {floor_name}, ID: {item_id}, 레이어 그룹 코드가 공백입니다")
                        file.write(f"\nFail: {floor_name}, ID: {item_id}, 레이어 그룹 코드가 공백")
                        fail = False

        if not fail:
            print("Pass: 레이어 그룹 검수")
            return True

        else:
            return False
