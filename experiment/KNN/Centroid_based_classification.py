# -*- coding: utf-8 -*-
import math
import jieba
def doc_cen(doc1,doc_dict,my_dict):
    complex_list_word = doc_dict[doc1]
    output_dict = dict()
    
    for word in complex_list_word:  
        tf = dict()
        tf_idf = dict()
        idf = math.log(10000/my_dict[word]['df'],10)
        tf[doc1] = my_dict[word]['inv_list'].count(doc1)

        if tf[doc1] != 0:
            tf[doc1] = 1 + math.log(tf[doc1],10)

        tf_idf[doc1] = tf[doc1] * idf

        output_dict[word] ={'idf': math.log(10000/my_dict[word]['df'],10), doc1:tf_idf[doc1] }
        
    temp_value = dict()
    temp_value[doc1] = 0
    for i in output_dict:
        temp_value[doc1] += math.pow(output_dict[i][doc1],2)
    temp_value[doc1] = math.sqrt(temp_value[doc1])
    for i in output_dict:
        output_dict[i][doc1] /= temp_value[doc1] 
    for i in output_dict:
        output_dict[i] = output_dict[i][doc]
    return output_dict
def vector_cos_sim(v1,v2):
    inner_product = 0
    for i in v1:
        if i in v2:
            inner_product += v1[i]*v2[i]
    v1_len = 0
    for i in v1:
        v1_len +=  v1[i] * v1[i]
    v1_len = math.sqrt(v1_len)
    v2_len = 0
    for i in v2:
        v2_len +=  v2[i] * v2[i]
    v2_len = math.sqrt(v2_len)
    return abs(inner_product / ( v1_len*v2_len ))
    
def cos_sim(doc1,doc2,doc_dict,my_dict):
    complex_list_word = doc_dict[doc1] + doc_dict[doc2]
    output_dict = dict()
    
    for word in complex_list_word:  
        tf = dict()
        tf_idf = dict()
        idf = math.log(10000/my_dict[word]['df'],10)
        tf[doc1] = my_dict[word]['inv_list'].count(doc1)
        tf[doc2] = my_dict[word]['inv_list'].count(doc2)
        if tf[doc1] != 0:
            tf[doc1] = 1 + math.log(tf[doc1],10)
        if tf[doc2] != 0:
            tf[doc2] = 1 + math.log(tf[doc2],10) 
        tf_idf[doc1] = tf[doc1] * idf
        tf_idf[doc2] = tf[doc2] * idf
        output_dict[word] ={'idf': math.log(10000/my_dict[word]['df'],10), doc1:tf_idf[doc1], doc2:tf_idf[doc2] }
        
    temp_value = dict()
    temp_value[doc1] = 0
    temp_value[doc2] = 0
    for i in output_dict:
        temp_value[doc1] += math.pow(output_dict[i][doc1],2)
        temp_value[doc2] += math.pow(output_dict[i][doc2],2)
    temp_value[doc1] = math.sqrt(temp_value[doc1])
    temp_value[doc2] = math.sqrt(temp_value[doc2])
    for i in output_dict:
        output_dict[i][doc1] /= temp_value[doc1] 
        output_dict[i][doc2] /= temp_value[doc2]         
#        sim('48735','48520',output_dict)      
    sim = list()
    sim =[0 for i in range(200)]
    my_count = 0
    for i in output_dict:

        if output_dict[i][doc2] != 0:
        
            sim[my_count] = output_dict[i][doc1] * output_dict[i][doc2]
        else:
            sim[my_count] = 0
        my_count+=1
    print(sum(sim))


with open("Shopee2020_cateBalanced.txt","r",encoding = 'utf-8') as f:
    lines = f.read()

    my_dict = dict()
    catg_dict =dict()
    doc_dict = dict()
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
        header = word[0][1:-1].split(' cateid="')
        my_index = header[0][:-1].replace('item id="','')
        my_categ = header[1][:-1]
        temp = list()
        for w in word[1:]:
           w = w.split(' ')
           for i in w:
                i=jieba.lcut(i)
                temp += i
           temp += w
        doc_dict[my_index] = temp
        if my_categ not in catg_dict:
            catg_dict[my_categ] = list()
        catg_dict[my_categ].append(my_index)
    for word_index,word_list in doc_dict.items():
#        print(word_list)
        for word in word_list:
#            print(word)
            if word in my_dict:
                
                my_dict[word]['inv_list'].append(word_index)
            else:
                my_dict[word] = {'inv_list':[word_index]}
    for key,value in my_dict.items():
        my_dict[key]['df'] = len(set(my_dict[key]['inv_list']))
    catg_avg_vector_dict = dict()
    for ctg in catg_dict:
        avg_vector_dict = dict()
        for doc in catg_dict[ctg]:
            temp_dict = doc_cen(doc,doc_dict,my_dict)
            for i in temp_dict:
                if i not in avg_vector_dict:
                    avg_vector_dict[i] = temp_dict[i]
                else:
                    avg_vector_dict[i] += temp_dict[i]
        for i in avg_vector_dict:
            avg_vector_dict[i] /= len(catg_dict[ctg])
        catg_avg_vector_dict[ctg] = avg_vector_dict
with open('Shopee2020_classifyTest.txt',"r",encoding = 'utf-8') as f:
    lines = f.read()

    my_dict = dict()
    catg_dict =dict()
    doc_dict = dict()
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
        header = word[0][1:-1].split(' cateid="')
        my_index = header[0][:-1].replace('item id="','')
#        my_categ = header[1][:-1]
        
        
        temp = list()
        for w in word[1:]:
           w = w.split(' ')
           for i in w:
                i=jieba.lcut(i)
                temp += i
           temp += w
        doc_dict[my_index] = temp
        if my_categ not in catg_dict:
            catg_dict[my_categ] = list()
        catg_dict[my_categ].append(my_index)
    for word_index,word_list in doc_dict.items():
#        print(word_list)
        for word in word_list:
#            print(word)
            if word in my_dict:
                
                my_dict[word]['inv_list'].append(word_index)
            else:
                my_dict[word] = {'inv_list':[word_index]}
    vector_dict = dict()
    for key,value in my_dict.items():
        my_dict[key]['df'] = len(set(my_dict[key]['inv_list']))
    for doc in doc_dict:
        vector_dict = doc_cen(doc,doc_dict,my_dict)
        max_value = 0 
        predict_ctg = str()
        for ctg in catg_avg_vector_dict:
            sim_val =vector_cos_sim(catg_avg_vector_dict[ctg],vector_dict)
            if sim_val>max_value:
                max_value = sim_val
                predict_ctg = ctg
        print(predict_ctg,end=", ")
        
        
                     
                      
                      
                      
        