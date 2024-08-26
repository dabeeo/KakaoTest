class SectionValidator:
    def __init__(self, json_data, map_sections_list):
        self.data = json_data
        self.map_sections_list = map_sections_list

    def get_floor_name(self, floor):
        return floor["name"][0]["text"] if floor["name"] else "Unknown"

    def validate_sections(self, file):
        valid = True
        level_count_per_floor = {}  # 층별 LEVEL 개수 저장

        for floor in self.data["payload"]["floors"]:
            floor_name = self.get_floor_name(floor)
            level_count_per_floor[floor_name] = 0

            for section in floor.get("sections", []):
                if section.get("title") == "LEVEL":
                    level_count_per_floor[floor_name] += 1
                    section_id = section.get("id")
                    found = False

                    for map_section in self.map_sections_list:
                        for level in map_section.get("LEVELs", []):
                            if level["id"] == section_id:
                                found = True
                                size_match = level.get("size") == section.get("size")
                                position_match = level.get("position") == section.get("position")
                                layer_group_code_match = level.get("layerGroupCode") == section.get("layerGroupCode")

                                if not size_match:
                                    # print(f"Fail: {floor_name}, ID: {section_id}, 사이즈가 일치하지 않습니다")
                                    file.write(f"\nFail: {floor_name}, ID: {section_id}, 사이즈가 일치하지 않습니다")
                                    valid = False

                                elif not position_match:
                                    # print(f"Fail: {floor_name}, ID: {section_id}, 포지션이 일치하지 않습니다")
                                    file.write(f"\nFail: {floor_name}, ID: {section_id}, 포지션이 일치하지 않습니다")
                                    valid = False

                                elif not layer_group_code_match:
                                    print(f"Fail: {floor_name}, ID: {section_id}, 레이어 그룹 코드가 일치하지 않습니다.")
                                    file.write(f"\nFail: {floor_name}, ID: {section_id}, 레이어 그룹 코드가 일치하지 않습니다.")
                                    valid = False

                    if not found:
                        print(f"층: {floor_name}, ID: {section_id}가 map_section_list에 존재하지 않습니다.")
                        file.write(f"\nFail: {floor_name}, ID: {section_id}가 map_section_list에 존재하지 않습니다.")
                        valid = False

        # 층별 LEVEL의 개수 검증
        for floor_name, count in level_count_per_floor.items():
            if count < 1:  # 각 층과 그룹에 최소 1개의 LEVEL이 있어야 함
                print(f"Fail: {floor_name}에 LEVEL 섹션이 없습니다.")
                file.write(f"\nFail: {floor_name}에 LEVEL 섹션이 없습니다.\n")
                valid = False

        if valid:
            print('Pass: "LEVEL" 바닥판 검수')
            return True
        else:
            return False
