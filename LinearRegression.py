import pandas as pd
import streamlit as st
import numpy as np
from pandas import DataFrame

def LinearRegression(df, type, split):
    #creating dataframe with date and the target variable
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', type])

    for i in range(0,len(data)):
         new_data['Date'][i] = data['Date'][i]
         new_data[type][i] = data[type][i]

    #create features
    from fastai.tabular import add_datepart
    add_datepart(new_data, 'Date')
    new_data.drop('Elapsed', axis=1, inplace=True)  #elapsed will be the time stamp

    new_data['mon_fri'] = 0
    for i in range(0,len(new_data)):
        if (new_data['Dayofweek'][i] == 0 or new_data['Dayofweek'][i] == 4): #如果是星期一或星期五
            new_data['mon_fri'][i] = 1
        else:
            new_data['mon_fri'][i] = 0

    #split into train and validation
    train = new_data[:split]
    valid = new_data[split:]

    x_train = train.drop(type, axis=1)
    y_train = train[type]
    x_valid = valid.drop(type, axis=1)
    y_valid = valid[type]

    #implement linear regression
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(x_train,y_train)

    preds = model.predict(x_valid)
    rmse = np.sqrt(np.mean(np.power((np.array(y_valid)-np.array(preds)),2)))
    st.write('RMSE value on validation set:')
    st.write(rmse)

    valid['Predictions'] = 0
    valid['Predictions'] = preds

    valid.index = new_data[split:].index
    train.index = new_data[:split].index

    append_data = DataFrame(data={type:[],'Predictions':[]})

    append_data[type] = train[type]
    append_data['Predictions'] = train[type]

    pic = pd.concat([append_data[[type,'Predictions']],valid[[type,'Predictions']]],axis=0)

    st.line_chart(pic)