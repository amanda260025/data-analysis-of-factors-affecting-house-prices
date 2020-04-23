# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:02:26 2020

@author: Jack
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

'''
(1)按照离市中心距离来分析指标相关性
'''
dis=[]
rkmd_pearson=[]
lwmd_pearson=[]
cyjg_pearson=[]
zxjl_pearson=[]

#按照离市中心距离每10km
for distance in range(10000,70000,10000):
    datai=data_q3_test[data_q3_test['离市中心距离']<=distance]
    r_value=datai.corr().loc['sell_area_']#只取和销售单价之间的相关系数
    #print(r_value)
    dis.append(distance)
    rkmd_pearson.append(r_value.loc['人口密度指标'])
    lwmd_pearson.append(r_value.loc['路网密度'])
    cyjg_pearson.append(r_value.loc['餐饮价格指标'])
    zxjl_pearson.append(r_value.loc['离市中心距离'])
    print('离市中心距离小于等于%i米时：'%distance)
    print('数据量为%i条'%len(datai))
    print('人口指标相关系数为:%.3f'%r_value.loc['人口密度指标'])
    print('路网密度指标相关系数为:%.3f'%r_value.loc['路网密度'])
    print('餐饮价格指标相关系数为:%.3f'%r_value.loc['餐饮价格指标'])
    print('离市中心距离指标相关系数为:%.3f'%r_value.loc['离市中心距离'])
    print('-------\n')
    
'''
(2)bokeh制图
'''

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool

output_file('C:\\Users\\Jack\\Desktop\\pro10.html')
df_r=pd.DataFrame({'rkmd_pearson':rkmd_pearson,
                   'lwmd_pearson':lwmd_pearson,
                   'cyjg_pearson':cyjg_pearson,
                   'zxjl_pearson':zxjl_pearson},index=dis)

source=ColumnDataSource(df_r)
hover=HoverTool(tooltips=[('离市中心距离','@index'),
                          ('人口密度相关系数','@rkmd_pearson'),
                          ('路网密度相关系数','@lwmd_pearson'),
                          ('餐饮价格相关系数','@cyjg_pearson'),
                          ('中心距离相关系数','@zxjl_pearson')])

p=figure(plot_width=900,plot_height=350,title='随着市中心距离增加，不同指标相关系数变化情况',
         tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
p.line(x='index',y='rkmd_pearson',source=source,line_alpha=0.8,line_color='green',line_dash=[15,5],legend='人口相关系数')
p.circle(x='index',y='rkmd_pearson',source=source,size=8,color='green',legend='人口相关系数')


p.line(x='index',y='lwmd_pearson',source=source,line_alpha=0.8,line_color='blue',line_dash=[15,5],legend='道路密度相关系数')
p.circle(x='index',y='lwmd_pearson',source=source,size=8,color='blue',legend='道路密度相关系数')

p.line(x='index',y='cyjg_pearson',source=source,line_alpha=0.8,line_color='black',line_dash=[15,5],legend='餐饮价格相关系数')
p.circle(x='index',y='cyjg_pearson',source=source,size=8,color='black',legend='餐饮价格相关系数')

p.line(x='index',y='zxjl_pearson',source=source,line_alpha=0.8,line_color='red',line_dash=[15,5],legend='中心距离相关系数')
p.circle(x='index',y='zxjl_pearson',source=source,size=8,color='red',legend='中心距离相关系数')

p.legend.location='center_right'
show(p)
#① “人口密度”、“道路密度”、“离市中心距离”和“房屋均价”有着明显的相关性，而“餐饮价格”和“房屋均价”的相关性较弱
#②随着离市中心的距离越远，指标的相关性在数据上体现更明显，而这个分界线大概在20-30km处，这正是上海中心城区和郊区的分界 → 上海房价市场的“中心城区-郊区”分化特征
#③中心城区的房产市场对指标因素的影响更加敏锐，而郊区则更迟钝 → 越靠近市中心，影响因素越复杂，而越靠近郊区，复杂的因素越少，而人口、道路密度、餐饮等指标的占比增大，成为主要影响因素后，相关程度也更加稳定。

