from pymongo import MongoClient
import math 
from datetime import datetime
DB = MongoClient('mongodb://localhost:27017')['Media_data']
NEWS_COLLECTION = DB['news_raw']

test_news_1 = NEWS_COLLECTION.find_one({'title':'美日防長5/4會晤 聚焦中國、俄烏與防衛合作'})
time_1 = test_news_1['post_time']
time_1 = datetime.strptime(time_1, "%Y/%m/%d %H:%M:%S")
print(time_1)
print(type(time_1))

test_news_2 = NEWS_COLLECTION.find_one({'title':'日本迄未採認高端疫苗 吳釗燮親與日代表協商'})
time_2 = test_news_2['post_time']
time_2 = datetime.strptime(time_2, "%Y/%m/%d %H:%M:%S")
print(time_2)
print(type(time_2))

#日期差
time_difference = time_2 - time_1
print(time_difference.days)

#最晚的時間
datetime_list = [
    datetime(2022, 5, 1, 0, 0, 0),
    datetime(2022, 5, 3, 7, 49, 58),
    datetime(2022, 4, 28, 12, 30, 0)
]

# 使用 max() 函数找到最晚的时间
latest_datetime = max(datetime_list)