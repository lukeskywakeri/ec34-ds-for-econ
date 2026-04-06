import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import GradientBoostingRegressor

    return (
        DecisionTreeRegressor,
        GradientBoostingRegressor,
        mo,
        np,
        pd,
        plt,
        sm,
    )


@app.cell
def _(np):
    # Data Generation: shared across all cells
    np.random.seed(2026)
    X = np.sort(5 * np.random.rand(80, 1), axis=0)
    y = np.sin(X).ravel() + np.random.normal(0, 0.2, X.shape[0])
    return X, y


@app.cell
def _(mo):
    mo.md(r"""
    # Ensemble Methods

    ## What is an Ensemble?

    A single model is like a single musician — talented, but limited.
    An **ensemble** combines many models, just like an orchestra combines many instruments.

    **Key insight:** If each model makes *different* mistakes, averaging them out produces a better prediction than any one model alone.

    ---

    ## The Three Big Ideas

    | Method | Problem it solves | Strategy |
    |--------|-------------------|----------|
    | **Bagging** | High variance (overfitting) | Train many models in parallel on random subsets; average |
    | **Boosting** | High bias (underfitting) | Train models sequentially, each correcting the last |
    | **Stacking** | Which model to trust? | Use a *meta-learner* to learn optimal weights |

    ---

    ## Our Running Example

    We have 80 noisy observations of $y = \sin(x) + \varepsilon$ where $\varepsilon \sim \mathcal{N}(0, 0.2)$.
    The true signal is a sine wave — but our models don't know that.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 1: Bagging 🌳🌳🌳

    **B**ootstrap **Agg**regat**ing** reduces *variance* by averaging many trees.

    ### How it works:
    1. Draw $B$ bootstrap samples (sample with replacement from the training data)
    2. Fit one decision tree on each bootstrap sample
    3. **Average** the predictions: $\hat{y} = \frac{1}{B} \sum_{b=1}^B \hat{y}_b$

    ### Why does averaging help?
    - Each tree is noisy (high variance), but *different* samples → *different* errors
    - Errors cancel out when you average: $\text{Var}(\bar{X}) = \frac{\sigma^2}{n}$
    - Bias stays the same; variance falls with more trees

    > **Try it:** Move the slider. Notice how the red curve gets smoother as you add more trees.
    """)
    return


@app.cell
def _(mo):
    n_trees_slider = mo.ui.slider(1, 50, label="Number of Trees (n_estimators)", value=1)
    return (n_trees_slider,)


@app.cell
def _(DecisionTreeRegressor, X, mo, n_trees_slider, np, plt, y):
    _preds = np.zeros((len(X), n_trees_slider.value))
    for _i in range(n_trees_slider.value):
        _idx = np.random.randint(0, len(X), len(X))
        _tree = DecisionTreeRegressor(max_depth=2).fit(X[_idx], y[_idx])
        _preds[:, _i] = _tree.predict(X)
    bagged_y = _preds.mean(axis=1)

    _fig, _ax = plt.subplots(figsize=(9, 4))
    _ax.scatter(X, y, alpha=0.4, label="Data", color="steelblue")
    if n_trees_slider.value == 1:
        _ax.plot(
            X, _preds[:, 0], color="orange", lw=2, alpha=0.7, label="Single tree (noisy)"
        )
    _ax.plot(
        X,
        bagged_y,
        color="red",
        lw=3,
        label=f"Bagged average ({n_trees_slider.value} trees)",
    )
    _ax.set_title(f"Bagging: {n_trees_slider.value} tree(s)")
    _ax.set_xlabel("x")
    _ax.set_ylabel("y")
    _ax.legend()
    plt.tight_layout()
    plt.close()

    _variance_note = (
        "⚠️ With just 1 tree, you can see the jagged, noisy fit."
        if n_trees_slider.value <= 3
        else f"✅ With {n_trees_slider.value} trees, the average is much smoother."
    )

    mo.vstack([
        n_trees_slider,
        mo.callout(mo.md(_variance_note), kind="info"),
        mo.as_html(_fig),
    ])
    return (bagged_y,)


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 2: Boosting 🚀

    Boosting reduces *bias* by training models **sequentially**, each one focusing on the previous model's mistakes.

    ### How Gradient Boosting works:
    1. Start with a simple prediction (e.g., the mean of $y$)
    2. Compute the **residuals** $r_i = y_i - \hat{y}_i$
    3. Fit a new (shallow) tree to the residuals
    4. Update: $\hat{y} \leftarrow \hat{y} + \eta \cdot \hat{r}$ where $\eta$ is the **learning rate**
    5. Repeat

    ### Key hyperparameters:
    - **Iterations**: more steps → more complex fit (risk of overfitting eventually)
    - **Learning rate** $\eta$: smaller = more conservative steps, need more iterations

    > **Try it:** Watch the green curve "chase" the data as iterations increase.
    > A high learning rate with few steps can overshoot; a low rate needs many steps to converge.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 🔬 Step-by-step: What boosting is actually doing

    Each row below is one boosting iteration.

    - **Left panel**: the cumulative prediction so far (what the model *currently* thinks)
    - **Right panel**: the residuals $r = y - \hat{y}$ (the signal the *next* tree will try to fit), with the new tree's fit overlaid in orange

    Notice how the residuals shrink and lose their pattern as iterations progress — that's the model extracting signal round by round.
    """)
    return


@app.cell
def _(DecisionTreeRegressor, X, mo, np, plt, y):
    _eta = 0.5  # learning rate for the illustration
    _n_steps = 5  # number of steps to show
    _max_depth = 1  # shallow stumps

    _cumulative = np.full(len(X), y.mean())  # start from the mean

    _fig, _axes = plt.subplots(_n_steps, 2, figsize=(12, 3 * _n_steps))

    for _step in range(_n_steps):
        _resid = y - _cumulative
        _stump = DecisionTreeRegressor(max_depth=_max_depth)
        _stump.fit(X, _resid)
        _stump_pred = _stump.predict(X)
        _update = _eta * _stump_pred
        _cumulative = _cumulative + _update

        # Left: cumulative fit so far (AFTER this update)
        _ax_l = _axes[_step, 0]
        _ax_l.scatter(X, y, alpha=0.3, color="steelblue", s=20)
        _ax_l.plot(X, _cumulative, color="green", lw=2.5)
        _ax_l.set_ylim(-1.8, 1.8)
        _ax_l.set_ylabel("y")
        _ax_l.set_title(f"Step {_step + 1} — cumulative prediction", fontsize=10)
        if _step == _n_steps - 1:
            _ax_l.set_xlabel("x")

        # Right: residuals before this update + the stump fit
        _ax_r = _axes[_step, 1]
        _ax_r.scatter(X, _resid, alpha=0.5, color="tomato", s=20, label="Residuals")
        _ax_r.plot(X, _stump_pred, color="orange", lw=2.5, label=f"New stump × η={_eta}")
        _ax_r.axhline(0, color="black", lw=0.8, linestyle="--")
        _ax_r.set_ylim(-1.0, 1.0)
        _ax_r.set_ylabel("residual")
        _ax_r.set_title(f"Step {_step + 1} — residuals the stump targets", fontsize=10)
        if _step == 0:
            _ax_r.legend(fontsize=8)
        if _step == _n_steps - 1:
            _ax_r.set_xlabel("x")

    plt.suptitle(
        f"Gradient Boosting — {_n_steps} steps, η={_eta}, max_depth={_max_depth}",
        fontsize=12,
        y=1.01,
    )
    plt.tight_layout()
    plt.close()

    mo.vstack([
        mo.as_html(_fig),
        mo.callout(
            mo.md(
                f"Each stump only captures a coarse piece of the remaining signal. "
                f"After {_n_steps} steps with η={_eta}, the cumulative fit is already close to the sine wave — "
                f"without any single model seeing the full picture."
            ),
            kind="success",
        ),
    ])
    return


@app.cell
def _(mo):
    boosting_steps = mo.ui.slider(1, 150, label="Boosting Iterations", value=1)
    lr_dropdown = mo.ui.dropdown(
        ["0.01", "0.1", "0.5"], label="Learning Rate (η)", value="0.1"
    )
    return boosting_steps, lr_dropdown


@app.cell
def _(GradientBoostingRegressor, X, boosting_steps, lr_dropdown, mo, plt, y):
    _model = GradientBoostingRegressor(
        n_estimators=boosting_steps.value,
        learning_rate=float(lr_dropdown.value),
        max_depth=1,
    )
    _model.fit(X, y)
    boosted_y = _model.predict(X)

    _r2 = _model.score(X, y)

    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))

    # Left: fit
    _axes[0].scatter(X, y, alpha=0.4, color="steelblue", label="Data")
    _axes[0].plot(
        X, boosted_y, color="green", lw=3, label=f"Boosted ({boosting_steps.value} steps)"
    )
    _axes[0].set_title(f"Boosting fit  |  η={lr_dropdown.value}")
    _axes[0].set_xlabel("x")
    _axes[0].legend()

    # Right: residuals
    _resid = y - boosted_y
    _axes[1].scatter(X, _resid, alpha=0.5, color="tomato")
    _axes[1].axhline(0, color="black", lw=1, linestyle="--")
    _axes[1].set_title("Remaining residuals")
    _axes[1].set_xlabel("x")
    _axes[1].set_ylabel("y − ŷ")
    _axes[1].set_ylim(-1, 1)

    plt.tight_layout()
    plt.close()

    _note = (
        "⚠️ Still underfitting — try more iterations or a higher learning rate."
        if _r2 < 0.5
        else (
            "⚠️ Potentially overfitting — residuals have no pattern left to exploit."
            if _r2 > 0.97
            else f"✅ Good fit  (in-sample R² = {_r2:.3f})"
        )
    )

    mo.vstack([
        mo.hstack([boosting_steps, lr_dropdown]),
        mo.callout(mo.md(_note), kind="info"),
        mo.as_html(_fig),
    ])
    return (boosted_y,)


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Part 3: Stacking 🏗️

    **Stacking** asks: *given predictions from multiple models, how should we combine them?*

    Instead of a simple average, we let a **meta-learner** (here, OLS) figure out the optimal weights.

    ### Setup:
    $$y = \beta_0 + \beta_1 \hat{y}^{\text{bagging}} + \beta_2 \hat{y}^{\text{boosting}} + \varepsilon$$

    - $\beta_1$ tells us how much to trust the bagged forest
    - $\beta_2$ tells us how much to trust the boosted model
    - The p-values tell us which contributions are statistically meaningful

    ### Caveat (important for your homework!):
    In practice, the meta-learner should be trained on **held-out predictions** (cross-validation),
    not in-sample predictions. Otherwise the meta-learner can overfit. Here we keep it simple.
    """)
    return


@app.cell
def _(bagged_y, boosted_y, mo, pd, sm, y):
    _df = pd.DataFrame({"Bagging": bagged_y, "Boosting": boosted_y})
    _X_meta = sm.add_constant(_df)
    _res = sm.OLS(y, _X_meta).fit()

    _trusted = "Boosting" if _res.params["Boosting"] > _res.params["Bagging"] else "Bagging"

    _coef_df = pd.DataFrame({
        "Model": ["Bagging", "Boosting"],
        "Weight (β)": [round(_res.params["Bagging"], 3), round(_res.params["Boosting"], 3)],
        "Std. Error": [round(_res.bse["Bagging"], 3), round(_res.bse["Boosting"], 3)],
        "P-Value": [round(_res.pvalues["Bagging"], 3), round(_res.pvalues["Boosting"], 3)],
    })

    _stats = mo.hstack([
        mo.stat(label="Meta-learner R²", value=f"{_res.rsquared:.3f}"),
        mo.stat(label="Most trusted model", value=_trusted),
        mo.stat(label="Intercept", value=f"{_res.params['const']:.3f}"),
    ])

    mo.vstack([
        _stats,
        mo.md("**OLS meta-learner coefficients:**"),
        mo.ui.table(_coef_df),
        mo.md(f"""
    **Interpretation:**
    - The meta-learner assigns weight **{_res.params["Bagging"]:.3f}** to bagging and **{_res.params["Boosting"]:.3f}** to boosting.
    - A p-value < 0.05 means that model's predictions carry statistically significant information *beyond* what the other model provides.
    - The intercept being close to 0 means neither model has a systematic bias.
        """),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Summary: When to use each method?

    | Situation | Recommended method |
    |-----------|-------------------|
    | Your model overfits (high variance) | **Bagging** / Random Forest |
    | Your model underfits (high bias) | **Boosting** (XGBoost, LightGBM) |
    | You have several diverse models | **Stacking** |
    | You need interpretability | Single decision tree or linear model |

    ### The bias–variance tradeoff in one sentence:
    > *Bagging reduces variance by averaging; boosting reduces bias by correcting errors; stacking learns which models to trust.*

    ### Going further:
    - **Random Forests** = Bagging + random feature subsets (even more decorrelation)
    - **XGBoost / LightGBM** = Gradient boosting with regularization and speed tricks
    - **Blending** = a simpler version of stacking using a holdout set instead of cross-validation
    """)
    return


if __name__ == "__main__":
    app.run()
