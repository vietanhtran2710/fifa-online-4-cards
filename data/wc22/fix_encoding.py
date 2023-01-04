import json

with open("wc22.json") as json_file:
    data = json.load(json_file)

with open("wc22.json", "w", encoding='utf-8') as fixed:
    json.dump(data, fixed, indent=2, ensure_ascii=False)
