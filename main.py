import time
from StratDict import *
from kiteapi import *
import datetime
import tkinter as tk
import time

global flag
global order
flag = 0
# Obtain the 'enctoken' manually from the 'kite.zerodha.com' website
enctoken = "eGLz+s7WiSirPv6B5HUnc8vm8nK7XHM3DXQvDsmdx2z6TFLzYLYgqU/fKBRxbfuQSeRm5X8YtlUbUNRa4AjViqfcz2eZBdkzyE/qeQpMhpqNU1qzc3B6vA=="  # Replace "YOUR_ENCTOKEN_HERE" with the actual 'enctoken' obtained

# Create an instance of the KiteApp class with the provided 'enctoken'
kite = KiteApp(enctoken=enctoken)

global asset
# Define the asset to trade
asset = "GOLDBEES"


# Function to execute buy signals for all strategies
def execute_buy_signals():
    try:
        while not buy_order_placed:  # Continue executing buy signals until buy order is placed
            # Check for buy signals from all strategies
            if moving_average_buy_signal():
                place_order()
            elif bollinger_bands_buy_signal():
                place_order()
            elif standard_deviation_buy_signal():
                place_order()
            elif envelope_buy_signal():
                place_order()
            elif hma_buy_signal():
                place_order()
            elif knn_buy_signal():
                place_order()  # Check for buy signals every 1 second
            else:
                print('No Buy Signal')
                
    except Exception as e:
        printt(e)

# Function to place order for the asset
def place_order():
    current_datetime = datetime.datetime.now()
    order = kite.place_order(variety=kite.VARIETY_REGULAR,               
                         exchange=kite.EXCHANGE_NSE,                  
                         tradingsymbol= asset,                       
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
    print(f"{current_datetime}: {order}")
    flag = 1  # Set flag to True indicating buy order is placed

# Function to execute sell signals for all strategies
def execute_sell_signals():
    try:
        while True:
            if buy_order_placed:  # Check if buy order is placed
                # Check for sell signals from all strategies
                if moving_average_sell_signal():
                    place_sell_order()
                elif bollinger_bands_sell_signal():
                    place_sell_order()
                elif standard_deviation_sell_signal():
                    place_sell_order()
                elif envelope_sell_signal():
                    place_sell_order()
                elif hma_sell_signal():
                    place_sell_order()
                elif knn_sell_signal():
                    place_sell_order()
            time.sleep(1)  # Check for sell signals every 1 second
    
    except Exception as e:
        print(e)

# Function to place sell order for the asset
def place_sell_order():
    kite.cancel_order(variety=kite.VARIETY_REGULAR,                      # Type of order variety (e.g., regular order)
                  order_id=order,                               # ID of the order to be cancelled
                  parent_order_id=None)
    print(order)
    flag=0

while (flag==0):
    time.sleep(1)
    execute_buy_signals()
    
    
    
while (flag==1):
    time.sleep()
    execute_sell_signals()
