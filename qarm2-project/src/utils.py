import numpy as np

def portfolio_stats(w, mu, Sigma, rf=0.01):
    """
    Calcule rendement, volatilité et Sharpe du portefeuille.
    mu et Sigma peuvent être pandas ou numpy, on convertit.
    """
    w = np.asarray(w).ravel()
    mu = np.asarray(mu).ravel()
    Sigma = np.asarray(Sigma)

    mu_p = float(w @ mu)
    sigma_p = float(np.sqrt(w @ Sigma @ w))
    sharpe = (mu_p - rf) / sigma_p if sigma_p > 0 else 0.0

    return {
        "return": mu_p,
        "vol": sigma_p,
        "sharpe": sharpe
    }


def show_weights(label, tickers, w):
    """
    Affiche les poids de manière lisible.
    """
    print(f"\n{label} weights:")
    for t, wi in zip(tickers, w):
        print(f"  {t:5s} : {wi:6.3f}")
