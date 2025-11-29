import numpy as np
from scipy.optimize import minimize

def _portfolio_vol(w, Sigma):
    w = np.asarray(w)
    Sigma = np.asarray(Sigma)
    return np.sqrt(w @ Sigma @ w)

def _risk_contributions(w, Sigma):
    """
    Contribution au risque de chaque actif.
    """
    w = np.asarray(w)
    Sigma = np.asarray(Sigma)
    sigma_p = _portfolio_vol(w, Sigma)
    mrc = Sigma @ w            # marginal risk contribution
    rc = w * mrc / sigma_p     # risk contribution par actif
    return rc

def erc_weights(Sigma):
    """
    Equal Risk Contribution portfolio.
    """
    Sigma = np.asarray(Sigma)
    n = Sigma.shape[0]

    w0 = np.ones(n) / n
    bounds = [(0, 1)] * n
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]

    def objective(w):
        rc = _risk_contributions(w, Sigma)
        return np.sum((rc - rc.mean())**2)

    res = minimize(objective, w0, method="SLSQP",
                   bounds=bounds, constraints=constraints)

    return np.array(res.x).ravel()
