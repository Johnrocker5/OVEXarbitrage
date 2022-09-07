import streamlit as st
import datetime
import pandas as pd
import numpy as np
import data
import charts


def get_data(timeperiod, hours, dates):
    if hours == 'all':
        df = data.get_data()
    if hours == 'business':
        df = data.only_working_hours()
    if timeperiod != 'All time':
        if timeperiod != 'Custom':
            if timeperiod == '30 days' or timeperiod == '60 days' or timeperiod == '90 days' or timeperiod == '180 days':
                tp = 'Days'
                if timeperiod == '30 days' or timeperiod == '60 days' or timeperiod == '90 days':
                    ln = int(timeperiod[0:2])
                if timeperiod == '180 days':
                    ln = int(timeperiod[0:3])
            if timeperiod == '1 year' or timeperiod == '2 years' or timeperiod == '5 years':
                tp = 'Years'
                ln = int(timeperiod[0])
            df = data.get_backwards_data(df=df, timeperiod=tp, length=ln)
        elif timeperiod == 'Custom':
            df = data.get_specific_data(df=df, dates=dates)
    return df

def get_day_data(timeperiod, hours, spread, dates):
    data = get_data(timeperiod=timeperiod, hours=hours, dates=dates)
    days = data['Day'].unique()
    df = pd.DataFrame()
    for i in days:
        day = [i]
        dff = data.loc[data['Day'] == i]
        avg = [dff[spread].mean()]
        med = [dff[spread].median()]
        p90 = [dff[spread].quantile(0.9)]
        p95 = [dff[spread].quantile(0.95)]
        p99 = [dff[spread].quantile(0.99)]
        maxi = [dff[spread].max()]
        dfff = pd.DataFrame({'Day': day, 'Mean': avg, 'Median': med, '90th percentile': p90,
                             '95th percentile': p95, '99th percentile': p99, 'Maximum': maxi})
        df = pd.concat([df, dfff], ignore_index=True)
    return df

def convert_days_array(array):
    ln = len(array)
    if ln == 1:
        ans = array[0]
    if ln == 2:
        ans = array[0] + ' and ' + array[1]
    if ln == 3:
        ans = array[0] + ', ' + array[1] + ' and ' + array[2]
    if ln == 4:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ' and ' + array[3]
    if ln == 5:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ', ' + array[3] + ' and ' + array[4]
    if ln == 6:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ', ' + array[3] + ', ' + array[4] + ' and ' + array[5]
    if ln == 7:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ', ' + array[3] + ', ' + array[4] + ', ' \
              + array[5] + ' and ' + array[6]
    return ans




def get_best_worst_days(timeperiod, hours, spread, dates):
    data = get_day_data(timeperiod=timeperiod, hours=hours, spread=spread, dates=dates)
    score_w = [0] * len(data.index)
    score_l = [0] * len(data.index)
    for i in data.columns[1:]:
        dfw = data.loc[data[i] == data[i].max()]
        dfl = data.loc[data[i] == data[i].min()]
        for j in dfw.index:
            score_w[j] = score_w[j] + 1
        for k in dfl.index:
            score_l[k] = score_l[k] + 1
    win_score = max(score_w)
    low_score = max(score_l)
    check_w = []
    for i in score_w:
        if i >= win_score:
            check_w.append(True)
        elif i < win_score:
            check_w.append(False)
    check_l = []
    for i in score_l:
        if i >= low_score:
            check_l.append(True)
        elif i < low_score:
            check_l.append(False)
    w_days = np.array(data.iloc[check_w]['Day'])
    l_days = np.array(data.iloc[check_l]['Day'])
    w_days = convert_days_array(w_days)
    l_days = convert_days_array(l_days)
    days = [w_days, l_days]
    return days


def get_hour_data(timeperiod, hours, spread, dates):
    data = get_data(timeperiod=timeperiod, hours=hours, dates=dates)
    if hours == 'all':
        hr_names = ['Between 00:00 and 01:00', 'Between 01:00 and 02:00', 'Between 02:00 and 03:00',
                    'Between 03:00 and 04:00', 'Between 05:00 and 05:00', 'Between 05:00 and 06:00',
                    'Between 06:00 and 07:00', 'Between 07:00 and 08:00', 'Between 08:00 and 09:00',
                    'Between 09:00 and 10:00', 'Between 10:00 and 11:00', 'Between 11:00 and 12:00',
                    'Between 12:00 and 13:00', 'Between 13:00 and 14:00', 'Between 14:00 and 15:00',
                    'Between 15:00 and 16:00', 'Between 16:00 and 17:00', 'Between 17:00 and 18:00',
                    'Between 18:00 and 19:00', 'Between 19:00 and 20:00', 'Between 20:00 and 21:00',
                    'Between 21:00 and 22:00', 'Between 22:00 and 23:00', 'Between 23:00 and 24:00']
        hrs = []
        for i in range(0, 24):
            hrs.append([i, i+1])
    if hours == 'business':
        hr_names = [' Between 08:00 and 09:00', 'Between 09:00 and 10:00', 'Between 10:00 and 11:00',
                    ' Between 11:00 and 12:00', 'Between 12:00 and 13:00', 'Between 13:00 and 14:00',
                    ' Between 14:00 and 15:00', 'Between 15:00 and 16:00', 'Between 16:00 and 17:00']
        hrs = []
        for i in range(8, 17):
            hrs.append([i, i+1])
    df = pd.DataFrame()
    for i in range(0, len(hrs)):
        start = hrs[i][0]
        end = hrs[i][1]
        hour = [hr_names[i]]
        check = []
        for i in data.index:
            time = data['Time'][i]
            if start <= time.hour < end:
                check.append(True)
            else:
                check.append(False)
        hour_df = data.iloc[check]
        avg = [hour_df[spread].mean()]
        med = [hour_df[spread].median()]
        p90 = [hour_df[spread].quantile(0.9)]
        p95 = [hour_df[spread].quantile(0.95)]
        p99 = [hour_df[spread].quantile(0.99)]
        maxi = [hour_df[spread].max()]
        dfff = pd.DataFrame({'Time': hour, 'Mean': avg, 'Median': med, '90th percentile': p90,
                             '95th percentile': p95, '99th percentile': p99, 'Maximum': maxi})
        df = pd.concat([df, dfff], ignore_index=True)
    return df


def convert_hours(array):
    ln = len(array)
    for i in range(0, len(array)):
        t = len(array[i])
        s = 'b'
        v = array[i][1:t]
        array[i] = s + v
    if ln == 1:
        ans = array[0]
    if ln == 2:
        ans = array[0] + ' and ' + array[1]
    if ln == 3:
        ans = array[0] + ', ' + array[1] + ' and ' + array[2]
    if ln == 4:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ' and ' + array[3]
    if ln == 5:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ', ' + array[3] + ' and ' + array[4]
    if ln == 6:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ', ' + array[3] + ', ' + array[4] + ' and ' + array[5]
    if ln == 7:
        ans = array[0] + ', ' + array[1] + ', ' + array[2] + ', ' + array[3] + ', ' + array[4] + ', ' \
              + array[5] + ' and ' + array[6]
    return ans

def get_best_worst_hours(timeperiod, hours, spread, dates):
    data = get_hour_data(timeperiod=timeperiod, hours=hours, spread=spread, dates=dates)
    score_w = [0] * len(data.index)
    score_l = [0] * len(data.index)
    for i in data.columns[1:]:
        dfw = data.loc[data[i] == data[i].max()]
        dfl = data.loc[data[i] == data[i].min()]
        for j in dfw.index:
            score_w[j] = score_w[j] + 1
        for k in dfl.index:
            score_l[k] = score_l[k] + 1
    win_score = max(score_w)
    low_score = max(score_l)
    check_w = []
    for i in score_w:
        if i >= win_score:
            check_w.append(True)
        elif i < win_score:
            check_w.append(False)
    check_l = []
    for i in score_l:
        if i >= low_score:
            check_l.append(True)
        elif i < low_score:
            check_l.append(False)
    w_hour = np.array(data.iloc[check_w]['Time'])
    l_hour = np.array(data.iloc[check_l]['Time'])
    w_hour = convert_hours(w_hour)
    l_hour = convert_hours(l_hour)
    hours = [w_hour, l_hour]
    return hours


def app():
    df = data.get_data()
    df = df[['Time', 'Spot spread', 'FX spread', 'USDZAR', 'TUSDZAR']]
    metrics = data.get_metrics(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Spot spread',
                str(metrics['spread_spot'][0]) + '%',
                str(round(metrics['spread_spot'][1], 2)) + '% in the last hour')
    col2.metric('FX spread',
                str(metrics['spread_fx'][0]) + '%',
                str(round(metrics['spread_fx'][1], 2)) + '% in the last hour')
    col3.metric('USDZAR',
                str(metrics['usdzar'][0]),
                str(round(metrics['usdzar'][1], 2)) + ' in the last hour')
    col4.metric('TUSDZAR',
                str(metrics['tusdzar'][0]),
                str(round(metrics['tusdzar'][1], 2)) + ' in the last hour')

    st.title('Data analysis')

    st.markdown('This page can be used to analyse past spreads to determine which days and times generally' +
                ' see more favourable spreads')

    st.subheader('Spread selection')

    spread = st.selectbox('Select the type of spread you wish to analyse', ('Spot spread', 'FX spread'),
                          index=0)

    st.subheader('Time period selection')

    trading_hours = st.checkbox('Only view banking hours', help=''' If this box is ticked, then only data which falls during banking hours will be shown. 

    Sasfin Bank trading hours are:
    - Monday to Thursday: 08h00 to 17h00
    - Friday: 08h00 to 16h45
    - Saturday and Sunday: closed
    - Public holiday: closed

    :warning: FX trades can only be submitted during the above hours.
    ''')
    if trading_hours:
        hours = 'business'
    if not trading_hours:
        hours = 'all'

    option = st.selectbox(f'Select the time period for which you wish to analyse {spread}s',
                          ('30 days', '60 days', '90 days',
                           '180 days', '1 year', '2 years', '5 years', 'All time', 'Custom'),
                          index=7,
                          help='The period selected is from the current date and time, e.g., selecting 7 days means' +
                               ' that the last week of data will be shown. Alternatively, you can select to' +
                               " customize the start and end dates by selecting 'Custom'.")

    if option == 'Custom':
        today = datetime.date.today()
        dates = st.date_input('Select the dates for which you wish to analyse data for',
                                   help='''Important to note:
                                    - The analysis will be inclusive of both the start and end dates
                                    - Recording of data only started on 2022/09/03
                                    ''',
                                   min_value=datetime.date(year=2022, month=9, day=3),
                                   max_value=today,
                                   value=[today - datetime.timedelta(days=1), today])

    elif option != 'Custom':
        dates = (0, 1)

    st.header('Day analysis')

    if spread == 'Spot spread':
        sp = 'spot spreads'
    elif spread == 'FX spread':
        sp = 'FX spreads'

    if option == 'All time':
        message1 = f'The following charts show the **all time** metrics recorded for **{sp}** on different days'
    elif option != 'All time':
        if option != 'Custom':
            message1 = f'The following charts show the metrics recorded for **{sp}** on different days,' + \
                       f' during the last **{option}**'
        elif option == 'Custom':
            message1 = f'The following charts show the metrics recorded for **{sp} between _{dates[0]}_ and _{dates[1]}** across different days'

    if trading_hours:
        message1 = message1 + ' during **banking hours**'
    if not trading_hours:
        message1 = message1 + ' during **all hours**'

    st.markdown(message1)

    day_charts = charts.get_day_charts(source=get_day_data(timeperiod=option,
                                                           hours=hours,
                                                           spread=spread,
                                                           dates=dates),
                                       hours=hours)
    st.altair_chart(day_charts, use_container_width=True)

    days_wl = get_best_worst_days(timeperiod=option, hours=hours, spread=spread, dates=dates)
    best_day = days_wl[0]
    worst_day = days_wl[1]

    if trading_hours:
        message2 = 'across banking hours during the selected period'
    if not trading_hours:
        message2 = 'across all hours during the selected period'

    message3 = f'Based on the above day analysis, the **most favourable** day(s) for {sp} {message2} has been **{best_day}**'
    message4 = f' and the **least favourable** day(s) has been **{worst_day}**'

    st.markdown(message3 + message4)

    st.subheader('Time analysis')

    if option == 'All time':
        message5 = f'The following charts show the **all time** metrics recorded for **{sp}** across different times'
    elif option != 'All time':
        if option != 'Custom':
            message5 = f'The following charts show the metrics recorded for **{sp}** across different times,' + \
                       f' during the last **{option}**'
        elif option == 'Custom':
            message5 = f'The following charts show the metrics recorded for **{sp} between _{dates[0]}_ and _{dates[1]}** across different times'

    if trading_hours:
        message5 = message5 + ' during **banking hours**'
    if not trading_hours:
        message5 = message5 + ' during **all hours**'

    st.markdown(message5)

    hour_charts = charts.get_time_charts(source=get_hour_data(timeperiod=option,
                                                              hours=hours,
                                                              spread=spread,
                                                              dates=dates),
                                         hours=hours)
    st.altair_chart(hour_charts, use_container_width=True)

    hours_wl = get_best_worst_hours(timeperiod=option, hours=hours, spread=spread, dates=dates)
    best_hour = hours_wl[0]
    worst_hour = hours_wl[1]

    message6 = f'Based on the above time analysis, the **most favourable** time(s) for {sp}'
    message7 = f' {message2} has been **{best_hour}**'
    message8 = f' and the **least favourable** time(s) has been **{worst_hour}**'

    st.markdown(message6 + message7 + message8)



















