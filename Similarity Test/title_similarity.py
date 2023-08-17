from sentence_transformers import SentenceTransformer, util
import json
import time

print("hello")
start_time = time.time()
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')  # 多語言模型
#paraphrase-multilingual-MiniLM-L12-v2
def read_data(file):
    with open(file, 'r', encoding="utf-8") as reader:
        datas = json.load(reader)

        return [data['title'] for data in datas]
    
data_file = 'news_stance_dataset.json'
sentences = read_data(data_file)

embedding = model.encode(sentences, convert_to_tensor=False)

cosine_scores = util.cos_sim(embedding, embedding)

end_time = time.time()
execution_time = end_time - start_time
print("执行时间：", execution_time, "秒")
similar_title_dict = dict()

for i,target in enumerate(sentences):
    for j,compare_sentence in enumerate(sentences):
        if target not in similar_title_dict:
            similar_title_dict[target] = [(compare_sentence, float(cosine_scores[i][j]))]
        else:
            similar_title_dict[target].append((compare_sentence, float(cosine_scores[i][j])))

for key, value in similar_title_dict.items():
    similar_title_dict[key] = sorted(value, reverse=True)

end_time = time.time()
execution_time = end_time - start_time
print("执行时间：", execution_time, "秒")
with open('title_similiar.json', 'w', encoding="utf-8") as json_file:
    json.dump(similar_title_dict, json_file, ensure_ascii=False, indent=4)