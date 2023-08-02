import pandas as pd
import numpy as nd

from main import goods1

goods_ABC = pd.pivot_table(goods1, index=['ITEM NUMBER'], values=['SUM'], aggfunc=nd.sum).sort_values(by=['SUM'], ascending=False)
goods_ABC['SUM_p'] = goods_ABC['SUM'] / goods_ABC['SUM'].sum()

print("\n\nСводная для ABC  : \n {}".format(goods_ABC['SUM_p'].cumsum().head(10)))

gr = ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
ind = range(1, 11)
df = pd.goods1({'ITEM NUMBER': ind, 'группа': gr})
print(df, '\n')
