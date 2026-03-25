import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import pyfixest as pf

    return np, pd, pf


@app.cell
def _(mo):
    mo.md(r"""
    ## PROBLEM 1
    """)
    return


@app.cell
def _(np, pd):
    df =pd.DataFrame({
        'user_id': np.arange(1000),
        'pre_experiment_spend' : np.random.exponential(scale=100, size=1000),
        'is_treated' : np.random.binomial(1, 0.5, size=1000),
        'city_id' : np.random.choice(['NY', 'LA', 'CHI'], size=1000)
    }).assign(
        post_experiment_spend = lambda x: 10 + 0.5 * x['pre_experiment_spend'] + 5 * x['is_treated'] + np.random.normal(0, 10, size=1000)
    )
    return (df,)


@app.cell
def _(df, pf):
    pf.feols("post_experiment_spend ~ is_treated +pre_experiment_spend", data=df).summary()
    return


@app.cell
def _(df, np):
    def cuped(y= 'post_experiment_spend', X='pre_experiment_spend'):
        # adjust Y by pre-experiment spend
        theta = np.cov(df[y], df[X])[0,1] / np.var(df[X])

        cuped_adjustment = df[y] - theta*(df[X] - df[X].mean())

        # calculate mean difference

        y_post = cuped_adjustment[df['is_treated'] == 1]
        y_control = cuped_adjustment[df['is_treated'] == 0]

        len_y_post = y_post.shape[0]

        len_y_pre = y_control.shape[0]

        var_diff = np.sqrt((1/len_y_post)*y_post.var(ddof=1) + (1/len_y_pre)*y_control.var(ddof=1))

        return y_post.mean() - y_control.mean(), var_diff


    return (cuped,)


@app.cell
def _(cuped):
    cuped("post_experiment_spend", "pre_experiment_spend")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Problem 2
    """)
    return


@app.cell
def _(np):
    np.min(np.nan, 0)
    return


@app.cell
def _(np, pd):
    dates = pd.date_range(start='2021-01-01', periods= 1000, freq='30min')

    df_switch = pd.DataFrame({
        'date' : dates,
        'is_treated' : np.random.choice([0,1], size=1000)
    }).assign(
        y = lambda df: 50 + df['is_treated']*20 + df['is_treated'].shift().fillna(0)*10 + np.random.normal(0, 5, size=1000)
    )


    # naive mean is biased
    y_treat = df_switch.query("is_treated == 1")['y'].mean()
    y_control = df_switch.query("is_treated==0")['y'].mean()

    print(y_treat - y_control)

    # now drop the burn-in periods
    no_burnin = df_switch.query("not (is_treated.shift() == 1)")

    y_treat_noburn = no_burnin.query("is_treated == 1")['y'].mean()
    y_control_noburn = no_burnin.query("is_treated==0")['y'].mean()

    print(y_treat_noburn - y_control_noburn)


    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Problem 4
    """)
    return


@app.cell
def _(pd):
    df_matching = pd.read_json("data/marketplace_matching.json")
    return


if __name__ == "__main__":
    app.run()
