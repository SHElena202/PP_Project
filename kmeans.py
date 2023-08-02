#Применение кластеризации
import pandas as pd
from matplotlib import pyplot as plt
from pandas import pivot_table
from sklearn.cluster import KMeans

from main import goods1, goods12

kmeans = KMeans(n_clusters=5)
labels = kmeans.fit_predict(goods1)
pivot_table["category"] = kmeans.labels_
ABC_dict = {
    0: "A",
    1: "C",
    2: "B"
}
pivot_table["ABC"] = pivot_table['category'].apply(lambda x: ABC_dict[x])
goodsN = pd.merge(goods12, pivot_table, on='rev_dist', how='left')
goods_SUM = goodsN.groupby(['ABC'])['SUM'].sum()
plt.pie(goods_SUM, explode=(0.05, 0, 0), autopct='%1.1f%%', shadow=False, startangle=90, colors=['mediumseagreen', 'grey', 'lightblue'], labeldistance=1.15, wedgeprops={'linewidth': 3, 'edgecolor': 'white'})
plt.show()

goods_AMOUNT = goodsN.groupby(['ABC'])['AMOUNT'].count()
plt.pie(goods_AMOUNT, explode=(0.05, 0, 0), autopct='%1.1f%%', shadow=False, startangle=90, colors=['mediumseagreen','grey', 'lightblue'], labeldistance=1.15, wedgeprops={'linewidth': 3, 'edgecolor': 'white'})
plt.show()