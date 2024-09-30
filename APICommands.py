#asset list https://www.nseindia.com/get-quotes/equity?symbol=GOLDBEES
# Import the necessary module or package
from kite_app import KiteApp  # Import the KiteApp class from the kite_app module
import datetime  # Import the datetime module for handling date and time operations

# Obtain the 'enctoken' manually from the 'kite.zerodha.com' website
# Ensure that you are logged into the website, but do not log out
# Access the website's login window and inspect the page
# Navigate to the 'Network' tab and press Ctrl+R (Windows) or Command+R (Mac)
# Click on 'Positions' and then click on 'Headers'
# Look for 'Authorisation' and copy the 'enctoken' value
enctoken = "YOUR_ENCTOKEN_HERE"  # Replace "YOUR_ENCTOKEN_HERE" with the actual 'enctoken' obtained

# Create an instance of the KiteApp class with the provided 'enctoken'
kite = KiteApp(enctoken=enctoken)

# Basic calls to retrieve information
print(kite.margins())     # Retrieve margin details
print(kite.orders())      # Retrieve order details
print(kite.positions())   # Retrieve position details

# Get instrument or exchange information
print(kite.instruments())           # Retrieve all instruments
print(kite.instruments("NSE"))      # Retrieve instruments for a specific exchange (NSE)
print(kite.instruments("NFO"))      # Retrieve instruments for a specific exchange (NFO)

# Get Live Data
print(kite.ltp("NSE:RELIANCE"))                                 # Retrieve last traded price for a specific instrument
print(kite.ltp(["NSE:NIFTY 50", "NSE:NIFTY BANK"]))             # Retrieve last traded price for multiple instruments
print(kite.quote(["NSE:NIFTY BANK", "NSE:ACC", "NFO:NIFTY22SEPFUT"]))  # Retrieve quote data for multiple instruments

# Get Historical Data
instrument_token = 9604354
from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)  # Start date for historical data (7 days ago)
to_datetime = datetime.datetime.now()                                 # End date for historical data (current date)
interval = "5minute"                                                  # Interval for data (e.g., 5-minute intervals)
print(kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False))

# Place Order
order = kite.place_order(variety=kite.VARIETY_REGULAR,               # Type of order variety (e.g., regular order)
                         exchange=kite.EXCHANGE_NSE,                  # Exchange for the order (e.g., NSE)
                         tradingsymbol="ACC",                        # Trading symbol of the instrument
                         transaction_type=kite.TRANSACTION_TYPE_BUY,  # Type of transaction (e.g., Buy)
                         quantity=1,                                 # Quantity of the instrument
                         product=kite.PRODUCT_MIS,                   # Product type (e.g., MIS)
                         order_type=kite.ORDER_TYPE_MARKET,          # Type of order (e.g., Market order)
                         price=None,                                 # Price of the order (None for market order)
                         validity=None,                              # Validity of the order (e.g., Day)
                         disclosed_quantity=None,                    # Disclosed quantity for disclosed order
                         trigger_price=None,                         # Trigger price for trigger-based order
                         squareoff=None,                             # Square off value for square off order
                         stoploss=None,                              # Stop loss value for stop loss order
                         trailing_stoploss=None,                     # Trailing stop loss value for trailing stop loss order
                         tag="TradeViaPython")                       # Tag for the order

print(order)  # Print the order details

# Modify Order
kite.modify_order(variety=kite.VARIETY_REGULAR,                      # Type of order variety (e.g., regular order)
                  order_id="order_id",                               # ID of the order to be modified
                  parent_order_id=None,                              # Parent order ID if applicable
                  quantity=5,                                        # New quantity for the order
                  price=200,                                         # New price for the order
                  order_type=kite.ORDER_TYPE_LIMIT,                  # New type of order (e.g., Limit order)
                  trigger_price=None,                                # New trigger price for trigger-based order
                  validity=kite.VALIDITY_DAY,                        # New validity for the order (e.g., Day)
                  disclosed_quantity=None)                           # New disclosed quantity for disclosed order

# Cancel Order
kite.cancel_order(variety=kite.VARIETY_REGULAR,                      # Type of order variety (e.g., regular order)
                  order_id="order_id",                               # ID of the order to be cancelled
                  parent_order_id=None)                              # Parent order ID if applicable
