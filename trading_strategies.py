import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
colours = sns.color_palette("muted")
sns.set_theme(style='whitegrid')

class Strategies:
    "This class will comprise all trading strategies"

    def __init__(self, price: pd.Series):
        "Initialises attributes"
        self.price = price


    def HOLD(self, price):

        buy_and_hold = pd.Series(1, index=price.index)

        return {"HOLD": buy_and_hold}
    
    def MOM(self, price):

        momentum = (price.diff() > 0).astype(int)

        return {"MOM": momentum}
    
    def MAC(self, price):

        short_ma = price.rolling(20).mean()
        long_ma = price.rolling(50).mean()
        ma_cross = (short_ma > long_ma).astype(int)

        return {"Moving average convergence": ma_cross}
    
    def RSI(self, price):

        delta = price.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rsi = 100 - (100 / (1+gain/loss))

        rsi_signal = (rsi < 30).astype(int)

        return {"RSI": rsi_signal}
    
    def BB(self, price):

        ma = price.rolling(20).mean()
        std = price.rolling(20).std()
        lower_band = ma - 2 * std
        bb_signal = (price < lower_band).astype(int)

        return {"Bollinger bands": bb_signal}


        