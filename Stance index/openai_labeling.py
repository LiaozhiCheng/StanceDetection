import openai
import json

# 設置 OpenAI API 密鑰
openai.api_key = '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'


# 定義函式以獲取情感分數
def get_sentiment_score(text):
    prompt = "情感：1,0,-1\n\n標題：" + text + "\n情感："
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=128,
        temperature=0,
        n=1,
        stop=None
    )
    sentiment = response.choices[0].text.strip()
    # print(response)
    return sentiment

# 讀取新聞標題資料
with open('news_stance_dataset.json', 'r') as file:
    news_stance_dataset = json.load(file)

# 進行情感標註
labeled_data = []
for news in news_stance_dataset:
    sentiment = get_sentiment_score(news['title'])
    if sentiment == '1':
        labeled_data.append({'title': news['title'], 'implict_sentiment': '正面'})
    elif sentiment == '-1':
        labeled_data.append({'title': news['title'], 'implict_sentiment': '負面'})
    else:
        labeled_data.append({'title': news['title'], 'implict_sentiment': '中立'})

# 儲存標註結果
with open('labeled_data.json', 'w') as json_file:
    json.dump(labeled_data, json_file, indent=4)