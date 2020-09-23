import json
with open("D://text_crawl_dantri//text_dantri_1", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)
print(data[0]['content'])