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
    st.title("CryptoCalculato Helper")
    
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
            "address": "88amiwvnVgC89AFUHAvxTm1628cquTfX3Np1S88Y1H6rKXXBzo58dn68pyDvoW5T3UArt9iouuKYyfPHLcn2vi3A6xHQiBN"
        }
    }
    
    selected_crypto_name = st.selectbox(
        "Select Cryptocurrency",
        options=list(crypto_options.keys())
    )
    
    selected_symbol = crypto_options[selected_crypto_name]["symbol"]
    selected_address = crypto_options[selected_crypto_name]["address"]
    
    api_key = st.secrets["coinmarketcap_api_key"]
    
    if st.button("Calculate"):
        current_price = get_crypto_price(selected_symbol, api_key)
        
        if current_price > 0:
            # $5 calculation based
            base_amount = 5 / current_price
            # Add a little 5% protection fee
            final_amount = base_amount * 1.05
            
            st.write("### Total Amount")
            st.code(f"{final_amount:.8f} {selected_symbol}")
            
            st.write("### Payment Address")
            st.code(selected_address)

if __name__ == "__main__":
    main()
