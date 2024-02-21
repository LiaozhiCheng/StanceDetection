import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import time
from matplotlib.font_manager import FontProperties

import matplotlib.dates as mdates
matplotlib.rc('font', family='Microsoft JhengHei')


# chinese_font = FontProperties(fname='/path/to/MicrosoftJhengHei.ttf')
plt.rcParams['font.family'] = 'Arial Unicode MS'

whole_news_list = list()
with open('news_stance_dataset_v3.json', 'r', encoding='utf-8') as jsonfile:
    whole_news_list = json.load(jsonfile)

media_dict = dict() 
for news in whole_news_list:
    if news['source'] not in media_dict:
        media_dict[news['source']] = 1
    else:
        media_dict[news['source']] += 1

#媒體立場
def media_stance(media):
    news_list = media_news(media)
    print('data_amount: ', len(news_list))
    if len(news_list) == 0:
        return "No data"
    #print的參數
    negative_amount = 0
    neutral_amount = 0
    positive_amount = 0
    # print(news_list)

    #計算最後一篇新聞的時間
    datetime_list = list()
    for news in news_list:
        #印出媒體stance的情況
        if news['stance'] == '1':
            positive_amount += 1
        elif news['stance'] == '0':
            neutral_amount += 1
        else:
            negative_amount += 1

        time =  datetime.strptime(news['post_time'], "%Y/%m/%d %H:%M:%S")
        # if time > datetime(2022,5,10):
        #     continue
        datetime_list.append(time)
    latest_news_time = max(datetime_list)
    # print(latest_news_time)
    # print(datetime_list)
    print('negative: ',negative_amount)
    print('neutral: ', neutral_amount)
    print('positvie: ', positive_amount)
    #計算時間差
    date_differences  = [(latest_news_time - dt).days for dt in datetime_list]
    print("date_differences")
    print(date_differences)
    #計算時間差反比和
    weighted_sum = sum([1/(i+1) for i in date_differences])
    print('weighted_sum')
    print(weighted_sum)
    #計算時間加權stance (可與上面合併)
    weighted_stance_sum = 0
    for index, news in enumerate(news_list):
        weighted_stance = int(news['stance']) / (date_differences[index]+1)
        weighted_stance_sum += weighted_stance
    #加權平均
    return weighted_stance_sum / weighted_sum

#印出特定媒體的立場曲線
def media_trend_plot(media='all'):
    news_list = media_news(media)
    # datetime_data  = [datetime.strptime(news['post_time'], "%Y/%m/%d %H:%M:%S") for news in news_list]
    # values = [int(news['stance']) for news in news_list]
    data = sorted([(datetime.strptime(news['post_time'], "%Y/%m/%d %H:%M:%S"), int(news['stance'])) for news in news_list])
    datetime_data = [d[0] for d in data]
    values = [d[1] for d in data]
    print('image')
    # plt.scatter(datetime_data[:], values[:])
    # plt.title(media)
    # plt.xlabel('date')
    # plt.ylabel('stance')
    return datetime_data[:], values[:]
    # plt.show()
    


#特定媒體的新聞
def media_news(media='all'):
    
    news_list = list()
    if media == 'all':
        news_list = whole_news_list.copy()

    for news in whole_news_list:
        #filter
        time = datetime.strptime(news['post_time'], "%Y/%m/%d %H:%M:%S")
        if time > datetime(2022,5,10):
            continue

        if media == 'all':
            news_list.append(news)
        elif news['source'] == media:
            news_list.append(news)
    return news_list

#計算各家媒體的stance分數
def medias_stance(theshold):
    medias_stance_dict = dict()
    for media, num in media_dict.items():
        if num > theshold:
            if media_stance(media) == "No data":
                continue
            medias_stance_dict[media] = media_stance(media)
    # medias_stance_dict['all'] = media_stance('all')
    return medias_stance_dict
if __name__ == "__main__":
    # num = 0
    # for media in media_dict:
        
    #     if media_dict[media] < 10:
    #         continue
        
    #     print(media)
    #     plt.subplot(2, 4, num%8+1)
    #     datetime_data, values = media_trend_plot(media)
    #     plt.scatter(datetime_data, values)
    #     plt.title(media)
    #     plt.xlabel('date')
    #     plt.ylabel('stance')
    #     num += 1
    #     if num % 8 == 0:
    #         plt.suptitle("Media News Distribution")
    #         plt.show()

########
    num = 0  # Initialize the counter to keep track of the number of plots
    for media in media_dict:
        
        if media_dict[media] < 10:
            continue
        
        # Check if we need to create a new figure
        if num % 4 == 0:
            plt.figure(figsize=(10, 8))  # Adjust the figure size as needed

        print(media)
        plt.subplot(2, 2, num % 4 + 1)  # Adjust the grid to 2x2
        datetime_data, values = media_trend_plot(media)
        plt.scatter(datetime_data, values)
        
        # Rotate the x-axis labels and format the date
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        
        plt.title(media)
        plt.xlabel('date')
        plt.ylabel('stance')
        

        num += 1
        if num % 4 == 0 or num == len(media_dict):
            plt.tight_layout()  # This will automatically adjust subplot params
            plt.suptitle("Media News Distribution", y=1.05)  # Adjust the title position
            plt.show()
    



    
    

    # print(media_stance('自由時報'))

    # medias_stance_dict = medias_stance(theshold = 50)
    # print(medias_stance_dict)

    # #畫條狀圖
    # categories = list(medias_stance_dict.keys())
    # values = list(medias_stance_dict.values())

    # plt.bar(categories, values)
    # plt.title('Bar Chart')
    # plt.xlabel('Media')
    # plt.ylabel('Stance value')
    # plt.xticks(rotation=45)
    # plt.show()
    #target_media = 'SETN 三立新聞網'
    # target_media = '鉅亨網'
    # #  target_media = 'all'
    # print(media_stance(target_media))
    # start_time = time.time()
    # medias_stance(0)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print("执行时间：", execution_time, "秒")
    # # #創造media stance的json
    # with open('medias_stance.json','w',encoding ='utf-8') as jsonfile:
    #     temp_dict = medias_stance(0)
    #     json.dump(temp_dict, jsonfile, ensure_ascii=False, indent=4)

    
