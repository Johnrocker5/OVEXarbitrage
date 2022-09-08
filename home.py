import streamlit as st
import data



def app():
    df = data.get_data()
    df = df[['Time', 'Spot spread', 'FX spread', 'USDZAR', 'TUSDZAR']]
    metrics = data.get_metrics(df)

    st.title('Home :house:')

    st.markdown(''' ### You can use this app to:
    - View current spreads in real time for any trading amount
    - View recent spreads
    - Calculate spread and profit based on OTC quote received from OVEX
    - View historical spreads and exchange rates
    - Analyse spreads for favourable days and times
    - Generate a quote request message in the correct format
    ''')

    st.header('Latest rates')

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

    st.header('Notes')

    st.markdown('''
    ### Definitions
    - Spot spread: the spread between the spot rate of USDZAR and the rate at which TUSDZAR can be sold for
    - FX spread: the spread between the foreign exchange rate at which USD can be bought with ZAR (assumed to be spot USDZAR + R0.05) and the rate at which TUSDZAR can be sold for
    - USDZAR: the spot rate of USDZAR    
    ### Important
    The spreads recorded above are:
    - Based on a trade amount of 2.5 million rand
    - Updated every two minutes
    - Never worse than the spread you will receive via the OTC desk on request
    ''')


  #  chart = charts.get_chart_spread(df[['Time', 'Spot spread', 'FX spread']])
  #  st.altair_chart(chart, use_container_width=True)

