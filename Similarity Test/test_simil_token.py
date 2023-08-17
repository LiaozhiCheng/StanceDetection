import json
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker

print("Initializing drivers ... WS")
ws_driver = CkipWordSegmenter(model="albert-base", device=0)
print("Initializing drivers ... POS")
pos_driver = CkipPosTagger(model="albert-base", device=0)
print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model="albert-base", device=0)
print("Initializing drivers ... all done")

#CKIP去除不重要的詞
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

def read_data(file):
    with open(file, 'r', encoding="utf-8") as reader:
        datas = json.load(reader)

        return [data['title'] for data in datas], [data['body'] for data in datas], [data['summarize'] for data in datas], [int(data['stance']) for data in datas], [int(data['sentiment']) for data in datas]
train_title, train_body, train_summarize, train_stance, train_sentiment = read_data('news_stance_dataset.json')
similar_title_dict = dict()
with open('title_similiar.json', 'r', encoding="utf-8") as json_file:
  similar_title_dict = json.load(json_file)
def get_target_token(text):
    print(text)
    #今天天氣真好
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
    print(simlar_text_list)
    simlar_text_amount = len(simlar_text_list)
    print('相似新聞數量',simlar_text_amount)
    similar_ws_list = list()
    #把相似詞的list做斷詞
    ws = ws_driver(simlar_text_list)
    pos = pos_driver(ws)
    for sentence, sentence_ws, sentence_pos,  in zip(simlar_text_list, ws, pos):
        short= clean(sentence_ws, sentence_pos)
        print(short)
        similar_ws_list.append(short)
    #print(similar_ws_list)
    #常出現的詞有哪些，這邊先用各個詞的出現次數 >= 相似新聞的數量
    ws_frequency_dict = dict()
    for ws_list in similar_ws_list:
        print(ws_list)
        for text_ws in ws_list:
            if text_ws not in ws_frequency_dict:
                ws_frequency_dict[text_ws] = 1
            else:
                ws_frequency_dict[text_ws] += 1
    print(ws_frequency_dict)
    target_token = list()
    for token, frequent in ws_frequency_dict.items():
        if token in text:
            target_token.append(token)
    print("Target Token: ")
    print(target_token)
get_target_token(train_title[0])