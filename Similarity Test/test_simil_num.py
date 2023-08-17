import json

similar_title_dict = dict()
with open('title_similiar.json', 'r', encoding="utf-8") as json_file:
    similar_title_dict = json.load(json_file)

count_sum = 0
for news, similar_list in similar_title_dict.items():
    count_num = 0
    for s_value in similar_list:
        if s_value[1]  > 0.7 :
            count_num+=1
    if count_num == 1:
        count_sum+=1
        print(news,count_num)
print(count_sum)