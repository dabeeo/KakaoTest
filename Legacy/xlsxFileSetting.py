# import re

# source_file = "/Users/dabeeo/Downloads/asdf/combined_data3.txt"  # 원본 txt 파일
# output_file = "/Users/dabeeo/Downloads/asdf/combined_data4.txt"  # 수정된 내용을 저장할 파일

# # with open(source_file, 'r') as infile, open(output_file, 'w') as outfile:
# #     for line in infile:
# #         modified_line = f" \"{line.strip()}\","  # 줄 앞뒤에 " "와 , 추가
# #         outfile.write(modified_line + '\n')
# #

# # unique_lines = set()
# # with open(source_file, 'r') as infile, open(output_file, 'w') as outfile:
# #     for line in infile:
# #         if line not in unique_lines:
# #             unique_lines.add(line)
# #             outfile.write(line)

# def sorting_key(s):
#     # 정규식 패턴을 사용하여 한글, 영문, 숫자, 기타 순으로 정렬
#     return (
#         re.match("[가-힣]", s) is None,  # 한글이 아니면 True (뒤로)
#         re.match("[A-Za-z]", s) is None,  # 영문이 아니면 True (뒤로)
#         re.match("[0-9]", s) is None,     # 숫자가 아니면 True (뒤로)
#         s                                 # 기본적으로 문자열 자체로 정렬
#     )

# # 파일 읽기 및 정렬 후 새 파일에 저장
# with open(source_file, 'r') as infile, open(output_file, 'w') as outfile:
#     lines = infile.readlines()
#     sorted_lines = sorted(lines, key=sorting_key)
#     outfile.writelines(sorted_lines)


a = int(5)
while a < 102:
    print(f'=COUNTIF(INDIRECT(N2 & "!D{a}:II{a}"), "Pass")')
    a+=1
