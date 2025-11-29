import yfinance as yf
import pandas as pd
import numpy as np


def load_prices(tickers, start="2019-01-01", end=None):
    """
    Télécharge les prix ajustés pour une liste de tickers.
    On utilise auto_adjust=True, donc on prend la colonne 'Close'.
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,   # important avec les nouvelles versions de yfinance
        progress=False
    )

    # Si plusieurs tickers -> colonnes MultiIndex (Close, ticker)
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data["Close"]

    return prices.dropna()


def to_returns(prices, method="log"):
    """
    Convertit les prix en rendements journaliers.
    method = 'log' (par défaut) ou 'simple'
    """
    if method == "log":
        rets = np.log(prices / prices.shift(1))
    else:
        rets = prices.pct_change()

    return rets.dropna()


def mean_cov(returns):
    mu = returns.mean()
    Sigma = returns.cov()

    # 🔥 Fix CVXPY : forcer la symétrie parfaite
    Sigma = (Sigma + Sigma.T) / 2

    return mu, Sigma, list(returns.columns)


