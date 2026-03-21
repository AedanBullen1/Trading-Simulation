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


    def HOLD(self):

        buy_and_hold = pd.Series(1, index=self.price.index)

        return buy_and_hold
    
    def MOM(self):

        momentum = (self.price.diff() > 0).astype(int)

        return momentum
    
    def MAC(self):

        short_ma = self.price.rolling(20).mean()
        long_ma = self.price.rolling(50).mean()
        ma_cross = (short_ma > long_ma).astype(int)
        ma_cross = ma_cross.fillna(0)

        return ma_cross
    
    def RSI(self):

        delta = self.price.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = -delta.clip(upper=0).rolling(14).mean()
        rsi = 100 - (100 / (1+gain/loss.replace(0, np.nan)))

        rsi_signal = (rsi < 30).astype(int)

        return rsi_signal
    
    def BB(self):

        ma = self.price.rolling(20).mean()
        std = self.price.rolling(20).std()
        lower_band = ma - 2 * std
        bb_signal = (self.price < lower_band).astype(int)

        return bb_signal
    

    def combine_strategies(self):
        
        strategies = {
            "HOLD": self.HOLD(),
            "MOM": self.MOM(),
            "Moving Average Crossover": self.MAC(),
            "RSI": self.RSI(),
            "Bollinger Bands": self.BB()
            }
        
        return strategies




        