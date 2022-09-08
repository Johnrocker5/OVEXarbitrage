import streamlit as st


def app():
    st.title('Quote generation')

    st.markdown('You can use this page to generate a quote request which you can copy, and paste in ' +
                ' a WhatsApp chat, so that it is easily available')

    st.subheader('Enter your details')

    name = st.text_input(
        'Enter your full name and surname',
        help='This is the name and surname associated with your FX account.'
    )

    email = st.text_input('Enter your OVEX account email address')

    trade_amount = st.number_input(
        'Enter your desired trade amount',
        help='The trade amount in ZAR you wish to request a quote for.',
        min_value=200000,
        max_value=10000000,
        step=100000
    )

    fia = st.text_input(
        'Enter your Foreign Investment Allowance (FIA) PIN',
        help='''
            This is a 10 character pin. Steps to find your pin:
    - login to SARS e-filing
    - Click on 'Tax Status' in the top right corner
    - Click on 'Tax Compliance Status' on the left hand panel
    - Click on 'Tax Compliance Status Request' on the left hand panel
    - Click on 'Foreign Investment Allowance'
    - Select the request for which you would like to get the PIN for
    - Click on 'Print PIN'
    You will now be able to view your pin in the table labelled 'TCS Details'
    '''
    )


    if name != '' and email != '' and fia != '':
        if len(fia) != 10:
            st.markdown(':warning: Invalid FIA PIN! Please ensure you have' +
                        ' entered the correct PIN')
        elif len(fia) == 10:
            x = trade_amount / 1000
            if x >= 1000:
                y = trade_amount / 1000000
                if y.as_integer_ratio()[1] == 1:
                    zar = 'R' + str(int(y)) + ' million'
                elif y.as_integer_ratio()[1] != 1:
                    zar = 'R' + str(y) + ' million'
            elif x < 1000:
                y = trade_amount / 1000
                if y.as_integer_ratio()[1] == 1:
                    zar = 'R' + str(int(y)) + ' thousand'
                elif y.as_integer_ratio()[1] != 1:
                    zar = 'R' + str(y) + ' thousand'
            st.markdown(f'''
            You are about to request a quote for:
            - Name: {name}
            - Email: {email}
            - Trade amount: {zar}
            - FIA PIN: {fia}
            ''')
            happy = st.checkbox(
                'The above details are correct',
                value=False
            )
            if happy:
                if st.button('Generate quote'):
                    message = f'''
                    Hi, can I please request **two** quotes:

                    1. **USD/ZAR ask**
                    2. **TUSD/ZAR bid**

                    **Details**:
                    
                    - Full name: {name}
                    - Trade amount: {zar}
                    - FIA PIN: {fia}
                    - Email: {email}'''

                    st.markdown('### Your message to copy and paste')

                    st.info(message)

