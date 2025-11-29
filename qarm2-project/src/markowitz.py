import numpy as np
import cvxpy as cp


def _to_numpy(x):
    """Transforme Series / liste en array 1D numpy[float]."""
    return np.asarray(x, dtype=float).flatten()


def _make_psd(Sigma):
    """
    Rend la matrice de covariance exploitable par cvxpy :
    - force la symétrie
    - clippe légèrement les valeurs propres négatives (problèmes numériques)
    """
    Sigma = np.asarray(Sigma, dtype=float)

    # 1) Symétrise
    Sigma = 0.5 * (Sigma + Sigma.T)

    # 2) Projection simple en PSD (on évite les petites valeurs propres négatives)
    eigvals, eigvecs = np.linalg.eigh(Sigma)
    eigvals_clipped = np.clip(eigvals, 1e-8, None)
    Sigma_psd = eigvecs @ np.diag(eigvals_clipped) @ eigvecs.T

    return Sigma_psd


def gmv_weights(Sigma, short: bool = False):
    """
    Global Minimum Variance (GMV)
    -> minimise la variance du portefeuille
    Contraintes :
      - somme des poids = 1
      - si short=False : w >= 0 (pas de vente à découvert)
    """
    Sigma_psd = _make_psd(Sigma)
    n = Sigma_psd.shape[0]

    w = cp.Variable(n)

    objective = cp.Minimize(cp.quad_form(w, Sigma_psd))

    constraints = [cp.sum(w) == 1]
    if not short:
        constraints.append(w >= 0)

    prob = cp.Problem(objective, constraints)
    prob.solve()

    return np.array(w.value).flatten()


def tangency_weights(mu, Sigma, rf: float = 0.0, short: bool = False):
    """
    Portefeuille de tangence (version convexifiée DCP-friendly).

    Idée :
      - maximise le rendement excédentaire (mu - rf)' w
      - sous contrainte de risque borné : w' Σ w <= 1
      - somme des poids = 1
      - si short=False : w >= 0
    """
    mu = _to_numpy(mu)
    Sigma_psd = _make_psd(Sigma)
    n = len(mu)

    w = cp.Variable(n)

    # Rendements excédentaires
    excess = mu - rf

    # Maximise le rendement excédentaire pour un risque borné
    objective = cp.Maximize(excess @ w)

    constraints = [
        cp.quad_form(w, Sigma_psd) <= 1,  # risque borné
        cp.sum(w) == 1                    # fully invested
    ]
    if not short:
        constraints.append(w >= 0)

    prob = cp.Problem(objective, constraints)
    prob.solve()

    return np.array(w.value).flatten()


