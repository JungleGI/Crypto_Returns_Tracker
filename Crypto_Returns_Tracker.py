# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 10:40:07 2023

@author: Ulrich
"""

import streamlit as st
import pandas as pd 
from binance.client import Client
client = Client()

def getdata(symbol, start):
    frame = pd.DataFrame(client.get_historical_klines(symbol, '1h', start))
    frame = frame.iloc[:,:5]
    frame.columns = ['Time','Open','High','Low','Close']
    frame.set_index('Time', inplace=True)
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

tickers = ['BTCUSDT','ETHUSDT','SOLUSDT','AVAXUSDT','MATICUSDT','IMXUSDT','RNDRUSDT','TIAUSDT','GALAUSDT','SANDUSDT','FETUSDT','AGIXUSDT','ENJUSDT','APTUSDT','AAVEUSDT','INJUSDT','OCEANUSDT']
#start = '2023-12-01'
start = str(st.date_input('Start', value = pd.to_datetime('2023-12-01')))

df = pd.DataFrame()
for ticker in tickers:
    df_tmp = getdata(ticker,start)
    df_tmp['Ticker'] = ticker
    df = pd.concat([df,df_tmp])

df = df[['Ticker','Close']]
df.columns = ['ticker','price']
df1 = df.pivot_table(index=['Time'],columns='ticker', values=['price'])
df1.columns = [col[1] for col in df1.columns.values]

df_daily_returns = df1.pct_change()
# skip first row with NA 
df_daily_returns = df_daily_returns[1:]

df_cum_daily_returns = (1 + df_daily_returns).cumprod() - 1

Chart1 = df_cum_daily_returns[['BTCUSDT','ETHUSDT','SOLUSDT','AVAXUSDT','MATICUSDT','APTUSDT','INJUSDT']]
Chart2 = df_cum_daily_returns[['BTCUSDT','ETHUSDT','IMXUSDT','GALAUSDT','SANDUSDT','ENJUSDT','OCEANUSDT']]
Chart3 = df_cum_daily_returns[['BTCUSDT','ETHUSDT','RNDRUSDT','TIAUSDT','FETUSDT','AGIXUSDT','AAVEUSDT']]

st.line_chart(Chart1)
st.line_chart(Chart2)
st.line_chart(Chart3)

