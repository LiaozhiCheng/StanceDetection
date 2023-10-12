import matplotlib.pyplot as plt

# 假設您有兩個列表，分別代表 x 軸和 y 軸的數據
x_values = [1027, 1232, 1437, 1642, 1848, 2032, 2216, 2400]
TF_IDF_values = [0.6088,0.6178,0.6505,0.6517,0.6774,0.6784,0.6812,0.6901]
# LSTM_values = [0.5291,0.5262,0.5888,0.5780,0.6022]
BERT_values = [0.6971,0.7251,0.7752,0.7817,0.8254, 0.8314, 0.8425,0.8472]
NORMAL_values = [0.7101,0.7152,0.7212,0.7244,0.7315,0.7451,0.7526,0.7572]
PROPOSED_value = [0.7712,0.7804,0.7852,0.7931,0.8042,0.8234,0.8302,0.8394]
# PROPOSED_BERT_value = [0.7185,0.7452,0.7852,0.8005,0.8216]

# 繪製折線圖
plt.plot(x_values, TF_IDF_values, label='TF-IDF', marker='o')
# plt.plot(x_values, LSTM_values, label='LSTM', marker='s')
plt.plot(x_values, BERT_values, label='BERT', marker='x')
plt.plot(x_values, NORMAL_values, label='Normal', marker='v')
plt.plot(x_values, PROPOSED_value, label='TAMB', marker='^')
# plt.plot(x_values, PROPOSED_BERT_value, label='TAMB+BERT', marker='*')


# 添加標題與標籤
plt.title('Accuracy of each method')
plt.xlabel('Percentage')
plt.ylabel('Amount')

# 顯示圖例
plt.legend(loc = 'lower right')

# 顯示圖形

plt.show()