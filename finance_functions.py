"""This will comrpise all the important functions for this simulation repo"""
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import numpy as np
colours = sns.color_palette("muted")
sns.set_theme(style='whitegrid')



class HelperFunctions:

    def __init__(self, signal: pd.Series, returns: pd.Series, curve: pd.Series, starting_cash: float = 10_000):

        self.signal = signal
        self.curve = curve
        self.returns = returns
        self.starting_cash = starting_cash


    def equity_curve(self) -> pd.Series:
        """Finds growth data based on strategy"""
    
        shifted_signal = self.signal.shift(1).fillna(0) # 1 day later. Cannot use today's signal to trade today.
    # the signal is the 1/0 trade/don't boolean. Also fills any nans.

        daily_growth = 1 + shifted_signal * self.returns # shifted signal (using whatever strategy) times returns
    # what growth u get if you use said method.
    # if signal 0 (out of market) 1 + 0 * return = 1.0, no change
    # if signal 1 (in market) 1 + 1 * return = ...
    # NB 1+ because of percentage change.

        return daily_growth.cumprod() * self.starting_cash


    def risk_metrics(self) -> dict:
        """ compute CAGR, sharpe, max drawdown, and 5th ptl final value"""
        
    
        trading_years = len(self.curve) / 252

    # compound annual growth rate.
        cagr = (self.curve.iloc[-1] / self.starting_cash) ** (1 / trading_years) - 1  # final = starting x rate ^ years. rearrange for rate.

    # find Sharpe
        sharpe = (self.returns.mean() / self.returns.std()) * np.sqrt(252) if self.returns.std() > 0 else 0 # div by 0 guard. also set risk-free rate to 0
    # sharpe asks how much return getting per unit risk. Average daily return/volatility (std), scaled to annual by root 252. 
    # think of as a parameter to assess how much worth a risk had. 1.5 is considered strong. less than 1 is bad.

    # max drawdown.
        rolling_max = self.curve.cummax() # tracks portfolios all-time high over time. 
        drawdown = (self.curve - rolling_max) / rolling_max # how far below the peak you are (zero or negative.) as a percentage
        max_drawdown = drawdown.min() # worst, most negative point.
    #MD asks what the worst peak to trough loss experienced is. Measures most painful moment in portfolio.

        return {"cagr": cagr, "sharpe": sharpe, "max_drawdown": max_drawdown, "final": self.curve.iloc[-1]}