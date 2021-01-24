import pandas as pd
import streamlit as st
import numpy as np

def MovingAverage(df, type, split):
    #creating dataframe with date and the target variable
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', type])

    for i in range(0,len(data)):
         new_data['Date'][i] = data['Date'][i]
         new_data[type][i] = data[type][i]

    # splitting into train and validation
    train = new_data[:split]
    valid = new_data[split:]

    # making predictions
    preds = [] #移动平均求出的预测集
    for i in range(0,valid.shape[0]):
        a = train[type][len(train)-248+i:].sum() + sum(preds) #从739开始往后做移动平均
        b = a/248
        preds.append(b)

    # checking the results (RMSE value)
    rms=np.sqrt(np.mean(np.power((np.array(valid[type])-preds),2)))
    st.write('RMSE value on validation set:')
    st.write(rms)

    valid['Predictions'] = 0
    valid['Predictions'] = preds

    append_data = train
    append_data['Predictions'] = train[type]
    append_data = append_data.append(valid)

    append_data.index = append_data['Date']
    append_data.drop('Date', axis=1, inplace=True)

    st.line_chart(append_data)