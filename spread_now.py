import streamlit as st
import pandas as pd
import data
import charts




def app():

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

