#!/usr/bin/python
# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
from snownlp import SnowNLP

import math
import json
import sys

def load_news_training_data():

	training_set_tf = dict()
	training_set_class = dict()
	keywords = list()

	with open('record.json', 'r', encoding='utf-8') as file:
		news_data = json.load(file)
	for news in news_data:
		training_set_class[news['id']] = news['category']
		#保存每篇文章詞彙出現次數
		#seg_list = jieba.cut(news['content'])
		seg_list = jieba.analyse.extract_tags(news['content'], topK = 20)
		seg_content = {}
		for seg in seg_list:
			if seg in seg_content:
				seg_content[seg] += 1
			else:
				seg_content[seg] = 1
		#保存文章詞彙頻率
		training_set_tf[news['id']] = seg_content	
		#獲取關鍵詞
		keywords.extend(jieba.analyse.extract_tags(news['content'], topK = 20))
	#文章斷詞轉成向量表示
	seg_corpus = list(set(keywords))
	for id in training_set_tf:
		tf_list = list()
		for word in seg_corpus:
			if word in training_set_tf[id]:
				tf_list.append(training_set_tf[id][word])
			else:
				tf_list.append(0)
		training_set_tf[id] = tf_list

	return (training_set_tf, training_set_class, seg_corpus)

def get_article_vector(content, seg_corpus):
    """
    計算要測試的文章向量。
    :param content: 文章內容
    :param seg_corpus: 新聞關鍵詞彙語料庫
    :return: 文章的詞頻向量
    """

    seg_content = {}
    #文章中前tf-idf前20個詞
    seg_list = jieba.analyse.extract_tags(content, topK = 20)
    for seg in seg_list:
        if seg in seg_content:
            seg_content[seg] += 1
        else:
            seg_content[seg] = 1
	#產生vector		one hot vector dimension是seg_corpus的 len

    tf_list = list()
    for word in seg_corpus:
        if word in seg_content:
            tf_list.append(seg_content[word])
        else:
            tf_list.append(0)
    return tf_list

def cosine_similarity(v1, v2):
    """
    計算兩個向量的cosine similarity。數值越高表示距離越近，也代表越相似，範圍為0.0~1.0。
    :param v1: 輸入向量1
    :param v2: 輸入向量2
    :return: 2個向量的正弦相似度
    """
    #compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)
    sum_xx, sum_xy, sum_yy = 0.0, 0.0, 0.0
    for i in range(0, len(v1)):
    	x, y = v1[i], v2[i]
    	sum_xx += math.pow(x, 2)
    	sum_yy += math.pow(y, 2)
    	sum_xy += x * y
    try:
        return sum_xy / math.sqrt(sum_xx * sum_yy)	
    except ZeroDivisionError:
        return 0	

def knn_classify(input_tf, trainset_tf, trainset_class, k):
	"""
	kNN分類演算法。
	:param input_tf: 輸入向量
	:param trainset_tf: 訓練集的向量
	:param trainset_class: 訓練集的分類
	:param k: 決定最近鄰居取k個
	:return:
	"""
	tf_distance = dict()
	# 計算每個訓練集合特徵關鍵字頻率向量和輸入向量的距離
	print ('1.計算向量距離')
	for position in trainset_tf.keys():
		tf_distance[position] = cosine_similarity(trainset_tf.get(position), input_tf)
		#print ('\tDistance(%s) = %f' % (position.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding), tf_distance.get(position)))

	# 取出k個最近距離的分類
	class_count = dict()
	print ('2.K個最近鄰居的分類, k = %d' % k)
	for i, position in enumerate(sorted(tf_distance, key=tf_distance.get, reverse=True)):
		current_class = trainset_class.get(position)
		print ('\t(%s) = %f, class = %s' % (position.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding), tf_distance.get(position), current_class))
		#將最接近的鄰居之分類做加權
		if i == 0:
			class_count[current_class] = class_count.get(current_class, 0) + 2
		else:
			class_count[current_class] = class_count.get(current_class, 0) + 1
		if (i + 1) >= k:
			break

	print ('3.依K個最近鄰居中出現最高頻率的作分類')
	input_class = ''
	for i, c in enumerate(sorted(class_count, key=class_count.get, reverse=True)):
		if i == 0:
			input_class = c
		print ('\t%s, %d' % (c, class_count.get(c)))
	print ('4.分類結果 = %s' % input_class)
	return input_class
def load_test_data(filename):
	with open(filename,"r",encoding = 'utf-8') as f:
		contents = list()
		lines = f.read()
		words = list()
		lines = lines.replace('<?xml version="1.0">','')
		lines = lines.replace('<itemset>','')
		lines = lines.replace('</itemset>','')
		documents = lines.split('</item>')
		for document in documents:
			word = document.split('\n')
			word = list(filter(None, word))
			words.append(word)
		words = list(filter(None, words))    
		for word in words:
			content = str()
			for w in word[1:]:
			   content += w
			contents.append(content)
	return contents
if __name__ == '__main__':
	trainset_tf, trainset_class, seg_corpus = load_news_training_data()
	contents = load_test_data('Shopee2020_classifyTest.txt')
   #contents 是斷詞的字串list
	correct_ans = list("AILEHDTSML")
	
	for k_length in range(5,7):
		my_ans =list()
		for content in contents:
			input_tf = get_article_vector(content, seg_corpus)
			ans = knn_classify(input_tf, trainset_tf, trainset_class, k=k_length)
			my_ans.append(ans)
        break
    
    
		correct_num = 10
		for i in range(10):
			if correct_ans[i]!=my_ans[i]:
				correct_num-=1
		print('k='+str(k_length),end = ' ')
		print(my_ans, end = ' ')
		print(correct_num/10)

			
			
			
			
			
			
			
			
			
			
			
			