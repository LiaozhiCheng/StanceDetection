import spacy


nlp = spacy.load("zh_core_web_sm")
#zh_core_web_sm for efficiency
#zh_core_web_trf for accurancy

word_vec = nlp("學校").vector
print(word_vec)