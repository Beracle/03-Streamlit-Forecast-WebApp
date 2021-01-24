import pandas as pd
import streamlit as st
import numpy as np
from pandas import DataFrame

def KNearestNeighbours(df, type, split):
    # creating dataframe with date and the target variable
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0, len(df)), columns=['Date', type])

    for i in range(0, len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data[type][i] = data[type][i]

    # create features
    from fastai.tabular import add_datepart
    add_datepart(new_data, 'Date')
    new_data.drop('Elapsed', axis=1, inplace=True)  # elapsed will be the time stamp, axis=1表示删除列

    new_data['mon_fri'] = 0
    for i in range(0, len(new_data)):
        if (new_data['Dayofweek'][i] == 0 or new_data['Dayofweek'][i] == 4):
            new_data['mon_fri'][i] = 1
        else:
            new_data['mon_fri'][i] = 0

    # split into train and validation
    train = new_data[:split]
    valid = new_data[split:]

    x_train = train.drop(type, axis=1)
    y_train = train[type]
    x_valid = valid.drop(type, axis=1)
    y_valid = valid[type]

    # importing libraries
    from sklearn import neighbors
    from sklearn.model_selection import GridSearchCV
    from sklearn.preprocessing import MinMaxScaler

    # scaling data
    scaler = MinMaxScaler(feature_range=(0, 1))
    x_train_scaled = scaler.fit_transform(x_train)  # 对x_train进行归一化处理
    x_train = pd.DataFrame(x_train_scaled)
    x_valid_scaled = scaler.fit_transform(x_valid)  # 对x_valid进行归一化处理
    x_valid = pd.DataFrame(x_valid_scaled)

    # using gridsearch to find the best parameter
    params = {'n_neighbors': [2, 3, 4, 5, 6, 7, 8, 9]}
    knn = neighbors.KNeighborsRegressor()
    model = GridSearchCV(knn, params, cv=5)

    # fit the model and make predictions
    model.fit(x_train, y_train)

    preds = model.predict(x_valid)
    rmse = np.sqrt(np.mean(np.power((np.array(y_valid) - np.array(preds)), 2)))
    st.write('RMSE value on validation set:')
    st.write(rmse)

    # plot
    valid['Predictions'] = 0
    valid['Predictions'] = preds

    valid.index = new_data[split:].index
    train.index = new_data[:split].index

    append_data = DataFrame(data={type: [], 'Predictions': []})

    append_data[type] = train[type]
    append_data['Predictions'] = train[type]

    pic = pd.concat([append_data[[type, 'Predictions']], valid[[type, 'Predictions']]], axis=0)

    st.line_chart(pic)


