import datetime
import streamlit as st
import data
import charts
import pandas as pd


def convert_time(time):
    t = time - datetime.timedelta(hours=2)
    return t


def get_data(timeperiod, hours):
    if hours == 'all':
        df = data.get_data()
    if hours == 'business':
        df = data.only_working_hours()
    if timeperiod != 'All time':
        if timeperiod == '1 hour' or timeperiod == '2 hours' or timeperiod == '4 hours' or timeperiod == '12 hours':
            tp = 'Hours'
            if timeperiod != '12 hours':
                ln = int(timeperiod[0])
            elif timeperiod == '12 hours':
                ln = int(timeperiod[0:2])
        if timeperiod == '1 day' or timeperiod == '7 days' or timeperiod == '14 days' or timeperiod == '30 days' \
        or timeperiod == '60 days' or timeperiod == '90 days' or timeperiod == '180 days':
            tp = 'Days'
            if timeperiod == '1 day' or timeperiod == '7 days':
                ln = int(timeperiod[0])
            if timeperiod == '14 days' or timeperiod == '30 days' or timeperiod == '60 days' or timeperiod == '90 days':
                ln = int(timeperiod[0:2])
            if timeperiod == '180 days':
                ln = int(timeperiod[0:3])
        if timeperiod == '1 year' or timeperiod == '2 years' or timeperiod == '5 years':
            tp = 'Years'
            ln = int(timeperiod[0])
        df = data.get_backwards_data(df=df, timeperiod=tp, length=ln)
        times = []
        for i in df.index:
            t = df['Time'][i]
            times.append(convert_time(time=t))
        ts = pd.DataFrame({'Time': times})
        df['Time'] = ts['Time'].values
    return df

def get_spread_data(timeperiod, hours):
    data = get_data(timeperiod=timeperiod, hours=hours)
    data = data[['Time', 'Spot spread', 'FX spread']]
    df = data.melt('Time', var_name='Type', value_name='Spread')
    return df

def get_rate_data(timeperiod, hours):
    data = get_data(timeperiod=timeperiod, hours=hours)
    data = data[['Time', 'USDZAR', 'TUSDZAR']]
    df = data.melt('Time', var_name='Market', value_name='Exchange rate')
    return df

def get_table(timeperiod, hours):
    data = get_data(timeperiod=timeperiod, hours=hours)
    data = data[['Spot spread', 'FX spread', 'USDZAR', 'TUSDZAR']]
    mini = pd.DataFrame(data.min()).transpose()
    lower = pd.DataFrame(data.quantile(0.25)).transpose()
    med = pd.DataFrame(data.median()).transpose()
    upper = pd.DataFrame(data.quantile(0.75)).transpose()
    q95 = pd.DataFrame(data.quantile(0.95)).transpose()
    q99 = pd.DataFrame(data.quantile(0.99)).transpose()
    maxi = pd.DataFrame(data.max()).transpose()
    avg = pd.DataFrame(data.mean()).transpose()
    stdev = pd.DataFrame(data.std()).transpose()
    df = pd.concat([mini, lower, med, upper, q95, q99, maxi,
                     avg, stdev], ignore_index=True)
    measurement = pd.DataFrame({'Measurement': ['Minimum', 'Lower quartile',
                                                'Median', 'Upper quartile',
                                                '95th percentile', '99th percentile',
                                                'Maximum', 'Mean', 'Standard deviation']})
    df.insert(0, 'Measurement', measurement)
    return df



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

    st.title('Historical data')

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


    option = st.selectbox('Select the time period for which you would wish to view historical data for',
                          ('1 hour', '2 hours', '4 hours', '12 hours', '1 day',
                           '7 days', '14 days', '30 days', '60 days', '90 days',
                           '180 days', '1 year', '2 years', '5 years', 'All time'),
                          index=4,
                          help='The period selected is from the current date and time, e.g., selecting 1 Hour means' +
                                ' that the last hour of data will be shown.')

    st.subheader('Charts')

    if option != 'All time':
        chart1_message = f'The chart below shows the movement in spreads during the last {option}'
    elif option == 'All time':
        chart1_message = 'The chart below shows the all time movement in spreads since recording'
    st.markdown(chart1_message)

    chart1 = charts.get_chart_spread(get_spread_data(timeperiod=option, hours=hours))
    st.altair_chart(chart1, use_container_width=True)

    if option != 'All time':
        chart2_message = f'The chart below shows the movement in exchange rates during the last {option}'
    elif option == 'All time':
        chart2_message = 'The chart below shows the all time movement in exchange rates since recording'
    st.markdown(chart2_message)

    chart2 = charts.real_rate_chart(get_rate_data(timeperiod=option, hours=hours))
    st.altair_chart(chart2, use_container_width=True)

    st.subheader('Spread distribution')

    if option != 'All time':
        chart3_message = f'The chart below shows the normal distribution of spreads during the last {option}'
    elif option == 'All time':
        chart3_message = 'The chart below shows the all time normal distribution of spreads since recording'
    st.markdown(chart3_message)

    chart3 = charts.get_dist_chart(get_data(timeperiod=option, hours=hours))
    st.plotly_chart(chart3, use_container_width=True)

    st.subheader('Table summary')

    st.table(get_table(timeperiod=option, hours=hours))



