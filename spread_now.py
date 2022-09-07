import streamlit as st
import pandas as pd
import data
import charts




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

    st.title('Current spreads')

    trade_amount = st.number_input('Insert your desired trade amount in rands',
                                   min_value=200000,
                                   step=100000,
                                   max_value=10000000,
                                   value=2500000)

    if st.button('Check current spreads'):
        spot_spread = data.get_spread(trade_amount=trade_amount)
        fx_spread = data.get_spread(spread_type='FX', trade_amount=trade_amount)
        st.markdown(f'The current spreads for a trade amount of R{trade_amount}:')
        col1, col2 = st.columns(2)
        col1.metric('Spot spread', str(spot_spread) + '%')
        col2.metric('FX spread', str(fx_spread) + '%')

