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

class MonteCarlo:

    def __init__(self, price, daily_returns, starting_cash, n_sims):
        self.price = price
        self.n_days = len(price)
        self.strategies = Strategies(self.price).combine_strategies()
        self.daily_returns = daily_returns
        self.starting_cash = starting_cash
        self.n_sims = n_sims


    def monte_carlo(self):

        seed = 20
        rng = np.random.default_rng(seed)
        ret_array = self.daily_returns.values # into NumPy arrau

        mc_results = {name: [] for name in self.strategies}
        mc_curves = {name: [] for name in self.strategies}

        for sim in range(self.n_sims):

            idx_boot = rng.integers(0, self.n_days, size=self.n_days)
            boot_rets = pd.Series(ret_array[idx_boot], index=self.daily_returns.index)

            for name, signal in self.strategies.items():
                curve = HelperFunctions.equity_curve(signal, boot_rets)
                mc_results[name].append(curve.iloc[-1])
                mc_curves[name].append(curve.values)

        print(f"Done: {self.n_sims} simulations {len(self.strategies)} strategies")

        return mc_curves, mc_results

    def plot_confidence_bands(self, mc_curves):

        fig, axes = plt.subplots(len(self.strategies), 1, figsize=(13, 4*len(self.strategies)), sharex=True)

        dates = self.price.index

        for ax, (name, signal), col in zip(axes, self.strategies.items(), colours):

            curves_arr = np.array(mc_curves[name]) # set of all mc curves for given strategy.
            lo = np.percentile(curves_arr, 5, axis=0)
            hi = np.percentile(curves_arr, 95, axis = 0)
            med = np.percentile(curves_arr, 50, axis=0)

            historical_curve = HelperFunctions.equity_curve(signal, self.daily_returns) # curve using method for actual data.

            ax.fill_between(dates, lo, hi, alpha=.25, color=col, label="5-95th pctl")
            ax.plot(dates, med, color=col, linewidth=1.5, label='median sim') # average
            ax.plot(dates, historical_curve, color='black', linewidth=1, linestyle='--', label='historical')
            ax.axhline(self.starting_cash, color='grey', linewidth=1, linestyle='-')
            ax.set_title(name, fontsize=11)
            ax.set_ylabel('portfolio ($)')
            ax.legend(fontsize=8, loc='upper left')
            sns.despine(ax=ax)

        axes[-1].set_xlabel('Date')
        fig.suptitle(f'Monte Carlo confidence bands ({self.n_sims} simulations)', fontsize=13, y=1.01)
        plt.tight_layout()
        plt.show()

    def VaR(self, mc_results):

        var_5 = {name: np.percentile(vals, 5) for name, vals in mc_results.items()} # 95% of histroies did better than this
        med = {name: np.percentile(vals, 50) for name, vals in mc_results.items()} # 50% did better

        fig, ax = plt.subplots(figsize = (9,4))
        names = list(var_5.keys()) # returns labels (keys)
        x = np.arange(len(names))

        bars = ax.bar(x, [var_5[n] for n in names], color=colours[:len(names)], alpha=0.85, label="VaR (5th pctile)")
        ax.scatter(x, [med[n] for n in names], color="black", zorder=5, label="Median", marker="D", s=50)
        ax.axhline(self.starting_cash, color="red", linestyle="--", linewidth=1, label="Starting cash")

        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.set_ylabel("Portfolio value ($)")
        ax.set_title("Value at Risk (5%) and Median Final Value")
        ax.legend()
        sns.despine(ax=ax)
        plt.tight_layout()
        plt.show()

        print("\nVaR (5th pctl of final portfolio val):")
        for name in names:
            print(f"  {name:<22}: ${var_5[name]:>8,.0f}  (median ${med[name]:>8,.0f})")

