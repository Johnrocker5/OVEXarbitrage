import streamlit as st

def app():
    st.title('Spread calculation')

    st.markdown('You can use this page to calculate the spread you received on your quote' +
                'from OVEX OTC desk as well as the resulting profits')

    st.subheader('Quote details')

    st.markdown('Enter the details of your quote below')

    usdzar = st.number_input(
            'USDZAR ask quote price',
            min_value=0.00,
            step=0.01
        )

    tusdzar = st.number_input(
            'TUSDZAR bid quote price',
            min_value=0.00,
            step=0.01
        )

    trade_amount = st.number_input(
            'Trade amount in ZAR',
            min_value=200000,
            max_value=10000000,
            step=100000
        )

    if usdzar > 0 and tusdzar > 0:
        spread = str(round(((tusdzar - usdzar) / usdzar) * 100, 2)) + '%'

        # May need to change sasfin charge applied
        sasfin_charge = 500

        # May need to change OVEX spread charge applied
        ovex_spread = 0.1

        profit = (trade_amount / usdzar) * tusdzar * (1 - ovex_spread * 0.01) - sasfin_charge - trade_amount
        profit = 'R' + str(round(profit, 2))

        st.markdown(f'The spread on the above quote is **{spread}**')
        st.markdown(f'Assuming Sasfin Bank charges of R{sasfin_charge} and OVEX OTC spread' +
                        f' charge of {ovex_spread}%, the above quote will yield a profit of **{profit}**')






