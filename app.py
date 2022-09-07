import streamlit as st
import data
import charts
import home
import spread_now
import history
import analysis
import calculation
import generate




pages = {'Home': home, 'Current spreads': spread_now, 'Historical data': history,
         'Data analysis': analysis, 'Calculate spread and profit': calculation,
         'Generate quote': generate}

st.sidebar.markdown('### Spread checker')
st.sidebar.markdown('Navigate using this side bar')
selection = st.sidebar.radio('Go to', list(pages.keys()))
page = pages[selection]
page.app()
