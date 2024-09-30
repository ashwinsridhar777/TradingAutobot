from kite_trade import KiteApp
import datetime
import time

# Function to check if the stochastic oscillator signals a buy
def check_stochastic_buy(stoch):
    if stoch > 80:  # Buy when the stochastic oscillator is above 80 (overbought condition)
        return True
    else:
        return False

# Function to check if the stochastic oscillator signals a sell
def check_stochastic_sell(stoch):
    if stoch < 20:  # Sell when the stochastic oscillator is below 20 (oversold condition)
        return True
    else:
        return False

# Replace 'enctoken' with your actual encrypted token
enctoken = '/ba+VmUolzQByvCBW/iHBfqb4LFxfpr0QTXdMz2bwBBWLXvDkUQtyQIWYTrxunYxSIdP0vL64kwfo1+tsV8JTeiOSlGoqS65axA7D1HXABU7R+QHf0ywog=='
# Initialize KiteApp object with the encrypted token
kite = KiteApp(enctoken=enctoken)

# Define instrument token and time interval
instrument_token = 3693569  # Replace with the instrument token of your choice
from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)  # Start date for historical data (7 days ago)
to_datetime = datetime.datetime.now()                                 # End date for historical data (current date)
interval = "5minute"                                                  # Interval for data (e.g., 5-minute intervals)

# Main loop to run the strategy every 5 minutes
while True:
    try:
        # Fetch historical data for the last 15 minutes
        historical_data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)

        # Check if historical data is available
        if historical_data:
            # Calculate stochastic oscillator
            close_prices = [candle['close'] for candle in historical_data]
            lowest_low = min(close_prices)
            highest_high = max(close_prices)
            current_close = close_prices[-1]
            stoch = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100

            # Check for buy signal
            if check_stochastic_buy(stoch):
                # Place Buy Order for 1 Unit of GOLDBEES
                order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                         exchange=kite.EXCHANGE_NSE,
                                         tradingsymbol="GOLDBEES",
                                         transaction_type=kite.TRANSACTION_TYPE_BUY,
                                         quantity=1,
                                         product=kite.PRODUCT_MIS,
                                         order_type=kite.ORDER_TYPE_MARKET,
                                         price=None,
                                         validity=None,
                                         disclosed_quantity=None,
                                         trigger_price=None,
                                         squareoff=None,
                                         stoploss=None,
                                         trailing_stoploss=None,
                                         tag="TradeViaPython")

                print("Buy order placed at", datetime.datetime.now())
                print("Order details:", order)

            # Check for sell signal
            elif check_stochastic_sell(stoch):
                # Place Sell Order for 1 Unit of GOLDBEES
                order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                         exchange=kite.EXCHANGE_NSE,
                                         tradingsymbol="GOLDBEES",
                                         transaction_type=kite.TRANSACTION_TYPE_SELL,
                                         quantity=1,
                                         product=kite.PRODUCT_MIS,
                                         order_type=kite.ORDER_TYPE_MARKET,
                                         price=None,
                                         validity=None,
                                         disclosed_quantity=None,
                                         trigger_price=None,
                                         squareoff=None,
                                         stoploss=None,
                                         trailing_stoploss=None,
                                         tag="TradeViaPython")

                print("Sell order placed at", datetime.datetime.now())
                print("Order details:", order)

        else:
            print("Historical data is empty")

        # Sleep for 5 minutes
        time.sleep(300)

    except Exception as e:
        print("Error:", e)
