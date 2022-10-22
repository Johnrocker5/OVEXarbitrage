import requests
import yfinance as yf
import datetime
import pymysql
import pandas as pd
import streamlit as st
import numpy as np
import json


def convert_datetime(x):
    year = int(x[0:2]) + 2000
    month = int(x[3:5])
    day = int(x[6:8])
    hour = int(x[9:11])
    minute = int(x[12:14])
    time = datetime.datetime(year=year, month=month, day=day,
                             hour=hour, minute=minute)
    return time


def convert_floats(x):
    ans = float(x)
    return ans


def convert_int(x):
    if x == 1:
        ans = True
    if x == 0:
        ans = False
    return ans


def get_data():
    cnx = pymysql.connect(
        host=st.secrets.mysql.host,
        user=st.secrets.mysql.user,
        password=st.secrets.mysql.password,
        database=st.secrets.mysql.database,
        port=st.secrets.mysql.port,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = cnx.cursor()
    query1 = ('select * from spreads')
    cursor.execute(query1)
    rawData = cursor.fetchall()
    jsonData = json.dumps(rawData)
    jsonStringList = json.loads(jsonData)
    df = pd.json_normalize(jsonStringList)
    df['time'] = df['time'].apply(convert_datetime)
    df['spread_spot'] = df['spread_spot'].astype('float')
    df['spread_fx'] = df['spread_fx'].astype('float')
    df['usdzar_spot'] = df['usdzar_spot'].astype('float')
    df['tusdzar_spot'] = df['tusdzar_spot'].astype('float')
    df['notification'] = df['notification'].apply(convert_int)
    df.rename(
        columns={
            'time': 'Time',
            'day': 'Day',
            'spread_spot': 'Spot spread',
            'spread_fx': 'FX spread',
            'usdzar_spot': 'USDZAR',
            'tusdzar_spot': 'TUSDZAR'
        },
        inplace=True
    )
    return df


def get_specific_data(df, dates):
    start = datetime.datetime(
        year=dates[0].year,
        month=dates[0].month,
        day=dates[0].day
    )
    end = datetime.datetime(
        year=dates[1].year,
        month=dates[1].month,
        day=dates[1].day,
        hour=59
    )
    check = []
    for i in df.index:
        if start <= df['Time'][i] <= end:
            check.append(True)
        else:
            check.append(False)
    df = df.iloc[check]
    return df


def get_backwards_data(df, timeperiod, length):
    data = df
    now = datetime.datetime.now()
    if timeperiod == 'Years':
        cutoff = datetime.datetime(year=now.year - length, month=now.month,
                                   day=now.day, hour=now.hour, minute=now.minute,
                                   second=now.second)
    if timeperiod == 'Days':
        cutoff = now - datetime.timedelta(days=length)
    if timeperiod == 'Hours':
        cutoff = now - datetime.timedelta(hours=length)
    if timeperiod == 'Weeks':
        mondays = data.loc[data['day'] == 'Monday']
        date = mondays['time'][max(mondays.index)]
        cutoff = date - datetime.timedelta(hours=date.hour)
        cutoff = cutoff - datetime.timedelta(minutes=date.minute + 1)
    check = []
    for i in data.index:
        if data['Time'][i] >= cutoff:
            check.append(True)
        elif data['Time'][i] < cutoff:
            check.append(False)
    df = data.iloc[check]
    return df


def get_spread(trade_amount, spread_type = 'spot'):
    usdzar_data = yf.Ticker('ZAR=X')
    usdzar = usdzar_data.stats()['price']['regularMarketPrice']
    if spread_type == 'FX':
        usdzar = usdzar + 0.05
    usd = round(trade_amount/usdzar, 2) - 0.01
    url = f'https://www.ovex.io/api/v2/rfq/get_quote?market=tusdzar&from_amount={usd}&side=sell'
    response = requests.get(url).json()
    profit = float(response['to_amount']) - trade_amount
    spread = round(profit / trade_amount * 100, 2)
    return spread


def get_metrics(df):
    data = df
    ind = max(data.index)
    spread_spot = [data['Spot spread'][ind],
                   data['Spot spread'][ind] - data['Spot spread'][ind - 30]]
    spread_fx = [data['FX spread'][ind],
                   data['FX spread'][ind] - data['FX spread'][ind - 30]]
    usdzar = [data['USDZAR'][ind],
                   data['USDZAR'][ind] - data['USDZAR'][ind - 30]]
    tusdzar = [data['TUSDZAR'][ind],
                   data['TUSDZAR'][ind] - data['TUSDZAR'][ind - 30]]
    df = pd.DataFrame({'spread_spot': spread_spot,
                       'spread_fx': spread_fx,
                       'usdzar': usdzar,
                       'tusdzar': tusdzar})
    return df


def only_working_hours():
    df = get_data()
    df = df.loc[df['Day'] != 'Saturday']
    df = df.loc[df['Day'] != 'Sunday']
    check = []
    for i in df.index:
        day = df['Day'][i]
        time = df['Time'][i]
        if day != 'Friday':
            if 8 <= time.hour <= 16:
                check.append(True)
            else:
                check.append(False)
        elif day == 'Friday':
            if (8 <= time.hour < 16) or (time.hour == 16 and time.minute <= 45):
                check.append(True)
            else:
                check.append(False)
    df = df.iloc[check]
    return df


