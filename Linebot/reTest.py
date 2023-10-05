import re


pattern = r'(\d+)[, ]*'

matches = re.findall(pattern, "112 123 7 8 9 1 ")

for match in matches:
    print(len(match))
