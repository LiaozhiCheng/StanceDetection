import time
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
import random

news_stance_dataset = list()
with open('news_stance_dataset_v3.json', 'r', encoding="utf-8") as json_file:
    news_stance_dataset = json.load(json_file)

similar_title_dict = dict()
with open('title_similiar.json', 'r', encoding="utf-8") as json_file:
    similar_title_dict = json.load(json_file)

def similar_news_statement(news: str):
    if news not in similar_title_dict:
        return False
    similarity_list = similar_title_dict[news]
    news_statement_list = list()
    for  s_list in similarity_list:
        s_news, s_similar = s_list[0], s_list[1]
        if s_similar > 0.8:
            complete_s_news = search_news(s_news)
            complete_s_news['similarity'] = s_similar
            news_statement_list.append(complete_s_news)
    news_statement_list = sorted(news_statement_list, key=lambda d:d['similarity'])

    #過濾相同的標題
    news_statement_list = list({item['title']: item for item in news_statement_list}.values())

    return news_statement_list

def search_news(title):
    news = next((item for item in news_stance_dataset if item["title"] == title), False)
    if news:
        return {'title': news['title'], 'stance': int(news['stance']), 'sentiment': int(news['sentiment']), 'media': news['source']}
    
error_list = list()
acc_num = 0
amount = 0
start_time = time.time()
execution_times = []
for news in news_stance_dataset:
    title = news['title']
    label = int(news['stance'])

    similar_news_list = similar_news_statement(news['title'])
    if len(similar_news_list) <= 1:
        continue

    amount += 1
    stance_score_dict = {1:0,0:0,-1:0}
    random.shuffle(similar_news_list)
    train_num = int(len(similar_news_list) * 0.5)
    train_time = 0
    for s_news in similar_news_list:
        
        if s_news['title'] == news['title'] and s_news['media'] == news['source']:
            continue
        else:
            s_label = s_news['stance']
            stance_score_dict[s_label] += 1
        train_time +=1
        if train_time > train_num:
            break
    
    max_label = max(stance_score_dict, key=stance_score_dict.get)
    if max_label == label:
        acc_num+=1
        end_time = time.time()
    else:
        error_list.append({title:stance_score_dict})
    execution_times.append(end_time - start_time)

print("执行时间：", execution_times[-1], "秒")
print("平均执行时间：", execution_times[-1]/amount, "秒")
print('acc_num:',acc_num)
print('amount',amount)
print('accuray', acc_num/amount)
with open('normal_time_experiment.json', 'w') as jsonfile:
    json.dump(execution_times, jsonfile)
with open('normal_error.json', 'w', encoding = 'utf-8') as jsonfile:
    json.dump(error_list, jsonfile,ensure_ascii=False,indent=4)
plt.plot(range(0, len(execution_times)), execution_times, marker='o')
plt.xlabel('Execution Number')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time of Your Function')
plt.grid(True)
plt.show()