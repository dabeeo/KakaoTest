import time

from POI import POIChecker
from GroupCode import MapValidator
from Section import SectionValidator
from Attribute import AttributeChecker
from API import GetAceessToken

from DataFolder.mapId import mapIds
from DataFolder.Map_Context import MapContext
from DataFolder.Map_Sections import Map_Sections_List
from DataFolder.Attribute_Context import Common_Facility


def main():
    start_time = time.time()

    # Access token 및 지도 리스트 호출
    token_getter = GetAceessToken()
    access_token = token_getter.call_token_API()

    QA_list = token_getter.call_QA_List()  # 실 검수 실행 시 주석 해제
    # QA_list = mapIds
    failCount = 0

    with open('validation_results.txt', 'w', encoding='UTF-8') as file:
        for map_id in QA_list:
            file.write(f"\n{map_id}")

            response = token_getter.call_mapData(map_id)

            if response.status_code != 200 or response.json().get("code") != "00":
                print(f"Could not load data for Map ID: {map_id}. Skipping to next map.")
                file.write(f"Could not load data for Map ID: {map_id}. Skipping to next map.\n")
                continue

            if map_id == "MP-qxocdxesiq0k3331":
                print("현대백화점 부산점이라 패스")
                continue
            if map_id == "MP-rhofdrxs6cdy2741" or map_id == "MP-rl7x2s354awg6681":
                print("빌드 대기 지도")
                continue

            json_data = response.json()

            map_validator = MapValidator(json_data, MapContext)
            section_validator = SectionValidator(json_data, Map_Sections_List)
            poi_checker = POIChecker(json_data)
            attribute_Checker = AttributeChecker(json_data, Common_Facility) # 어트리뷰트 검수 필요 시 해제

            # 검수 메서드 실행
            validation_results = [
                map_validator.validate_layer_group_code(file),  # 그룹 검수 메서드
                section_validator.validate_sections(file),  # 바닥판 검수 메서드
                poi_checker.check_pois(map_id, file),  # POI 타이틀 검수 메서드
                poi_checker.check_empty_object_ids(file),  # POI 오브젝트 연결 검수 메서드
                attribute_Checker.find_attribute_codes(file)  # 어트리뷰트 검수 메서드
            ]

            if all(validation_results):
                token_getter.call_QA_done(map_id)  # QA 프로세스 완료 후 API 호출 필요시 주석 해제
                print("All Passed\n")
            else:
                failCount += 1

    end_time = time.time()
    runtime = end_time - start_time

    print(f'맵 전체 갯수: {len(QA_list)}')
    print(f'Fail: {failCount}')
    print(f"실행 시간: {runtime:.2f}초")


if __name__ == "__main__":
    main()
