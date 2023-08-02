"""
Проект
"""

import numpy as nd
import matplotlib.pyplot as plt
import pandas as pd


#Для отражения всех столбцов
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', '{:.2f}'.format)

#Чтение таблицы
goods = pd.read_csv('Товародвижение22.csv')

#Выявление дубликатов
Dup_Rows = goods[goods.duplicated()]

#Удаление дубликатов, сохранив только последнее вхождение
DF_RM_DUP = goods.drop_duplicates(keep='last')

#Статистика продаж
#Общий объем продаж(код 251 - Продажа)
#в разрезе товара
goods1 = goods.loc[(goods['TYPE MOVEMENT'] == '251')]
goods2 = pd.pivot_table(goods1, index=['ITEM NUMBER', 'TYPE MOVEMENT'], values=['SUM'], aggfunc='sum')

#в разрезе товара и дня
goods3 = pd.pivot_table(goods1, index=['DATA', 'TYPE MOVEMENT'], values=['SUM'], aggfunc='sum')

#Статистика возврата и списаний товара
"""
901 - Возврат товара,
909 - Поступление для переклассификации товара,
910 - Списание для пр-ва,
Z79 - ОМ для списания,
Z80 - Сторно ОМ для списания.

"""
#в разрезе товара
goods4 = goods.loc[(goods['TYPE MOVEMENT'] >= '900')]
goods5 = pd.pivot_table(goods4, index=['ITEM NUMBER', 'TYPE MOVEMENT'], values=['SUM'], aggfunc='sum')
goods6 = pd.pivot_table(goods4, index=['ITEM NUMBER', 'TYPE MOVEMENT'], values=['AMOUNT'], aggfunc='sum')

#в разрезе дня, вида движения и товара
goods7 = pd.pivot_table(goods4, index=['ITEM NUMBER', 'TYPE MOVEMENT'], columns=['DATA'], values=['SUM'], aggfunc='sum', fill_value=0)
goods8 = goods7.dropna(how='all')

#в разрезе дня по видам движения
goods9 = pd.pivot_table(goods4, index=['TYPE MOVEMENT'], columns=['DATA'], values=['SUM'], aggfunc='sum', fill_value=0)

#График
#Продажи по дням товара с max выручкой
goods10 = goods.loc[((goods['TYPE MOVEMENT'] == '251')&(goods['ITEM NUMBER'] == 103303))]
goods11 = pd.pivot_table(goods10, index=['DATA'], values=['SUM'], aggfunc='sum', fill_value=0)

#goods11.plot(kind='bar')
#plt.xticks(rotation=45)
#plt.show()

#Списания товара по дням
goods12 = pd.pivot_table(goods4, index=['DATA'], columns=['TYPE MOVEMENT'], values=['SUM'], aggfunc='sum')

#goods12.plot(kind='barh')
#plt.xticks(rotation=45)
#plt.show()


#ABC-анализ
goods_ABC = pd.pivot_table(goods1, index=['ITEM NUMBER'], values=['SUM'], aggfunc=nd.sum).sort_values(by=['SUM'], ascending=False)
goods_ABC['SUM_p'] = goods_ABC['SUM'] / goods_ABC['SUM'].sum()

#plt.plot(goods_ABC['SUM_p'].cumsum().head(5))
#plt.title('Кривая Парето (кривая Лоренца или ABC-кривая)')
#plt.show()

top_goods_10 = goods_ABC[goods_ABC['SUM_p'].cumsum() < 0.7]

#XYZ-анализ
goods_XYZ = pd.pivot_table(goods1, index=['ITEM NUMBER', 'DATA'], values=['SUM'], aggfunc=[nd.sum, nd.mean, nd.std])
goods_XYZ_1 = goods1[goods1['ITEM NUMBER'] == 103303]
goods_XYZ_goods = pd.pivot_table(goods1, index=['ITEM NUMBER'], values=['SUM'], aggfunc=[nd.sum, nd.mean, nd.std])

#Потребность в запасе
#продажа с артикулом 103303 20210101 360шт,
#необходимо оповещение на @ о закупке, если запас меньше max значения по продажам.
#«НЕТ», если запас > (max)
#«ДА», если запас < max
goods_reserve = pd.pivot_table(goods10, index=['DATA'], values=['AMOUNT'], aggfunc='sum', fill_value=0)
goods_max_AMOUNT = goods_reserve['AMOUNT'].max()
goods_reserve['reserve'] = nd.where(goods_reserve['AMOUNT'] < goods_max_AMOUNT, 'yes', 'no')

#Сбор в файл сводных таблиц
goods_sheets = {'Выручка': goods3, 'Списание возврат': goods5, 'ABC': goods_ABC, 'Потребность запас': goods_reserve}
writer = pd.ExcelWriter(r'C:\Users\selivanova\Desktop\HM Python\ProjectPP\Сводные.xlsx', engine='xlsxwriter')
for sheet_name in goods_sheets.keys():
    goods_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)

writer.save()


def main():
    # Вывод данных заруженной таблицы
    print("\n\nДанные товародвижения за период : \n {}".format(goods))
    # Информация по столбцам:
    # print(goods.info())
    print("\n\nИнформация по столбцам таблицы за период : \n {}".format(goods.info()))
    # Описание данных
    # print(goods.describe())
    print("\n\nСтатистика по таблице за период : \n {}".format(goods.describe()))
    # Выявление дубликатов
    print("\n\nПовторяющиеся строки : \n {}".format(Dup_Rows))
    # Удаление дубликатов, сохранив только последнее вхождение
    print('\n\nРезультирующий кадр данных после удаления дубликата :\n', DF_RM_DUP.head(n=5))
    # Статистика продаж
    # Общий объем продаж(код 251 - Продажа)
    # в разрезе товара
    print("\n\nСводная объема продаж в разрезе товара MAX-значения за период  : \n {}".format(
        goods2[goods2['SUM'] == goods2['SUM'].max()],
    ))
    print("\n\nСводная объема продаж в разрезе товара MIN-значения за период  : \n {}".format(
        goods2[goods2['SUM'] == goods2['SUM'].min()],
    ))
    # в разрезе товара и дня
    print("\n\nСводная выручки MAX-значения за день  : \n {}".format(
        goods3[goods3['SUM'] == goods3['SUM'].max()],
    ))
    print("\n\nСводная выручки MIN-значения за день  : \n {}".format(
        goods3[goods3['SUM'] == goods3['SUM'].min()],
    ))
    # Статистика возврата и списаний товара
    # в разрезе товара
    print("\n\nСводная возврата, списаний в разрезе суммы MAX-значения за период  : \n {}".format(
        goods5[goods5['SUM'] == goods5['SUM'].max()],
    ))
    print("\n\nСводная возврата, списаний в разрезе количества товара MAX-значения за период  : \n {}".format(
        goods6[goods6['AMOUNT'] == goods6['AMOUNT'].max()],
    ))
    # в разрезе дня, вида движения и товара
    print("\n\nСводная возврата, списаний в разрезе количества товара MAX-значения за период  : \n {}".format(goods8))
    # в разрезе дня по видам движения
    print("\n\nСводная возврата, списаний в разрезе количества товара MAX-значения за период  : \n {}".format(goods9))
    # График
    # Продажи по дням товара с max выручкой
    print("\n\nСводная для графика  : \n {}".format(goods11))
    # ABC-анализ
    print("\n\nСводная для ABC  : \n {}".format(goods_ABC['SUM_p'].cumsum().head(10)))
    print("\n\nСводная для ABC 1 : \n {}".format(goods_ABC.reset_index()))
    print("\n\nСводная для ABC  топ 10: \n {}".format(top_goods_10))
    # XYZ-анализ
    print("\n\nСводная для XYZ_1  : \n {}".format(goods_XYZ_1))
    print("\n\nСводная для XYZ_goods  : \n {}".format(goods_XYZ_goods))
    # Потребность в запасе
    print("\n\nСводная для расчета запаса : \n {}".format(goods_reserve))

if __name__ == '__main__':
    main()

