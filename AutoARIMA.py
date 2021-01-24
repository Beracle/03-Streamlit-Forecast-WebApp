import pandas as pd
import streamlit as st
import numpy as np
from pandas import DataFrame
from pmdarima import auto_arima

def AutoARIMA(df, type, split):
    data = df.sort_index(ascending=True, axis=0)

    train = data[:split]
    valid = data[split:]

    training = train[type]
    validation = valid[type]

    model = auto_arima(training, start_p=1, start_q=1, max_p=3, max_q=3, m=12, start_P=0, seasonal=True, d=1, D=1,
                       trace=True, error_action='ignore', suppress_warnings=True)
    model.fit(training)

    forecast = model.predict(len(df)-split)
    forecast = pd.DataFrame(forecast, index=valid.index, columns=['Prediction'])

    rmse = np.sqrt(np.mean(np.power((np.array(valid[type]) - np.array(forecast['Prediction'])), 2)))
    st.write('RMSE value on validation set:')
    st.write(rmse)

    append_data = DataFrame(data={type: [], 'Predictions': []})

    append_data[type] = training
    append_data['Predictions'] = training

    append_data_2 = DataFrame(data={type: [], 'Predictions': []})

    append_data_2[type] = validation
    append_data_2['Predictions'] = forecast['Prediction']

    pic = pd.concat([append_data[[type, 'Predictions']], append_data_2[[type, 'Predictions']]], axis=0)

    st.line_chart(pic)

