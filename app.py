import pandas as pd
import numpy as np
import streamlit as st
from LinearRegression import  LinearRegression
from MovingAverage import MovingAverage
from KNearestNeighbours import KNearestNeighbours
from AutoARIMA import AutoARIMA
from LongShortTM import LongShortTM
import cartoon_html

#------------------------侧边栏------------------------
st.sidebar.image('BigDataCenter.jpg',width=300)
st.sidebar.header("预测分析常用机器学习算法简介")
choose = st.sidebar.selectbox("",('移动平均算法','线性回归算法',
                     '最近邻算法','AutoARIMA算法','LSTM算法'))
if choose == '移动平均算法':
    st.sidebar.write('“平均”是我们日常生活中最常见的事物之一。例如，计算平均分数以确定总体性能，'
             '或者找到过去几天的平均温度以了解当前的温度。')
    st.sidebar.write('移动平均（Moving Average）是用'
             '来衡量当前趋势的方向。移动平均和一般意义下的平均概念是一致的，都是通过计算'
             '过去数据的平均值得到的数学结果。移动平均经常用于金融领域的预测，将计算出'
             '的平均值结果绘制成图标，以便于能够观测平滑的数据，而不是聚焦于所有金融市'
             '场固有的每日价格波动。移动平均可过滤高频噪声，反映出中长期低频趋势，辅助投'
             '资者做出投资判断。')
    st.sidebar.image('MVPicture.png',width=300)
    st.sidebar.write('移动平均不是使用简单的平均值，而是使用移动平均技术，'
             '该技术为每个预测使用最新的一组值。换句话说，对于每个后续步骤，在从集合中删'
             '除最旧的观察值的同时考虑预测值。数据集在不断“移动”。')
    st.sidebar.write('如果您需要进一步了解，请转到我的博客：https://blog.csdn.net/Be_racle/article/details/112600268',unsafe_allow_html=1)
elif choose == '线性回归算法':
    st.sidebar.write('如果您需要进一步了解，请转到我的博客：https://blog.csdn.net/be_racle/article/details/112604437', unsafe_allow_html=1)
elif choose == '最近邻算法':
    st.sidebar.write('如果您需要进一步了解，请转到我的博客：https://blog.csdn.net/be_racle/article/details/112747349', unsafe_allow_html=1)
elif choose == 'AutoARIMA算法':
    st.sidebar.write('如果您需要进一步了解，请转到我的博客：https://blog.csdn.net/be_racle/article/details/112780195', unsafe_allow_html=1)
elif choose == 'LSTM算法':
    st.sidebar.write('如果您需要进一步了解，请转到我的博客：https://blog.csdn.net/be_racle/article/details/112999853', unsafe_allow_html=1)

#---------------------------正文-----------------------
cartoon_html.cartoon_html()

st.subheader('1.读入数据')
df = pd.read_csv('NSE-TATAGLOBAL11.csv')
st.dataframe(df)

st.subheader('2.选择时间序列')
options = np.array(df['Date']).tolist()

(start_time, end_time) = st.select_slider("请选择时间序列长度：",
     #min_value = datetime(2013, 10, 1,),
     #max_value = datetime(2018, 10, 31,),
     options = options,
     value= ('2016-05-04','2014-06-27',),
 )
st.write("时间序列开始时间:",end_time)
st.write("时间序列结束时间:",start_time)

#setting index as date
df['Date'] = pd.to_datetime(df.Date, format = '%Y-%m-%d')
df.index = df['Date']

df = df[start_time:end_time]
st.dataframe(df)

st.subheader('3.训练集划分')
number = st.number_input("请输入训练集所占比例：",min_value=0.5,max_value=0.9,value=0.8,step=0.1)
split = int(number * len(df))
st.write("选择的数据集大小：",len(df))
st.write("训练集大小：",split)
st.write("预测集大小：",len(df)-split)

st.subheader('4.选择预测目标')
type = st.selectbox('请选择预测目标：',('Close','Turnover'))
st.line_chart(df[type])

st.subheader('5.选择机器学习算法')
genre = st.selectbox("请选择时间序列预测算法",
     ('移动平均算法', '线性回归算法', '最近邻算法', 'AutoARIMA算法', 'LSTM算法'))
if genre == '移动平均算法':
    MovingAverage(df, type, split)
elif genre == '线性回归算法':
     LinearRegression(df, type, split)
elif genre == '最近邻算法':
     KNearestNeighbours(df, type, split)
elif genre == 'AutoARIMA算法':
    AutoARIMA(df, type, split)
elif genre == 'LSTM算法':
    LongShortTM(df, type, split)


