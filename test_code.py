import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
colours = sns.color_palette("muted")
sns.set_theme(style='whitegrid')

from trading_strategies import Strategies
from finance_functions import HelperFunctions
from monte_carlo import MonteCarlo



#=== configuration =======
symbol = "AAPL"
start = "2015-01-01"
end = '2025-01-01'
starting_cash = 10000
n_sims = 1000 # number of Monte Carlo sims per strategy


raw = yf.download(symbol, start=start, end=end, auto_adjust=True)
price = raw["Close"].squeeze().dropna() # remember squeeze() gets rid of titles in series.
daily_returns = price.pct_change().fillna(0)

n_days = len(price)
print(f"{symbol}: {n_days} trading days loaded {start} to {end}")

montecarlo = MonteCarlo(price, daily_returns, starting_cash, n_sims)

mc_curves, mc_results = montecarlo.monte_carlo()  # capture the return values
montecarlo.plot_confidence_bands(mc_curves)
montecarlo.VaR(mc_results)