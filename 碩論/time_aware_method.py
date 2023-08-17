
from tqdm import tqdm
import json
import time
import matplotlib.pyplot as plt
import random
media_stance = {
    "中天快點TV": -0.06919534596034466,
    "自由時報": 0.548563406246023,
    "聯合新聞網": 0.7863398935564617,
    "中央社": 0.8597575855016136,
    "TVBS": -0.5302707858747131,
    "中國時報": -0.010053383170122911,
    "SETN 三立新聞網": 0.608548316139993,
    "大紀元": 0.022396715309373295,
    "ettoday": 0.6696251249337366,
    "民視新聞": 0.873015873015873,
    "台視新聞網": 0.9243430234400465,
    "鉅亨網": 1.0,
    "Nownews 今日新聞": 0.8257445003479418,
    "新頭殼 Newtalk": -0.7347775332840706,
    "PChome新聞": 0.6738793701974385,
    "FT中文網": -1.0,
    "健康醫療網": -0.034721666616309634,
    "經濟日報": -0.2722384461850449,
    "中央廣播": 0.396591445807752,
    "TechNews 科技新聞": 0.8554143392490985,
    "MoneyDJ": 0.1365707136619697,
    "華視新聞": -0.004935366162920624,
    "鏡週刊": 0.44947728864075165,
    "HiNet-中華電信HiNet網路服務入口": 0.22279525246672968,
    "公共電視": 0.45262146838433004,
    "遠見雜誌": 0.37342042515925,
    "今周刊": -0.003408270736988425,
    "華人健康網": 0.1046900353360654,
    "早安健康": -0.875,
    "商業週刊": 0.0,
    "噓星聞": 1.0,
    "德國之聲中文網": -0.07692307692307691,
    "法廣": 0.3333333333333333,
    "all": 0.1325690778983875
}
def search_news(title):
    news = next((item for item in news_stance_dataset if item["title"] == title), False)
    if news:
        return {'title': news['title'], 'stance': int(news['stance']), 'sentiment': int(news['sentiment']), 'media': news['source']}
#找出相似的新聞
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

news_stance_dataset = list()
with open('news_stance_dataset_v3.json', 'r', encoding="utf-8") as json_file:
    news_stance_dataset = json.load(json_file)

similar_title_dict = dict()
with open('title_similiar.json', 'r', encoding="utf-8") as json_file:
    similar_title_dict = json.load(json_file)



def simil_score(num):
    if num > 0.9:
        return 2
    if num > 0.8:
        return 1
    if num > 0.75:
        return 0.5
    if num > 0.7:
        return 0.1

acc_num = 0
amount = 0
start_time = time.time()
initial_time = 5.2564
execution_times = []
acc_times = []
train_num = int(1032 *0.5)
for news in news_stance_dataset:
    
    title = news['title']
    label = int(news['stance'])
    media_bias = media_stance[news['source']]
    similar_news_list = similar_news_statement(news['title'])
    if len(similar_news_list) <= 1:
        continue
    amount += 1
    stance_score_dict = {1:0,0:0,-1:0}
    train_time = 0
    random.shuffle(similar_news_list)
    train_num = int(len(similar_news_list) * 0.9)

    for s_news in similar_news_list:

        if s_news['title'] == news['title'] and s_news['media'] == news['source']:
            continue
        else:
            #print(s_news['title'])
            candidate_media_bias = media_stance[s_news['media']]
            s_label = s_news['stance']
            stance_score_dict[s_label] += (s_news['similarity']*2 / abs((candidate_media_bias-media_bias)+1))
        train_time +=1
        if train_time > train_num:
            break
    # print('title: ',title)
    # print('label: ',label)
    # print(stance_score_dict)
    # max_label = max(stance_score_dict, key=stance_score_dict.get)
    # print('predict_label',max_label)

    max_label = max(stance_score_dict, key=stance_score_dict.get)
    if max_label == label:
        acc_num+=1
    end_time = time.time()
    acc_times.append(acc_num)
    execution_times.append(end_time - start_time + initial_time)

    # else:
    #     print('title: ',title)
    #     print('label: ',label)
    #     print(stance_score_dict)
    #     print('predict_label',max_label)
    # if len(similar_news_list) == 1:
    #     print('title: ',title)
    #     print('label: ',label)
    #     print(stance_score_dict)
    #     print('predict_label',max_label)
    # elif len(similar_news_list) == 0:
    #     print("哪尼!!!")
    


print("执行时间：", execution_times[-1], "秒")
print("平均执行时间：", execution_times[-1]/amount, "秒")
print('acc_num:',acc_num)
print('amount',amount)
print('accuray', acc_num/amount)
with open('proposed_time_experiment.json', 'w') as jsonfile:
    json.dump(execution_times, jsonfile)



# plt.plot(range(0, len(acc_times)), acc_times, marker='o')
# plt.xlabel('Execution Number')
# plt.ylabel('Execution Time (seconds)')
# plt.title('Execution Time of Your Function')
# plt.grid(True)
# plt.show()