import streamlit as st
import requests
from typing import Dict

def get_crypto_price(symbol: str, api_key: str) -> float:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': 'USD'
    }
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        if 'data' in data and symbol in data['data']:
            return float(data['data'][symbol]['quote']['USD']['price'])
        else:
            raise KeyError("Data field not found in response")
    except Exception as e:
        st.error(f"Error fetching price: {str(e)}")
        return 0

def main():
    st.title("CryptoCalculator Helper")
    
    # Get URL parameters
    try:
        # For newer Streamlit versions
        query_params = st.query_params
        amount_param = query_params.get("amount", None)
    except:
        # For older Streamlit versions
        query_params = st.experimental_get_query_params()
        amount_param = query_params.get("amount", [None])[0]
    
    crypto_options = {
        "Litecoin": {
            "symbol": "LTC",
            "address": "ltc1q2y4xh62xe39c8hsljzavdj0ccwjqmjj736g0t8"
        },
        "Tron": {
            "symbol": "TRX",
            "address": "TPHK7t5AmBLPaKHxTiygH8e8CrSmpetUjM"
        },
        "Monero": {
            "symbol": "XMR",
            "address": "82guQ3jedEnBsSXN6wksAmF5tPDBUBaaNcdqmRK43JdABGQExJ78pFL6MC9yqm2eZfPmHVwJNDTo5KPn5MGHDGtTMifQBhs"
        }
    }
    
    selected_crypto_name = st.selectbox(
        "Select Cryptocurrency",
        options=list(crypto_options.keys())
    )
    
    selected_symbol = crypto_options[selected_crypto_name]["symbol"]
    selected_address = crypto_options[selected_crypto_name]["address"]
    
    # Default amount
    default_amount = 5.0
    
    # Check if amount is provided in URL
    if amount_param is not None:
        try:
            base_amount_usd = float(amount_param)
            st.info(f"Using amount from URL: ${base_amount_usd}")
        except ValueError:
            st.error(f"Invalid amount parameter: {amount_param}. Using default amount: ${default_amount}")
            base_amount_usd = default_amount
    else:
        # If no URL parameter, provide a number input
        base_amount_usd = st.number_input("Amount in USD ($)", min_value=1.0, value=default_amount, step=1.0)
        st.caption("You can also specify the amount via URL parameter, e.g., ?amount=10")
    
    api_key = st.secrets["coinmarketcap_api_key"]
    
    if st.button("Calculate"):
        current_price = get_crypto_price(selected_symbol, api_key)
        
        if current_price > 0:
            # Calculation based on provided amount
            base_amount = base_amount_usd / current_price
            # Add a little 5% protection fee
            final_amount = base_amount * 1.05
            
            st.write("### Total Amount")
            st.code(f"{final_amount:.8f} {selected_symbol}")
            
            st.write("### Payment Address")
            st.code(selected_address)

if __name__ == "__main__":
    main()
