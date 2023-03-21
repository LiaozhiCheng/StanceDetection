import json


my_json_list = list()        
with open("Shopee2020_cateBalanced.txt","r",encoding = 'utf-8') as f:
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
        my_index=word[0][1:-1].replace('item id=','')
        temp = my_index.split(' ')
        article_id = temp[0][1:-1]
        category = temp[1][:-1].replace('cateid="','')
        temp = str()
        for w in word[1:]:
           temp += w
        temp_dict = {'id':article_id,'category':category,'content':temp}
        my_json_list.append(temp_dict)
with open('record.json','w',encoding = 'utf-8') as f:
    json.dump(my_json_list,f,ensure_ascii=False)