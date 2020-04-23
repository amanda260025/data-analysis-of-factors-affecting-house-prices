# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:31:27 2020

@author: Jack
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

'''
(1)加载数据
'''
import os
os.chdir('C:\\Users\\Jack\\Desktop')
df01=pd.read_csv('house_rent.csv',engine='python')
df02=pd.read_csv('house_sell.csv',engine='python')
#去除缺失值
df01.dropna(inplace=True)
df02.dropna(inplace=True)

'''
(2)计算指标并按照租金、售价汇总数据
'''
df01['rent_area']=df01['price']/df01['area']
data_rent=df01[['community','rent_area','lng','lat']].groupby(by='community').mean()
data_sell=df02[['property_name','average_price','lng','lat']].groupby(by='property_name').mean()
data_rent.reset_index(inplace=True)
data_sell.reset_index(inplace=True)
#数据计算及清洗

data=pd.merge(data_rent,data_sell,left_on='community',right_on='property_name',how='inner')#默认取交集
data=data[['community','lng_x','lat_x','rent_area','average_price']]
data.columns=['community','lng','lat','rent_area','sell_area']#改列名


'''
(3)计算“房屋售租比”(通常200-300是比较合适的)，并做初步判断
要求：
① 计算指标
②绘制直方图、箱型图看“售租比”的一个数据分布情况
'''

data['sell_rent']=data['sell_area']/data['rent_area']
print('上海房屋售租比的中位数为%i个月'%data['sell_rent'].median())

#绘制直方图\箱型图
data['sell_rent'].plot.hist(bins=100,color='green',figsize=(10,4))
data['sell_rent'].plot.box(vert=False,grid=True,figsize=(10,4))

#结论：如果仅靠租金收入的话，上海全市平均回收投资需要725个月（全款买房并且不考虑净现值折算）
#而这种格局的维持，必须有赖于购房者对上海的房价上升的持续预期。

'''
(4)上海市人口密度、路网密度、餐饮价格和“房屋每平米均价”是否有关系呢？
'''
data.to_csv('pro10data.csv',encoding='gbk')#有乱码需要加gbk

'''
(5)加载数据
'''
data_q3=pd.read_csv('result03.csv',engine='python')
data_q3.fillna(0,inplace=True)

'''
(6)指标标准化处理
'''
def f1(data,col):
    return(data[col]-data[col].min())/(data[col].max()-data[col].min())
    
data_q3['人口密度指标']=f1(data_q3,'Z')
data_q3['路网密度']=f1(data_q3,'长度')
data_q3['餐饮价格指标']=f1(data_q3,'人均消费_')#'人均消费_'是用qgis计算出的格网内的平均消费价格

data_q3['离市中心距离']=((data_q3['lng']-353508.848122)**2+(data_q3['lat']-3456140.926976)**2)**0.5

data_q3_test=data_q3[['人口密度指标','路网密度','餐饮价格指标','sell_area_','离市中心距离']]
data_q3_test=data_q3_test[data_q3_test['sell_area_']>0].reset_index()#'sell_area_'是用qgis计算出的每个格网内的平均销售单价
del data_q3_test['index']

'''
(7)作图
'''
plt.figure(figsize=(10,4))
plt.scatter(data_q3_test['人口密度指标'],data_q3_test['sell_area_'],s=2,alpha=0.2)

plt.figure(figsize=(10,4))
plt.scatter(data_q3_test['路网密度'],data_q3_test['sell_area_'],s=2,alpha=0.2)

plt.figure(figsize=(10,4))
plt.scatter(data_q3_test['餐饮价格指标'],data_q3_test['sell_area_'],s=2,alpha=0.2)

plt.figure(figsize=(10,4))
plt.scatter(data_q3_test['离市中心距离'],data_q3_test['sell_area_'],s=2,alpha=0.2)

data_q3_test.corr().loc['sell_area_']


