from DataFolder.POI_titles import poi_title_list

# 중복 제거 및 정렬
sorted_unique_poi_titles = sorted(set(poi_title_list), key=lambda x: (x.isdigit(), x.isalpha(), x))

# 파일 경로
file_path = '/Users/dabeeo/Downloads/unique_poi_titles.txt'

# 정렬된 리스트를 txt 파일로 저장
with open(file_path, 'w', encoding='utf-8') as file:
    for title in sorted_unique_poi_titles:
        file.write(f'"{title}",\n')
