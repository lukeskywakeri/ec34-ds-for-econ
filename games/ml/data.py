"""
PROJECT OVERFIT — Answer key module.

Each function runs the EXACT same code shown in app.py so the answers match.
Seeds are fixed; never change them or the game breaks.
"""

import numpy as np
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.datasets import make_regression, make_blobs
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score


# ---------------------------------------------------------------------------
# M1: Feature-selection leakage on pure noise
# ---------------------------------------------------------------------------
def get_mission1_answer():
    np.random.seed(99)
    X = np.random.randn(100, 500)   # 500 features, ALL pure noise
    y = np.random.randn(100)        # target is also pure noise

    # Pipeline A — leaky: select features using ALL data before splitting
    corrs   = np.abs(np.corrcoef(X.T, y)[-1, :-1])
    top_idx = np.argsort(corrs)[-25:]
    X_sel   = X[:, top_idx]
    X_tr_a, X_te_a, y_tr_a, y_te_a = train_test_split(X_sel, y, test_size=0.3, random_state=7)
    r2_a = r2_score(y_te_a, LinearRegression().fit(X_tr_a, y_tr_a).predict(X_te_a))

    # Pipeline B — correct: split first, then select from training data only
    X_tr_b, X_te_b, y_tr_b, y_te_b = train_test_split(X, y, test_size=0.3, random_state=7)
    corrs_b   = np.abs(np.corrcoef(X_tr_b.T, y_tr_b)[-1, :-1])
    top_idx_b = np.argsort(corrs_b)[-25:]
    r2_b = r2_score(
        y_te_b,
        LinearRegression().fit(X_tr_b[:, top_idx_b], y_tr_b).predict(X_te_b[:, top_idx_b]),
    )

    return {"r2_leaky": round(r2_a, 2), "r2_correct": round(r2_b, 2)}


# ---------------------------------------------------------------------------
# M2: LassoCV — how many features survive?
# ---------------------------------------------------------------------------
def get_mission2_answer():
    np.random.seed(0)
    X, y = make_regression(noise=4, random_state=0, n_samples=100, n_features=200)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=123)

    scaler = StandardScaler().fit(X_tr)
    X_tr_s = scaler.transform(X_tr)

    lasso = LassoCV(alphas=np.linspace(0.1, 1, 30), random_state=0, max_iter=10000)
    lasso.fit(X_tr_s, y_tr)

    n_nonzero = int((np.abs(lasso.coef_) >= 1e-6).sum())
    return {"n_nonzero": n_nonzero, "alpha": round(lasso.alpha_, 3)}


# ---------------------------------------------------------------------------
# M3: Decision-tree CV — best max_depth
# ---------------------------------------------------------------------------
def get_mission3_answer():
    np.random.seed(1)
    X = np.sort(5 * np.random.rand(80, 1), axis=0)
    y = np.sin(X).ravel()
    y[::5] += 3 * (0.5 - np.random.rand(16))

    cv_means = {}
    for depth in range(1, 11):
        scores = cross_val_score(
            DecisionTreeRegressor(max_depth=depth), X, y, cv=5, scoring="r2"
        )
        cv_means[depth] = scores.mean()

    best_depth = max(cv_means, key=cv_means.get)
    return {"best_depth": best_depth, "cv_means": cv_means}


# ---------------------------------------------------------------------------
# M4: K-Means — inertia at k = 4
# ---------------------------------------------------------------------------
def get_mission4_answer():
    np.random.seed(42)
    X_raw, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=42)

    # Standardise — exactly as shown in the app code block
    X = StandardScaler().fit_transform(X_raw)
    km4 = KMeans(n_clusters=4, random_state=42, n_init="auto").fit(X)
    return {"inertia_k4": int(round(km4.inertia_))}


# ---------------------------------------------------------------------------
# M5: Bagging — test R² of 50-tree ensemble
# ---------------------------------------------------------------------------
def get_mission5_answer():
    np.random.seed(2026)
    X = np.sort(5 * np.random.rand(80, 1), axis=0)
    y = np.sin(X).ravel() + np.random.normal(0, 0.2, 80)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=7)

    np.random.seed(0)
    bag_preds = np.zeros((len(X_te), 50))
    for i in range(50):
        idx = np.random.randint(0, len(X_tr), len(X_tr))
        t   = DecisionTreeRegressor(max_depth=None).fit(X_tr[idx], y_tr[idx])
        bag_preds[:, i] = t.predict(X_te)

    r2_bag = r2_score(y_te, bag_preds.mean(axis=1))
    return {"r2_bag": round(r2_bag, 3)}


# ---------------------------------------------------------------------------
# Pre-compute everything at import time so app.py pays the cost once
# ---------------------------------------------------------------------------
ANSWERS = {
    1: str(get_mission1_answer()["r2_leaky"]),
    2: str(get_mission2_answer()["n_nonzero"]),
    3: str(get_mission3_answer()["best_depth"]),
    4: str(get_mission4_answer()["inertia_k4"]),
    5: str(get_mission5_answer()["r2_bag"]),
}
