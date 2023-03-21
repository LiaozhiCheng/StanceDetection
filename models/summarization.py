# -*- coding: utf-8 -*-
# spaCy 載入中文模型
import spacy
import zh_core_web_lg
# import neuralcoref

nlp = zh_core_web_lg.load()
# neuralcoref.add_to_pipe(nlp)

# summarizer 載入中文模型
from summarizer import Summarizer
from summarizer.text_processors.sentence_handler import SentenceHandler
from spacy.lang.zh import Chinese
from transformers import *

# Load model, model config and tokenizer via Transformers
modelName = "ckiplab/albert-base-chinese" # 可以換成自己常用的
custom_config = AutoConfig.from_pretrained(modelName)
custom_config.output_hidden_states=True
custom_tokenizer = AutoTokenizer.from_pretrained(modelName)
custom_model = AutoModel.from_pretrained(modelName, config=custom_config)

model = Summarizer(
    custom_model=custom_model, 
    custom_tokenizer=custom_tokenizer,
    sentence_handler = SentenceHandler(language=Chinese)
    )

def summarize_sentence(sentence:str, num_sentences:int) -> str:
    result = model(sentence, num_sentences = 1)
    return ''.join(result)





if __name__ == "__main__":
    body = "只不過是打個疫苗，人生怎會因此變調呢？台南有1名郭小姐，原本擔任養生的櫃檯服務員，因為工作需要，去年8月及9月，分別施打「高端」疫苗，第1劑後，她流鼻涕長達1個月，打第2劑後更激烈，竟然全身癱瘓、失明，雖然抽換血漿保住性命，但至今仍然下半身癱瘓，半年多來，都是包尿布臥床，向來與母親相依為命的她，媽媽中風，母女倆只能借錢過活。客廳裡有2張床，施打2劑疫苗後，42歲的郭小姐，就只能包著尿布躺在床上！                                                                                                                         郭小姐：「出意外，我都一直包尿布，然後過得生不如死，我媽又中風，我又癱瘓了，我們家經濟來源都沒有，跟人家借錢來買紙尿布，還有三餐啊，房子給人家租的，1個月又租8千多塊。」原本在養生館擔任櫃台服務員的她，因為工作需要，她在去年8月及9月，分別施打高端疫苗，第1劑打完後，流鼻涕長達1個月，第2劑出現發燒，接著激烈嘔吐，突然癱瘓、失明，半年多來，換了5次血漿，做了10次的神經傳導，才恢復視力，但下半身仍然無法動彈。                                                                                                                                           生活無法自理，她由社會局提供居家長照，每週3次協助洗澡、下床步行、關節運動；每週2次陪同到醫院復健，儘管被通報為疫苗接種不良個案，但案件仍在審理。郭小姐：「畢竟也半年沒有工作了，都四處跟朋友借錢，幾千塊，幾千塊，導致現在朋友都不太敢接我的電話，我現在也求助無門，(政府)還要半年才能整合完畢，才說要賠多少錢啊，我現在也不知道要怎麼辦。」安南醫院神經內科主治醫師邱于禎：「格林巴利症候群，比較常見可能是跟一些病毒感染有關係，另外，有些人在接種疫苗之後也會發生。」郭小姐被診斷罹患「格林巴利症候群」，但是從去年提出救濟案，審查至今都超過半年了，遲遲沒有下文，中央曾說過疫苗審查時間大約三個月，郭小姐到底還要等多久，才能得到公平合理的對待。"

    result = model(body, num_sentences = 1)

    print(result) # 摘要出來的句子
    print(type(result))
    print(''.join(result))