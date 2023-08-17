
from tqdm import tqdm
import json
import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', family='Microsoft JhengHei')
sentence_ws_dict = dict()


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


#讀欲更新檔案
news_stance_dataset = list()
with open('news_stance_dataset_v3.json', 'r', encoding="utf-8") as json_file:
    news_stance_dataset = json.load(json_file)
#過濾相同的標題
news_stance_dataset = list({item['title']: item for item in news_stance_dataset}.values())

#讀相似新聞的檔案
similar_title_dict = dict()
with open('title_similiar.json', 'r', encoding="utf-8") as json_file:
    similar_title_dict = json.load(json_file)

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
        if s_similar > 0.7:
            complete_s_news = search_news(s_news)
            complete_s_news['similarity'] = s_similar
            news_statement_list.append(complete_s_news)
    news_statement_list = sorted(news_statement_list, key=lambda d:d['similarity'])

    #過濾相同的標題
    news_statement_list = list({item['title']: item for item in news_statement_list}.values())

    return news_statement_list

#找出相似新聞中stance不一樣的
def different_stance_news(whole_news:dict):
    news_statement_list = similar_news_statement(whole_news['title'])
    diff_news_list = [news for news in news_statement_list if news['stance'] != whole_news['stance']]
    return diff_news_list

def each_stance_news(whole_news:dict):
    news_statement_list = similar_news_statement(whole_news['title'])
    positive_news_list = [news for news in news_statement_list if news['stance'] == 1]
    neutral_news_list = [news for news in news_statement_list if news['stance'] == 0]
    negative_news_list = [news for news in news_statement_list if news['stance'] == -1]
    print(news_statement_list)
    print('------------------------------')
    print(positive_news_list)
    temp_dict = dict()
    for news in positive_news_list:
        if media_stance[news['media']] not in temp_dict:
            temp_dict[media_stance[news['media']]] =1
        else:
            temp_dict[media_stance[news['media']]] +=1
    print(temp_dict)
        
    categories = list(temp_dict.keys())
    values = list(temp_dict.values())
    plt.scatter(categories,values)
    plt.title(whole_news['title']+' positive related news')
    plt.xlabel('media_stance')
    plt.ylabel('number')

    plt.show()

def test_func():
    target_news_title = "保護力最佳疫苗曝　高端、BNT、莫德納、AZ優缺點一次看"
    target_news = search_news(target_news_title)
    print('news:', target_news['title'])
    print('stance:', target_news['stance'])
    print('sentiment:', target_news['sentiment'])
    print('simialr news: ')
    print(similar_news_statement(target_news['title']))
    print('different stance')
    for news in different_stance_news(target_news):
        print(news)
    # print(different_stance_news(target_news))
    

def test_func2():
    num_items = 10
    test_list = random.sample(news_stance_dataset, num_items)
    for target_news in test_list:
        target_news = search_news(target_news['title'])
        print('news:', target_news['title'])
        print('stance:', target_news['stance'])
        print('sentiment:', target_news['sentiment'])
        print('simialr news: ')
        print(similar_news_statement(target_news['title']))
        print('different stance')
        diff_news_list = different_stance_news(target_news)
        for item in diff_news_list:
            print(item)



def test_func3():
    num_items = 1


    target_news = search_news('高端：台灣疫苗接種記錄，出國可通行無阻 指揮中心這樣回應')
    print('news:', target_news['title'])
    print('stance:', target_news['stance'])
    print('sentiment:', target_news['sentiment'])
    each_stance_news(target_news)

if __name__ == "__main__":
    #test_func3()
    print(similar_news_statement())



# for news, similarity_list in similar_title_dict.items():
#     print('news:', news)
#     print('simialr news: ')
#     for  s_list in similarity_list:
#         s_news, s_similar = s_list[0], s_list[1]
#         if s_similar > 0.7:
#             complete_s_news = search_news(s_news)
#             complete_s_news['similarity'] = s_similar
#             print(complete_s_news)
    
#     print('---------------------------')
#     break