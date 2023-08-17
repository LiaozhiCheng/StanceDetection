from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
import json


sentence_ws_dict = dict()

#讀欲更新檔案
news_stance_dataset = list()
with open('news_stance_dataset.json', 'r', encoding="utf-8") as json_file:
    news_stance_dataset = json.load(json_file)

#讀相似新聞的檔案
similar_title_dict = dict()
with open('title_similiar.json', 'r', encoding="utf-8") as json_file:
    similar_title_dict = json.load(json_file)


#載入CKIP模型
print("Initializing drivers ... WS")
ws_driver = CkipWordSegmenter(model="albert-base", device=0)
print("Initializing drivers ... POS")
pos_driver = CkipPosTagger(model="albert-base", device=0)
print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model="albert-base", device=0)
print("Initializing drivers ... all done")

#CKIP去除不重要的詞function
def clean(sentence_ws, sentence_pos):
  short_with_pos = []
  short_sentence = []
  stop_pos = set(['Nep', 'Nh', 'Nb']) # 這 3 種詞性不保留
  for word_ws, word_pos in zip(sentence_ws, sentence_pos):
    # 只留名詞和動詞
    is_N_or_V = word_pos.startswith("V") or word_pos.startswith("N")
    # 去掉名詞裡的某些詞性
    is_not_stop_pos = word_pos not in stop_pos
    # 只剩一個字的詞也不留
    is_not_one_charactor = not (len(word_ws) == 1)
    # 組成串列
    if is_N_or_V and is_not_stop_pos and is_not_one_charactor:
      short_sentence.append(f"{word_ws}")
  return short_sentence

def build_sentence_ws_dict():

    sentence_list = [data['title'] for data in news_stance_dataset]
    #把相似詞的list做斷詞
    ws = ws_driver(sentence_list)
    pos = pos_driver(ws)
    for sentence, sentence_ws, sentence_pos,  in zip(sentence_list, ws, pos):
        short= clean(sentence_ws, sentence_pos)
        sentence_ws_dict[sentence] = short
#版本2
def get_target_token_2(text):
    #print(text)
    #simlar_text_list 相似的新聞list
    simlar_text_list = list()
    if text not in similar_title_dict:
        return list()
    if text in similar_title_dict:
        candidate_list = similar_title_dict[text]
        for value in candidate_list:
            canidate_sentence = value[0]
            cosine_value = value[1]
            if cosine_value > 0.8 and cosine_value < 0.999:
                simlar_text_list.append(canidate_sentence)
    simlar_text_amount = len(simlar_text_list)

    #print('相似新聞數量',simlar_text_amount)
    similar_ws_list = list()
    #把相似詞的list做斷詞
    for temp_text in simlar_text_list:
        if temp_text in sentence_ws_dict:
            similar_ws_list.append(sentence_ws_dict[temp_text])
        else:
            print(temp_text)
    #print(similar_ws_list)

    input_ws_list = sentence_ws_dict[text]
    #常出現的詞有哪些，這邊先用各個詞的出現次數 >= 相似新聞的數量
    ws_frequency_dict = dict()
    for ws_list in similar_ws_list:

        for text_ws in ws_list:
            if text_ws not in ws_frequency_dict:
                ws_frequency_dict[text_ws] = 1
            else:
                ws_frequency_dict[text_ws] += 1
    # print('input_ws_list:')
    # print(input_ws_list)
    
    target_token = list()
    for token, frequent in ws_frequency_dict.items():
        if token in input_ws_list:
            # print(token)
            target_token.append(token)

    return target_token

news_stance_token_dataset = list()
build_sentence_ws_dict()
for data in news_stance_dataset:
    try:
        target_token = get_target_token_2(data['title'])
        data['target_token'] = target_token
    except:
        print(data['title'])
    #print(data['target_token'])
    news_stance_token_dataset.append(data)
# print('sentence_ws:')
# print(sentence_ws_dict['挺國產！彰化開打高端疫苗 花壇僅2人爽約'])
# print(get_target_token_2('挺國產！彰化開打高端疫苗 花壇僅2人爽約'))

with open('news_stance_token_dataset_v2.json', 'w', encoding = 'utf-8')as json_file:
    json.dump(news_stance_token_dataset, json_file, ensure_ascii=False, indent=4)