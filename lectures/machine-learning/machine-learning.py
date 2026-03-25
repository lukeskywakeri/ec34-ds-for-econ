import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import statsmodels.api as sm
    import warnings
    warnings.filterwarnings('ignore')

    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LassoCV, Lasso, LinearRegression
    from sklearn.datasets import load_iris, make_regression, make_blobs, load_digits
    from sklearn.model_selection import (
        train_test_split, ValidationCurveDisplay, LearningCurveDisplay,
    )
    from sklearn.inspection import DecisionBoundaryDisplay
    from sklearn.svm import SVC
    from sklearn.metrics import r2_score
    from sklearn.decomposition import PCA
    from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
    from sklearn.ensemble import GradientBoostingRegressor

    return (
        DecisionBoundaryDisplay, DecisionTreeRegressor,
        GradientBoostingRegressor, KMeans, Lasso, LassoCV,
        LearningCurveDisplay, LinearRegression, PCA, SVC,
        StandardScaler, ValidationCurveDisplay,
        load_digits, load_iris, make_blobs, make_regression,
        mo, np, pd, plt, r2_score, sm, sns, train_test_split,
    )


# ── INTRODUCTION ───────────────────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    # Machine Learning for Economists

    Python is one of the premier languages for machine learning. The main library is **`scikit-learn`**, which provides a consistent API for:
    - Data processing and feature engineering
    - Model fitting and prediction
    - Cross-validation and hyperparameter tuning

    ---

    ## What is Machine Learning?

    Rather than caring about *why* a variable affects an outcome, ML is about **prediction**:

    $$y = f(X; \varepsilon)$$

    The goal is $\hat{y}$ — a good estimate of $y$ that generalizes to new data.

    | | Supervised | Unsupervised |
    |---|---|---|
    | **Goal** | Predict a known $y$ | Find structure without $y$ |
    | **Type of $y$** | Continuous (regression) or categorical (classification) | None |
    | **Examples** | Lasso, SVM, trees | Clustering, PCA |
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The ML Workflow

    ```
    Clean Data → Feature Engineering → Train/Test Split → Fit → Evaluate → Tune → Repeat
    ```

    ### The Golden Rule: No Data Contamination

    Training data must **never** leak into the test set — including during preprocessing.

    - Fit your scaler, imputer, or encoder on the **training set only**
    - Then *transform* (apply) it to the test set
    - Normalizing with the full dataset transfers test-set information to training → inflated scores

    ### K-Fold Cross-Validation

    A single train/test split can be unlucky. K-Fold rotates through $k$ splits:
    each observation is in the test set exactly once. Common choices: $k=5$ or $k=10$.

    This gives a more reliable estimate of out-of-sample performance and is the standard way
    to tune hyperparameters.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Bias–Variance Tradeoff

    $$\text{MSE} = \mathbb{E}[(Y - \hat{Y})^2] = \underbrace{\text{Bias}^2}_{\text{wrong structure}} + \underbrace{\text{Variance}}_{\text{sensitive to data}} + \underbrace{\sigma^2}_{\text{irreducible noise}}$$

    - **Bias**: the model is systematically wrong because it's too simple (underfitting)
    - **Variance**: the model memorizes training noise and fails on new data (overfitting)
    - In causal econometrics we insist on zero bias; in ML we trade some bias for lower variance

    | Model complexity | Bias | Variance | Out-of-sample performance |
    |---|---|---|---|
    | Too low (underfit) | High | Low | Poor |
    | Just right | Low | Low | Good |
    | Too high (overfit) | Low | High | Poor |
    """)
    return


# ── PART 1: UNSUPERVISED LEARNING ──────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    # Part 1: Unsupervised Learning

    No target variable $y$. The goal is to find structure in $X$ alone.

    We cover two foundational methods:
    1. **K-Means Clustering** — group observations into $k$ homogeneous clusters
    2. **PCA** — compress many features into a few uncorrelated components
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## K-Means Clustering

    K-Means partitions $n$ observations into $k$ clusters by iterating:

    1. Assign each point to its nearest centroid (by Euclidean distance)
    2. Move each centroid to the mean of its assigned points
    3. Repeat until centroids stop moving

    **Key parameter:** $k$ — must be chosen by the researcher. Elbow plots and silhouette scores help.
    """)
    return


@app.cell
def _(KMeans, make_blobs, mo, np, plt, sns):
    np.random.seed(42)
    _features, _true_labels = make_blobs(n_samples=1000, centers=5, random_state=42)
    _km = KMeans(n_clusters=5, random_state=42, n_init='auto')
    _pred_labels = _km.fit_predict(_features)

    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.scatterplot(x=_features[:, 0], y=_features[:, 1], hue=_true_labels,
                    palette='tab10', ax=_axes[0], legend=False)
    _axes[0].set_title("True cluster labels")

    sns.scatterplot(x=_features[:, 0], y=_features[:, 1], hue=_pred_labels,
                    palette='tab10', ax=_axes[1], legend=False)
    _axes[1].scatter(_km.cluster_centers_[:, 0], _km.cluster_centers_[:, 1],
                     c='black', marker='X', s=200, zorder=5, label='Centroids')
    _axes[1].set_title("K-Means predictions (k=5)")
    _axes[1].legend()
    plt.tight_layout()
    plt.close()

    mo.as_html(_fig)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Principal Component Analysis (PCA)

    High-dimensional data is hard to visualize, expensive to compute, and often multicollinear.
    PCA finds the directions of **maximum variance** and projects the data onto them.

    Think of it as finding the "best angle" to photograph a 3D object in 2D.

    ### The math
    - **Eigenvectors** ($\vec{v}$): the new axes — they point along the principal stretches of the data cloud
    - **Eigenvalues** ($\lambda$): how much variance each axis captures (large = informative)
    - Eigenvectors are **orthogonal** → resulting components are uncorrelated

    ### Algorithm
    1. Standardize $X$ (center and scale to unit variance)
    2. Compute covariance matrix $C = \frac{1}{n} X^\top X$
    3. Eigendecompose: solve $C\vec{v} = \lambda\vec{v}$
    4. Sort eigenvectors by eigenvalue (descending)
    5. Project: $X_\text{new} = X \cdot V_k$ (keep top $k$ components)
    """)
    return


@app.cell
def _(mo, np, plt):
    # PCA rotation demo
    _rng = np.random.RandomState(1)
    _X_pca_demo = np.dot(_rng.rand(2, 2), _rng.randn(2, 400)).T
    _X_pca_demo -= _X_pca_demo.mean(axis=0)

    _cov = np.cov(_X_pca_demo, rowvar=False)
    _eigenvalues, _eigenvectors = np.linalg.eigh(_cov)
    _idx = _eigenvalues.argsort()[::-1]
    _eigenvalues, _eigenvectors = _eigenvalues[_idx], _eigenvectors[:, _idx]
    _X_rot = np.dot(_X_pca_demo, _eigenvectors)

    _fig, _axes = plt.subplots(1, 2, figsize=(13, 5))

    _axes[0].scatter(_X_pca_demo[:, 0], _X_pca_demo[:, 1], alpha=0.4, color='gray')
    _axes[0].quiver(0, 0, *_eigenvectors[:, 0], color='r', scale=3, label='PC1 direction')
    _axes[0].quiver(0, 0, *_eigenvectors[:, 1], color='b', scale=3, label='PC2 direction')
    _axes[0].set_title("Original space\n(eigenvectors show principal directions)")
    _axes[0].axis('equal'); _axes[0].grid(alpha=0.3); _axes[0].legend()

    _axes[1].scatter(_X_rot[:, 0], _X_rot[:, 1], alpha=0.4, color='purple')
    _axes[1].axhline(0, color='r', linestyle='--', alpha=0.8, label='PC1 axis')
    _axes[1].axvline(0, color='b', linestyle='--', alpha=0.8, label='PC2 axis')
    _axes[1].set_title("PCA space\n(data rotated — same points, better angle)")
    _axes[1].axis('equal'); _axes[1].grid(alpha=0.3); _axes[1].legend()

    plt.suptitle("PCA: rotating the coordinate system to align with variance", fontsize=11)
    plt.tight_layout()
    plt.close()

    _off_diag_before = _cov[0, 1]
    _off_diag_after = np.cov(_X_rot, rowvar=False)[0, 1]

    mo.vstack([
        mo.as_html(_fig),
        mo.callout(mo.md(
            f"Off-diagonal covariance (correlation) before PCA: **{_off_diag_before:.3f}** → "
            f"after PCA: **{_off_diag_after:.3f}**. "
            f"The new components are mathematically uncorrelated — great for downstream regression."
        ), kind="info"),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### PCA for Noise Filtering

    Project noisy data into the low-dimensional PCA space (retaining only high-variance components),
    then project back. The noise — which lives in low-variance directions — gets discarded.

    This works because the top components capture the *signal* (consistent across all digits),
    while the bottom components capture idiosyncratic noise.
    """)
    return


@app.cell
def _(PCA, load_digits, mo, np, plt):
    np.random.seed(42)
    _digits = load_digits()
    _ids = [0, 10, 20, 30]
    _clean = _digits.data[_ids]
    _noisy = _clean + np.random.normal(0, 6.0, _clean.shape)

    _pca_nf = PCA(n_components=12)
    _pca_nf.fit(_digits.data)  # fit on all digits, not just the 4 noisy samples
    _restored = _pca_nf.inverse_transform(_pca_nf.transform(_noisy))

    _fig, _axes = plt.subplots(3, 4, figsize=(9, 7))
    for _i in range(4):
        _axes[0, _i].imshow(_clean[_i].reshape(8, 8), cmap='gray_r')
        _axes[1, _i].imshow(_noisy[_i].reshape(8, 8), cmap='gray_r')
        _axes[2, _i].imshow(_restored[_i].reshape(8, 8), cmap='gray_r')
        if _i == 0:
            _axes[0, _i].set_ylabel("Original", fontweight='bold')
            _axes[1, _i].set_ylabel("Noisy", fontweight='bold')
            _axes[2, _i].set_ylabel("PCA Restored\n(12 components)", fontweight='bold')
    for _ax in _axes.flatten():
        _ax.set_xticks([]); _ax.set_yticks([])
    plt.suptitle("PCA Noise Filtering — fit on 1797 images, applied to 4 noisy samples", fontsize=11)
    plt.tight_layout()
    plt.close()

    mo.as_html(_fig)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### How Many Components? The Scree Plot

    Every PCA returns as many components as there are features, but most carry little information.
    The scree plot helps choose $k$:

    - **Fixed variance threshold**: keep enough components to explain 95% of total variance
    - **Elbow rule**: look for the bend where individual variance drops sharply
    - **Kaiser's rule**: drop any component with eigenvalue < 1 (less informative than one original variable)
    """)
    return


@app.cell
def _(PCA, load_digits, mo, np, plt):
    _digits2 = load_digits()
    _pca_full = PCA().fit(_digits2.data)

    _exp_var = _pca_full.explained_variance_ratio_ * 100
    _cum_var = np.cumsum(_exp_var)
    _k95 = int(np.argmax(_cum_var >= 95)) + 1

    _fig, _ax = plt.subplots(figsize=(10, 5))
    _ax.bar(range(1, len(_exp_var) + 1), _exp_var, alpha=0.5,
            color='cornflowerblue', label='Individual explained variance')
    _ax.step(range(1, len(_cum_var) + 1), _cum_var, where='mid',
             color='red', lw=2, label='Cumulative explained variance')
    _ax.axhline(95, color='green', linestyle='--', label='95% threshold')
    _ax.axvline(_k95, color='green', linestyle=':', alpha=0.7)
    _ax.text(_k95 + 1, 78, f'95% variance\nat {_k95} components', color='green', fontweight='bold')
    _ax.set_xlabel('Principal Component'); _ax.set_ylabel('Explained Variance (%)')
    _ax.set_title('Scree Plot: Digits Dataset (64 original pixel features)')
    _ax.legend(); _ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.close()

    mo.vstack([
        mo.as_html(_fig),
        mo.callout(mo.md(
            f"The digits dataset has **64** features. We can retain 95% of the variance "
            f"with just **{_k95}** components — a **{100*(64-_k95)//64}%** reduction "
            f"in dimensionality with almost no information loss."
        ), kind="success"),
    ])
    return


# ── PART 2: SUPERVISED LEARNING ────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    # Part 2: Supervised Learning

    We have a target $y$ and want to find $\hat{f}$ such that $\hat{y} = \hat{f}(X)$ generalizes to new data.

    We cover:
    1. **Regularized Regression** — Lasso, Ridge, ElasticNet
    2. **Support Vector Machines** — decision boundaries with kernels
    3. **Decision Trees** — non-linear, interpretable, and a building block for ensembles
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Regularized Regression

    OLS minimizes $\sum_i (y_i - X_i\beta)^2$. With $p > n$ features, OLS is ill-posed.
    Regularization adds a penalty on $\beta$ to shrink coefficients:

    | Method | Full objective | Effect |
    |--------|---------------|--------|
    | **Lasso** (L1) | $\text{OLS} + \alpha \sum_j \vert\beta_j\vert$ | Sets some $\beta_j$ exactly to 0 → automatic feature selection |
    | **Ridge** (L2) | $\text{OLS} + \alpha \sum_j \beta_j^2$ | Shrinks all coefficients smoothly, never exactly 0 |
    | **ElasticNet** | $\text{OLS} + \alpha_1 \sum_j \vert\beta_j\vert + \alpha_2 \sum_j \beta_j^2$ | Combines both |

    **$\alpha$** is the regularization strength — find the optimal value with `LassoCV`.

    > **Economic context:** Lasso is especially useful when you have many potential controls and want the model to select the relevant ones (e.g., LASSO for instrument selection in IV).
    """)
    return


@app.cell
def _(LassoCV, LinearRegression, StandardScaler, make_regression, mo, np, plt, r2_score, train_test_split):
    np.random.seed(0)
    _X_reg, _y_reg = make_regression(noise=4, random_state=0, n_samples=100, n_features=200)
    _X_tr, _X_te, _y_tr, _y_te = train_test_split(_X_reg, _y_reg, random_state=123)

    _scaler = StandardScaler().fit(_X_tr)
    _X_tr_s = _scaler.transform(_X_tr)
    _X_te_s = _scaler.transform(_X_te)

    # OLS
    _ols = LinearRegression().fit(_X_tr_s, _y_tr)
    _y_ols = _ols.predict(_X_te_s)
    _r2_ols = r2_score(_y_te, _y_ols)

    # LassoCV
    _lasso_cv = LassoCV(alphas=np.linspace(0.1, 1, 30), random_state=0, max_iter=10000)
    _lasso_cv.fit(_X_tr_s, _y_tr)
    _y_lasso = _lasso_cv.predict(_X_te_s)
    _r2_lasso = r2_score(_y_te, _y_lasso)
    _n_zero = int((np.abs(_lasso_cv.coef_) < 1e-6).sum())

    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    for _ax, _pred, _r2, _title in [
        (_axes[0], _y_ols, _r2_ols, f"OLS  (test R²={_r2_ols:.3f})"),
        (_axes[1], _y_lasso, _r2_lasso, f"LassoCV  α={_lasso_cv.alpha_:.3f}  (test R²={_r2_lasso:.3f})"),
    ]:
        _ax.scatter(_pred, _y_te, alpha=0.6)
        _lims = [min(_pred.min(), _y_te.min()), max(_pred.max(), _y_te.max())]
        _ax.plot(_lims, _lims, 'k--', lw=1, label='Perfect prediction')
        _ax.set_xlabel("Predicted"); _ax.set_ylabel("True"); _ax.set_title(_title)
        _ax.legend()
    plt.tight_layout()
    plt.close()

    mo.vstack([
        mo.hstack([
            mo.stat(label="OLS test R²", value=f"{_r2_ols:.3f}"),
            mo.stat(label="Lasso test R²", value=f"{_r2_lasso:.3f}"),
            mo.stat(label="Features zeroed out", value=f"{_n_zero} / 200"),
        ]),
        mo.as_html(_fig),
        mo.callout(mo.md(
            f"With 200 features and only 100 observations, OLS wildly overfits (negative R²!). "
            f"Lasso sets **{_n_zero}** of 200 coefficients to exactly 0, keeping only the informative ones."
        ), kind="warn"),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Validation Curve: Choosing $\alpha$

    The validation curve plots training vs. cross-validated test score as we vary a hyperparameter.

    - Too small $\alpha$ → low regularization → overfit (training high, test low)
    - Too large $\alpha$ → too much shrinkage → underfit (both scores drop)
    - The **optimal $\alpha$** is where the test (validation) score peaks
    """)
    return


@app.cell
def _(Lasso, StandardScaler, ValidationCurveDisplay, make_regression, mo, np, plt, train_test_split):
    _X_vc, _y_vc = make_regression(noise=4, random_state=0, n_samples=100, n_features=200)
    _X_tr_vc, _, _y_tr_vc, _ = train_test_split(_X_vc, _y_vc, random_state=123)
    _X_sc_vc = StandardScaler().fit_transform(_X_tr_vc)

    _disp_vc = ValidationCurveDisplay.from_estimator(
        Lasso(max_iter=10000), _X_sc_vc, _y_tr_vc,
        param_name='alpha', param_range=np.linspace(0.2, 2, 30),
    )
    _fig_vc = _disp_vc.figure_
    _fig_vc.set_size_inches(9, 4)
    _fig_vc.axes[0].set_title("Validation Curve: Lasso regularization strength α")
    plt.tight_layout()
    plt.close()

    mo.as_html(_fig_vc)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Support Vector Machines (SVM)

    SVMs find a **decision boundary** that maximally separates classes.
    For non-linear problems, a **kernel** implicitly maps data to a higher-dimensional space
    where a linear boundary can separate them.

    ### Key parameters
    - **C** (regularization): low C = wide margin but tolerates misclassifications; high C = tight fit to training data
    - **kernel**: `linear`, `rbf` (radial basis — most common), `poly`
    - **gamma** (for `rbf`): how "curvy" the boundary is — too high → every point gets its own region → overfit

    Below we show the effect of `gamma` on the Iris dataset using two features.
    """)
    return


@app.cell
def _(DecisionBoundaryDisplay, SVC, load_iris, mo, plt):
    _X_iris, _y_iris = load_iris(return_X_y=True)
    _X_iris = _X_iris[:, :2]

    _fig, _axes = plt.subplots(1, 3, figsize=(14, 4))
    for _ax, _gamma, _title in zip(
        _axes,
        [0.001, 1.0, 100.0],
        ["γ=0.001 (underfit)", "γ=1.0 (good)", "γ=100 (overfit)"],
    ):
        _svm = SVC(kernel='rbf', gamma=_gamma).fit(_X_iris, _y_iris)
        _disp = DecisionBoundaryDisplay.from_estimator(
            _svm, _X_iris, response_method='predict', alpha=0.35, ax=_ax
        )
        _disp.ax_.scatter(_X_iris[:, 0], _X_iris[:, 1], c=_y_iris, edgecolor='k', s=30)
        _ax.set_title(_title)

    plt.suptitle("SVM (RBF kernel): effect of gamma on the decision boundary")
    plt.tight_layout()
    plt.close()

    mo.as_html(_fig)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Validation and Learning Curves for SVM

    **Validation curve**: performance vs. hyperparameter — shows where under/overfitting occurs.

    **Learning curve**: performance vs. training set size.
    - If test score keeps improving as $n$ grows → more data would help
    - If training and test scores converge at a low value → the model is underfitting regardless of data size
    """)
    return


@app.cell
def _(LearningCurveDisplay, SVC, ValidationCurveDisplay, load_iris, mo, np, plt):
    _X_iris2, _y_iris2 = load_iris(return_X_y=True)

    _fig, _axes = plt.subplots(1, 2, figsize=(13, 4))

    ValidationCurveDisplay.from_estimator(
        SVC(kernel='rbf'), _X_iris2, _y_iris2,
        param_name='gamma', param_range=np.logspace(-6, 5, 10),
        score_type='both', n_jobs=2, score_name='Accuracy', ax=_axes[0],
    )
    _axes[0].set_title("Validation Curve: SVM gamma")

    LearningCurveDisplay.from_estimator(
        SVC(kernel='rbf'), _X_iris2, _y_iris2,
        cv=10, score_type='both', n_jobs=2, score_name='Accuracy', ax=_axes[1],
    )
    _axes[1].set_title("Learning Curve: SVM on Iris")

    plt.tight_layout()
    plt.close()

    mo.as_html(_fig)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Decision Trees

    Decision trees recursively split the feature space into rectangular regions by asking binary questions:
    > "Is $x_1 > 3.5$?" → go left or right, then repeat at each node.

    - **Classification trees**: split to minimize impurity (Gini, log-loss) at each node
    - **Regression trees**: split to minimize MSE
    - **Feature importance**: how much each feature reduced total impurity across all splits

    ### Key hyperparameter: `max_depth`

    Deeper trees fit training data better but overfit quickly.
    The plot below shows the same data fitted with different tree depths.
    """)
    return


@app.cell
def _(DecisionTreeRegressor, mo, np, plt):
    _rng = np.random.RandomState(1)
    _X_tr_tree = np.sort(5 * _rng.rand(80, 1), axis=0)
    _y_tr_tree = np.sin(_X_tr_tree).ravel()
    _y_tr_tree[::5] += 3 * (0.5 - _rng.rand(16))
    _X_test_tree = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]

    _fig, _ax = plt.subplots(figsize=(10, 4))
    _ax.scatter(_X_tr_tree, _y_tr_tree, s=20, edgecolor='black', c='darkorange', label='Data')
    for _depth, _color in [(1, 'tab:red'), (2, 'cornflowerblue'), (5, 'yellowgreen')]:
        _m = DecisionTreeRegressor(max_depth=_depth).fit(_X_tr_tree, _y_tr_tree)
        _ax.plot(_X_test_tree, _m.predict(_X_test_tree), color=_color, lw=2, label=f'max_depth={_depth}')
    _ax.set_title("Decision Tree Regression: effect of max_depth")
    _ax.set_xlabel("x"); _ax.set_ylabel("y"); _ax.legend()
    plt.tight_layout()
    plt.close()

    mo.vstack([
        mo.as_html(_fig),
        mo.callout(mo.md(
            "**max_depth=1** (red): too simple, misses the sine wave. "
            "**max_depth=2** (blue): captures the main shape. "
            "**max_depth=5** (green): memorizes every wiggle — won't generalize."
        ), kind="warn"),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Hyperparameter Tuning: Grid Search

    Decision trees have many parameters. **GridSearchCV** exhaustively tries all combinations
    and picks the best via cross-validation:

    ```python
    param_grid = {
        'max_depth':         [1, 2, 3, 5, 10, 20],
        'min_samples_split': [0.1, 0.5, 1.0],
        'max_features':      [0.25, 0.5, 0.75, 1.0],
    }
    gs = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=10, n_jobs=-1)
    gs.fit(X_train, y_train)

    gs.best_params_   # → {'max_depth': 5, 'min_samples_split': 0.1, ...}
    gs.best_score_    # cross-validated accuracy on training set
    gs.best_estimator_.score(X_test, y_test)  # final evaluation on held-out test set
    ```

    > **Note:** For large parameter grids, use `RandomizedSearchCV` — it samples randomly instead of
    > exhaustively and is much faster.
    """)
    return


# ── PART 3: ENSEMBLE METHODS ───────────────────────────────────────────────────

@app.cell
def _(mo):
    mo.md(r"""
    ---
    # Part 3: Ensemble Methods

    A single model is like a single musician — talented, but limited.
    An **ensemble** combines many models, like an orchestra combining many instruments.

    **Key insight:** If models make *different* mistakes, averaging their predictions cancels the errors.

    | Method | Problem it solves | Strategy |
    |--------|-------------------|----------|
    | **Bagging** | High variance (overfitting) | Train many models in parallel on random subsets; average |
    | **Boosting** | High bias (underfitting) | Train models sequentially, each correcting the last |
    | **Stacking** | Which model to trust? | Use a *meta-learner* to learn optimal weights |

    ### Running example
    80 noisy observations of $y = \sin(x) + \varepsilon$ where $\varepsilon \sim \mathcal{N}(0, 0.2)$.
    The true signal is a sine wave — but our models don't know that.
    """)
    return


@app.cell
def _(np):
    np.random.seed(2026)
    X = np.sort(5 * np.random.rand(80, 1), axis=0)
    y = np.sin(X).ravel() + np.random.normal(0, 0.2, X.shape[0])
    return X, y


@app.cell
def _(mo):
    mo.md(r"""
    ## Bagging: Reducing Variance

    **B**ootstrap **Agg**regat**ing** reduces *variance* by averaging many trees.

    ### How it works:
    1. Draw $B$ bootstrap samples (sample **with replacement** from training data)
    2. Fit one decision tree on each bootstrap sample
    3. **Average** predictions: $\hat{y} = \frac{1}{B} \sum_{b=1}^B \hat{y}_b$

    ### Why averaging helps:
    - Each tree is trained on different data → makes different errors
    - Errors cancel: $\text{Var}(\bar{X}) = \sigma^2 / n$ (variance falls linearly with more trees)
    - Bias stays the same — only variance shrinks

    > **Try it:** Move the slider. Notice how the red curve smooths out as you add more trees.
    """)
    return


@app.cell
def _(mo):
    n_trees_slider = mo.ui.slider(1, 50, label="Number of Trees (n_estimators)", value=1)
    return (n_trees_slider,)


@app.cell
def _(DecisionTreeRegressor, X, mo, n_trees_slider, np, plt, y):
    _preds_bag = np.zeros((len(X), n_trees_slider.value))
    for _i in range(n_trees_slider.value):
        _idx = np.random.randint(0, len(X), len(X))
        _tree = DecisionTreeRegressor(max_depth=2).fit(X[_idx], y[_idx])
        _preds_bag[:, _i] = _tree.predict(X)
    bagged_y = _preds_bag.mean(axis=1)

    _fig, _ax = plt.subplots(figsize=(9, 4))
    _ax.scatter(X, y, alpha=0.4, label="Data", color="steelblue")
    if n_trees_slider.value == 1:
        _ax.plot(X, _preds_bag[:, 0], color="orange", lw=2, alpha=0.7, label="Single tree (noisy)")
    _ax.plot(X, bagged_y, color="red", lw=3, label=f"Bagged average ({n_trees_slider.value} trees)")
    _ax.set_title(f"Bagging: {n_trees_slider.value} tree(s)")
    _ax.set_xlabel("x"); _ax.set_ylabel("y"); _ax.legend()
    plt.tight_layout()
    plt.close()

    _note = (
        "⚠️ With just 1 tree, you can see the jagged, noisy fit."
        if n_trees_slider.value <= 3
        else f"✅ With {n_trees_slider.value} trees, the average is much smoother."
    )

    mo.vstack([
        n_trees_slider,
        mo.callout(mo.md(_note), kind="info"),
        mo.as_html(_fig),
    ])
    return (bagged_y,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Boosting: Reducing Bias

    Boosting reduces *bias* by training models **sequentially** — each one focuses on the previous model's mistakes.

    ### How Gradient Boosting works:
    1. Start with a simple prediction (e.g., $\hat{y} = \bar{y}$)
    2. Compute residuals $r_i = y_i - \hat{y}_i$
    3. Fit a new **shallow** tree to the residuals
    4. Update: $\hat{y} \leftarrow \hat{y} + \eta \cdot \hat{r}$ where $\eta$ is the **learning rate**
    5. Repeat

    ### Key hyperparameters:
    - **Iterations**: more steps → more complex fit (overfitting risk grows)
    - **Learning rate $\eta$**: smaller = more conservative updates, need more iterations to converge

    The step-by-step visualization below makes this concrete.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Step-by-step: What boosting is actually doing

    Each row is one boosting iteration (η=0.5, max_depth=1 stumps).

    - **Left**: cumulative prediction after this step — watch it gradually trace the sine wave
    - **Right**: residuals the *next* tree will target, with the new stump's fit overlaid in orange

    Notice how residuals shrink and lose their sinusoidal pattern as the model extracts signal round by round.
    """)
    return


@app.cell
def _(DecisionTreeRegressor, X, mo, np, plt, y):
    _eta_demo = 0.5
    _n_steps_demo = 5
    _cumulative = np.full(len(X), y.mean())

    _fig, _axes = plt.subplots(_n_steps_demo, 2, figsize=(12, 3 * _n_steps_demo))

    for _step in range(_n_steps_demo):
        _resid = y - _cumulative
        _stump = DecisionTreeRegressor(max_depth=1)
        _stump.fit(X, _resid)
        _stump_pred = _stump.predict(X)
        _cumulative = _cumulative + _eta_demo * _stump_pred

        _ax_l = _axes[_step, 0]
        _ax_l.scatter(X, y, alpha=0.3, color="steelblue", s=20)
        _ax_l.plot(X, _cumulative, color="green", lw=2.5)
        _ax_l.set_ylim(-1.8, 1.8); _ax_l.set_ylabel("y")
        _ax_l.set_title(f"Step {_step + 1} — cumulative prediction", fontsize=10)
        if _step == _n_steps_demo - 1:
            _ax_l.set_xlabel("x")

        _ax_r = _axes[_step, 1]
        _ax_r.scatter(X, _resid, alpha=0.5, color="tomato", s=20, label="Residuals")
        _ax_r.plot(X, _stump_pred, color="orange", lw=2.5, label=f"New stump × η={_eta_demo}")
        _ax_r.axhline(0, color="black", lw=0.8, linestyle="--")
        _ax_r.set_ylim(-1.0, 1.0); _ax_r.set_ylabel("residual")
        _ax_r.set_title(f"Step {_step + 1} — residuals the stump targets", fontsize=10)
        if _step == 0:
            _ax_r.legend(fontsize=8)
        if _step == _n_steps_demo - 1:
            _ax_r.set_xlabel("x")

    plt.suptitle(
        f"Gradient Boosting — {_n_steps_demo} steps, η={_eta_demo}, max_depth=1",
        fontsize=12, y=1.01
    )
    plt.tight_layout()
    plt.close()

    mo.vstack([
        mo.as_html(_fig),
        mo.callout(mo.md(
            f"Each stump captures a coarse piece of the remaining signal. "
            f"After {_n_steps_demo} steps with η={_eta_demo}, the cumulative fit is already close "
            f"to the sine wave — without any single model seeing the full picture."
        ), kind="success"),
    ])
    return


@app.cell
def _(mo):
    boosting_steps = mo.ui.slider(1, 150, label="Boosting Iterations", value=1)
    lr_dropdown = mo.ui.dropdown(["0.01", "0.1", "0.5"], label="Learning Rate (η)", value="0.1")
    return boosting_steps, lr_dropdown


@app.cell
def _(GradientBoostingRegressor, X, boosting_steps, lr_dropdown, mo, plt, y):
    _gb = GradientBoostingRegressor(
        n_estimators=boosting_steps.value,
        learning_rate=float(lr_dropdown.value),
        max_depth=1,
    )
    _gb.fit(X, y)
    boosted_y = _gb.predict(X)
    _r2_gb = _gb.score(X, y)

    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    _axes[0].scatter(X, y, alpha=0.4, color="steelblue", label="Data")
    _axes[0].plot(X, boosted_y, color="green", lw=3, label=f"Boosted ({boosting_steps.value} steps)")
    _axes[0].set_title(f"Boosting fit  |  η={lr_dropdown.value}")
    _axes[0].set_xlabel("x"); _axes[0].legend()

    _resid_gb = y - boosted_y
    _axes[1].scatter(X, _resid_gb, alpha=0.5, color="tomato")
    _axes[1].axhline(0, color="black", lw=1, linestyle="--")
    _axes[1].set_title("Remaining residuals")
    _axes[1].set_xlabel("x"); _axes[1].set_ylabel("y − ŷ")
    _axes[1].set_ylim(-1, 1)

    plt.tight_layout()
    plt.close()

    _note_gb = (
        "⚠️ Still underfitting — try more iterations or a higher learning rate."
        if _r2_gb < 0.5
        else ("⚠️ Potentially overfitting — residuals show no remaining pattern."
              if _r2_gb > 0.97
              else f"✅ Good fit  (in-sample R² = {_r2_gb:.3f})")
    )

    mo.vstack([
        mo.hstack([boosting_steps, lr_dropdown]),
        mo.callout(mo.md(_note_gb), kind="info"),
        mo.as_html(_fig),
    ])
    return (boosted_y,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Stacking: The Meta-Learner

    **Stacking** asks: *given predictions from multiple models, how should we weight them?*

    Instead of a simple average, we let a **meta-learner** (here, OLS) learn the optimal weights:

    $$y = \beta_0 + \beta_1 \hat{y}^{\text{bagging}} + \beta_2 \hat{y}^{\text{boosting}} + \varepsilon$$

    - $\beta_1, \beta_2$: how much to trust each base model
    - p-values: whether each model adds information *beyond* what the other already provides

    ### Important caveat
    In practice, the meta-learner must be trained on **held-out (cross-validated) predictions**,
    not in-sample ones. Otherwise it will over-weight whichever model happened to fit training data best.
    Here we keep it simple for illustration.
    """)
    return


@app.cell
def _(bagged_y, boosted_y, mo, pd, sm, y):
    _df_stack = pd.DataFrame({"Bagging": bagged_y, "Boosting": boosted_y})
    _X_meta = sm.add_constant(_df_stack)
    _res = sm.OLS(y, _X_meta).fit()

    _trusted = "Boosting" if _res.params["Boosting"] > _res.params["Bagging"] else "Bagging"

    _coef_df = pd.DataFrame({
        "Model": ["Bagging", "Boosting"],
        "Weight (β)": [round(_res.params["Bagging"], 3), round(_res.params["Boosting"], 3)],
        "Std. Error": [round(_res.bse["Bagging"], 3), round(_res.bse["Boosting"], 3)],
        "P-Value": [round(_res.pvalues["Bagging"], 3), round(_res.pvalues["Boosting"], 3)],
    })

    mo.vstack([
        mo.hstack([
            mo.stat(label="Meta-learner R²", value=f"{_res.rsquared:.3f}"),
            mo.stat(label="Most trusted model", value=_trusted),
            mo.stat(label="Intercept", value=f"{_res.params['const']:.3f}"),
        ]),
        mo.md("**OLS meta-learner coefficients:**"),
        mo.ui.table(_coef_df),
        mo.md(f"""
**Interpretation:**
- Weight **{_res.params['Bagging']:.3f}** on bagging, **{_res.params['Boosting']:.3f}** on boosting.
- A p-value < 0.05 means that model contributes statistically significant information *beyond* the other.
- An intercept near 0 means neither model has a systematic bias.
        """),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    | Situation | Recommended approach |
    |-----------|---------------------|
    | No labeled target | **K-Means** (clustering) or **PCA** (dimensionality reduction) |
    | High-dimensional features ($p \gg n$) | **Lasso** for selection; then any supervised model |
    | Non-linear decision boundary | **SVM** with RBF kernel |
    | High variance / overfitting | **Bagging** / Random Forest |
    | High bias / underfitting | **Boosting** (XGBoost, LightGBM) |
    | Multiple diverse models available | **Stacking** |
    | Interpretability required | Single tree or linear model |

    ### Core tradeoffs to remember:
    > *Bagging reduces variance by averaging; boosting reduces bias by correcting errors; stacking learns which models to trust.*

    > *PCA reduces dimensions by finding variance; K-Means reduces observations by finding groups.*

    ### Going further:
    - **Random Forests** = Bagging + random feature subsets (more decorrelation between trees)
    - **XGBoost / LightGBM** = Gradient boosting with regularization, speed, and built-in missing-value handling
    - **Blending** = simplified stacking using a held-out validation set (no cross-validation needed)
    - **UMAP / t-SNE** = non-linear dimensionality reduction for visualization (alternative to PCA)
    - **LASSO + IV** = use Lasso to select instruments or controls in a causal framework (Belloni et al.)
    """)
    return


if __name__ == "__main__":
    app.run()
