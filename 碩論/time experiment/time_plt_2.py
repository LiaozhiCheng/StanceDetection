import matplotlib.pyplot as plt

# 假設您有兩個列表，分別代表 x 軸和 y 軸的數據
x_values = [1027, 1232, 1437, 1642, 1848, 2032, 2216, 2400]
# x_values = [int(x*2540) for x in x_values]
TF_IDF_values = [0.6390,0.6664,0.6930,0.6517,0.6774,0.6942, 0.7154, 0.7345]
# LSTM_values = [67.84377145767212, 69.35078406333923, 207.30575275421143, 267.5368275642395, 325.25331020355225]
BERT_values = [34.835,39.732,47.137,48.312,59.343,63.414,67.512,73.497]
NORMAL_values = [0.297,0.390,0.476,0.557,0.657,0.714,0.804,0.921]
PROPOSED_value = [15.2564, 15.3141, 15.5256, 15.7138 ,15.9218, 16.142, 16.365, 16.507]
# PROPOSED_BERT_value = [29.982,35.467,39.69,46.65,61.49]

# 繪製折線圖
plt.plot(x_values, TF_IDF_values, label='TF-IDF', marker='o')
# plt.plot(x_values, LSTM_values, label='LSTM', marker='s')
plt.plot(x_values, BERT_values, label='BERT', marker='x')
plt.plot(x_values, NORMAL_values, label='Non-MB', marker='v')
plt.plot(x_values, PROPOSED_value, label='TAMB', marker='^')
# plt.plot(x_values, PROPOSED_BERT_value, label='TAMB+BERT', marker='*')

# 添加標題與標籤
plt.title('Time Cost of each method')
plt.xlabel('Amount', fontsize=14)
plt.ylabel('Time(sec)',  fontsize=14)

# 顯示圖例
plt.legend(loc = 'upper left', fontsize=14)

# 顯示圖形

plt.show()