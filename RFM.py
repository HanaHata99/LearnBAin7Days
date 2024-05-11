#RFM
import pandas as pd

df['Thời gian tạo đơn'] = pd.to_datetime(df['Thời gian tạo đơn'])

current_date = pd.to_datetime('now')

# Tính Recency bằng cách tính số ngày kể từ ngày gần nhất tạo đơn đến hiện tại
recency = current_date - df.groupby('Mã khách hàng')['Thời gian tạo đơn'].max()

# Tính Frequency bằng số lượng đơn hàng của mỗi khách hàng
frequency = df.groupby('Mã khách hàng').size()

# Tính Monetary bằng tổng số tiền mỗi khách hàng đã chi
monetary = df.groupby('Mã khách hàng')['Thành tiền'].sum()

# Gộp các chỉ số RFM lại thành một DataFrame
rfm_table = pd.concat([recency, frequency, monetary], axis=1)
rfm_table.columns = ['Recency', 'Frequency', 'Monetary']

# Thực hiện chia các giá trị RFM theo thang điểm 1-5
def assign_rfm_score(x, col):
    if x <= col.quantile(0.2):
        return 5
    elif x <= col.quantile(0.4):
        return 4
    elif x <= col.quantile(0.6):
        return 3
    elif x <= col.quantile(0.8):
        return 2
    else:
        return 1

rfm_table['Recency_Score'] = rfm_table['Recency'].apply(assign_rfm_score, args=(rfm_table['Recency'],))
rfm_table['Frequency_Score'] = rfm_table['Frequency'].apply(assign_rfm_score, args=(rfm_table['Frequency'],))
rfm_table['Monetary_Score'] = rfm_table['Monetary'].apply(assign_rfm_score, args=(rfm_table['Monetary'],))

# Tạo cột RFM_Segment bằng cách kết hợp các điểm RFM
rfm_table['RFM_Segment'] = rfm_table['Recency_Score'].astype(str) + rfm_table['Frequency_Score'].astype(str) + rfm_table['Monetary_Score'].astype(str)

# Phân loại khách hàng vào các nhóm RFM tương ứng
def assign_rfm_label(segment):
    if segment in ['555', '554', '545', '544', '455', '454', '445', '444']:
        return 'Champion'
    elif segment in ['543', '542', '541', '534', '533', '532', '531', '524', '523', '522', '521', '515', '514', '513', '435', '434', '433', '432', '431']:
        return 'Loyal Customer'
    elif segment in ['553', '552', '551', '425', '424', '423', '422', '421', '415', '414', '413', '412', '411', '315', '314', '313', '312', '311']:
        return 'Potential Loyalist'
    elif segment in ['522', '521', '515', '514', '513', '435', '434', '433', '432', '431']:
        return 'Promising'
    elif segment in ['535', '534', '443', '434', '343', '334', '325', '324']:
        return 'Need Attention'
    elif segment in ['155', '154', '144', '214', '215', '115', '114', '113']:
        return 'Cannot Lose Them'
    elif segment in ['331', '321', '312', '221', '213']:
        return 'About To Sleep'
    elif segment in ['255', '254', '245', '244', '253', '252', '243', '242', '235', '234', '225', '224', '153', '152', '145', '143', '142', '135', '134', '133', '125', '124']:
        return 'At Risk'
    elif segment in ['332', '322', '231', '241', '251', '233', '232', '223', '222', '132', '123', '122', '212', '211']:
        return 'Hibernating'
    else:
        return 'Lost'

rfm_table['RFM_Label'] = rfm_table['RFM_Segment'].apply(assign_rfm_label)

print(rfm_table[['Recency', 'Frequency', 'Monetary', 'RFM_Segment', 'RFM_Label']])




import matplotlib.pyplot as plt
import squarify

# Tạo DataFrame chỉ chứa số lượng khách hàng theo nhãn RFM
rfm_label_counts = rfm_table['RFM_Label'].value_counts()

# Tính phần trăm cho mỗi nhóm RFM
total_customers = rfm_label_counts.sum()
rfm_label_percentages = (rfm_label_counts / total_customers) * 100
rfm_label_percentages = rfm_label_percentages.round(1)

colors = {
    'Champion': '#006400',            # Màu xanh lá đậm
    'Loyal Customer': '#228B22',      # Màu xanh lá lợt hơn Champion
    'Potential Loyalist': '#32CD32',  # Màu xanh lá lợt hơn Loyal Customer
    'New Customer': '#00FF00',        # Màu xanh mạ
    'Promising': '#ADFF2F',           # Màu xanh lá nghiên vàng
    'Need Attention': '#FFFF00',      # Màu vàng chói
    'Cannot Lose Them': '#FFD700',     # Màu vàng đậm hơn Need Attention
    'About To Sleep': '#FFA500',       # Màu vàng ngả cam
    'At Risk': '#FF4500',              # Màu cam
    'Hibernating': '#FF0000',          # Màu đỏ chói
    'Lost': '#8B0000'                  # Màu đỏ đô đậm
}
colors_mapped = [colors[label] for label in rfm_label_counts.index]


plt.figure(figsize=(10, 6))
squarify.plot(sizes=rfm_label_counts.values, label=[f'{label}\n({percentage}%)' for label, percentage in zip(rfm_label_counts.index, rfm_label_percentages)], color=colors_mapped, alpha=0.7)
plt.axis('off')
plt.title('Biểu đồ tree map 1.3.2.1 Tỷ lệ phần trăm mỗi nhóm RFM')
plt.show()






import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.barh(rfm_label_counts.index, rfm_label_counts.values, color=colors_mapped)

for i, value in enumerate(rfm_label_counts.values):
    plt.text(value, i, str(value), ha='left', va='center', fontsize=10)

plt.xlabel('Số lượng khách hàng')
plt.ylabel('Nhãn RFM')
plt.title('Biểu đồ 1.3.2.2 Tổng số lượng khách hàng theo nhãn RFM')
plt.gca().invert_yaxis()

plt.show()






average_monetary_sorted = average_monetary.sort_values(ascending=False)
average_frequency_sorted = average_frequency.sort_values(ascending=False)

# Map colors
sorted_colors_monetary = {k: colors[k] for k in average_monetary_sorted.index}
sorted_colors_frequency = {k: colors[k] for k in average_frequency_sorted.index}

fig, axs = plt.subplots(1, 2, figsize=(16, 6))

# Average monetary value of each RFM segment
average_monetary_sorted.plot(kind='barh', color=sorted_colors_monetary.values(), ax=axs[0])
axs[0].set_xlabel('Average Monetary Value (M đ)')
axs[0].set_ylabel('RFM Segment')
axs[0].set_title('Average Monetary Value by RFM Segment')
axs[0].invert_yaxis()

# Average frequency of each RFM segment
average_frequency_sorted.plot(kind='barh', color=sorted_colors_frequency.values(), ax=axs[1])
axs[1].set_xlabel('Average Frequency')
axs[1].set_ylabel('RFM Segment')
axs[1].set_title('Average Frequency by RFM Segment')
axs[1].invert_yaxis()

plt.suptitle('Biểu đồ 1.3.2.3: Doanh thu trung bình và tần suất mua bình quân của từng nhóm RFM', fontsize=16)

plt.tight_layout()
plt.show()
