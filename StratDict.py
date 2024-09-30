from sklearn.neighbors import KNeighborsClassifier
from kiteapi import *
from pyswarm import pso
import numpy as np
import datetime


enctoken = "L+vcN/ekdPSXTe4hwy3lp/0hShsOS4uQut5+7Rb8/0mhjnK27oXAGpj9swk7MgPHMc3z4jWZvXhkIcKIVoM3IT67vFQEKK4yz2jW8rjTeca84chzrzjC+Q=="  
kite = KiteApp(enctoken=enctoken)

# Fetch historical data
def fetch_historical_data():
    try:
        instrument_token = 3693569
        from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)  # From last 7 days
        to_datetime = datetime.datetime.now()
        interval = "5minute"
        data = kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False)
        return data
    except Exception as e:
        printt(e)

data = fetch_historical_data()


def moving_average_buy_signal():

    short_window=50
    long_window=200
    
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    buy_signal = (data['Short_MA'] > data['Long_MA']).any()
    
    return buy_signal


def moving_average_sell_signal():

    short_window=50
    long_window=200
    
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    sell_signal = (data['Short_MA'] <= data['Long_MA']).any()
    
    return sell_signal


def bollinger_bands_buy_signal():

    window=20
    num_std_dev=2
    
    data['MA'] = data['Close'].rolling(window=window).mean()
    data['Upper_BB'] = data['MA'] + num_std_dev * data['Close'].rolling(window=window).std()
    buy_signal = (data['Close'] < data['Lower_BB']).any()
    
    return buy_signal


def bollinger_bands_sell_signal():

    window=20
    num_std_dev=2
    
    data['MA'] = data['Close'].rolling(window=window).mean()
    data['Upper_BB'] = data['MA'] + num_std_dev * data['Close'].rolling(window=window).std()
    sell_signal = (data['Close'] >= data['Lower_BB']).any()
    
    return sell_signal


def standard_deviation_buy_signal():

    window=20
    num_std_dev=2
    
    data['Rolling_std'] = data['Close'].rolling(window=window).std()
    buy_signal = (data['Close'] < (data['Rolling_std'] * -num_std_dev)).any()
    
    return buy_signal


def standard_deviation_sell_signal():

    window=20
    num_std_dev=2
    
    data['Rolling_std'] = data['Close'].rolling(window=window).std()
    sell_signal = (data['Close'] >= (data['Rolling_std'] * -num_std_dev)).any()
    
    return sell_signal


def envelope_buy_signal():

    window=20
    percent=0.05
    
    data['Upper_Env'] = data['Close'].rolling(window=window).mean() * (1 + percent)
    buy_signal = (data['Close'] < data['Lower_Env']).any()
    
    return buy_signal


def envelope_sell_signal():

    window=20
    percent=0.05
    
    data['Lower_Env'] = data['Close'].rolling(window=window).mean() * (1 - percent)
    sell_signal = (data['Close'] >= data['Lower_Env']).any()
    
    return sell_signal


def hma():

    window=20
    wma1 = 2 * data['Close'].rolling(window=int(window/2)).mean() - data['Close'].rolling(window=window).mean()
    hma = data['Close'].rolling(window=int(np.sqrt(window))).mean()
    
    return hma


def hma_buy_signal():

    window=20
    hma_val = hma(data, window)
    buy_signal = (data['Close'] > hma_val).any()
    
    return buy_signal


def hma_sell_signal():

    window=20
    hma_val = hma(data, window)
    sell_signal = (data['Close'] <= hma_val).any()
    
    return sell_signal


def knn_buy_signal():
    # Prepare features and target variable
    X = data[['Feature1', 'Feature2', 'Feature3']]  # Example features
    y = data['Target']
    
    # Define objective function for PSO
    def objective_function(k):
        # Initialize and fit KNN model
        knn_model = KNeighborsClassifier(n_neighbors=int(k))
        knn_model.fit(X, y)
        
        # Use the model for predictions
        predictions = knn_model.predict(X)
        
        # Calculate accuracy (you can use any other evaluation metric here)
        accuracy = (predictions == y).mean()
        
        # Return the negative accuracy since PSO minimizes the objective function
        return -accuracy
    
    # Set the bounds for k
    lb = 1  # Lower bound for k
    ub = 10  # Upper bound for k
    
    # Use PSO to find the best value of k
    best_k, _ = pso(objective_function, lb, ub)
    
    # Initialize and fit KNN model with the best k value
    best_knn_model = KNeighborsClassifier(n_neighbors=int(best_k))
    best_knn_model.fit(X, y)
    
    # Use the model for predictions
    predictions = best_knn_model.predict(X)
    
    # Generate buy signal based on predictions
    buy_signal = predictions == 1
    
    return buy_signal

def knn_sell_signal():
    # Prepare features and target variable
    X = data[['Feature1', 'Feature2', 'Feature3']]  # Example features
    y = data['Target']
    
    # Define objective function for PSO
    def objective_function(k):
        # Initialize and fit KNN model
        knn_model = KNeighborsClassifier(n_neighbors=int(k))
        knn_model.fit(X, y)
        
        # Use the model for predictions
        predictions = knn_model.predict(X)
        
        # Calculate accuracy (you can use any other evaluation metric here)
        accuracy = (predictions == y).mean()
        
        # Return the negative accuracy since PSO minimizes the objective function
        return -accuracy
    
    # Set the bounds for k
    lb = 1  # Lower bound for k
    ub = 10  # Upper bound for k
    
    # Use PSO to find the best value of k
    best_k, _ = pso(objective_function, lb, ub)
    
    # Initialize and fit KNN model with the best k value
    best_knn_model = KNeighborsClassifier(n_neighbors=int(best_k))
    best_knn_model.fit(X, y)
    
    # Use the model for predictions
    predictions = best_knn_model.predict(X)
    
    # Generate sell signal based on predictions
    sell_signal = predictions != 1
    
    return sell_signal
