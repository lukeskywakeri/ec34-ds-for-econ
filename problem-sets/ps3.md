# Problem Set 3

## Do 401(k) Plans Build Wealth? Machine Learning for Prediction and Causal Inference

A central question in household finance is whether tax-advantaged retirement savings accounts — like 401(k) plans — actually cause people to save more, or whether workers who enroll in them would have saved anyway. This is the classic **selection problem**: employees who are *eligible* for a 401(k) tend to be different from those who are not, so a naive comparison overstates the program's effect.

In this problem set you will use the 401(k) dataset from Chernozhukov et al. (2018) — a canonical dataset in applied econometrics — to do two things:

1. **Predict** net financial assets using machine learning.
2. **Estimate the causal effect** of 401(k) eligibility on net financial assets using Double Machine Learning (DML).

You can load the data directly from the `doubleml` package:

```python
from doubleml.datasets import fetch_401K
data = fetch_401K(return_type='DataFrame')
```

The key variables are:

| Variable | Description |
|----------|-------------|
| `net_tfa` | Net total financial assets (outcome, $Y$) |
| `e401` | 1 if eligible for a 401(k) plan (treatment, $D$) |
| `age`, `inc`, `fsize`, `educ`, `pira`, `married`, `two_earner`, `db` | Individual characteristics (controls, $X$) |

---

## Part 1: Predicting Net Financial Assets

Your goal is to understand the **bias-variance tradeoff** in practice by comparing several models' ability to predict `net_tfa` out of sample.

1. **Split** the data into a training set (80%) and a test set (20%). Use `random_state=42` for reproducibility.

2. **Train and evaluate** the following four models on the training set, then compute the **root mean squared error (RMSE)** on the test set for each:
   - OLS (using `statsmodels` or `sklearn`'s `LinearRegression`) with all controls
   - Ridge regression (tune `alpha` using 5-fold cross-validation on the training set)
   - LASSO (tune `alpha` using 5-fold cross-validation on the training set)
   - Random Forest (use `n_estimators=200`; tune `max_depth` over `[3, 5, 10, None]` using 5-fold cross-validation on the training set)

   Present your results in a single bar chart with model name on the x-axis and test RMSE on the y-axis.

3. **Learning curves**: For the best-performing model from step 2, plot a **learning curve** — that is, compute both training RMSE and test RMSE as you vary the training set size from 5% to 100% of the training data (use at least 10 evenly spaced points). Plot both curves on the same figure.

   What do you observe? Is the model high-variance, high-bias, or well-fit?

---

## Part 2: Causal Inference with Double Machine Learning

Now use the same dataset to answer a causal question: **What is the average treatment effect (ATE) of 401(k) eligibility (`e401`) on net financial assets (`net_tfa`)?**

1. **Naive OLS**: Run a simple OLS regression of `net_tfa` on `e401` and all controls $X$. Report the coefficient on `e401` and its standard error.

2. **Naive LASSO**: Use LASSO (with cross-validated `alpha`) to select controls, then regress `net_tfa` on `e401` and the selected controls. Report the coefficient on `e401` and its standard error.

   *Hint*: Fit LASSO on all variables including `e401`. Then re-run OLS with `e401` and whatever variables LASSO kept.

3. **Double Machine Learning**: Use the `DoubleML` library to implement DML with a Random Forest as the nuisance learner. Specifically, use `DoubleMLPLR` (the Partially Linear Regression model).

   ```python
   from doubleml import DoubleMLPLR
   from sklearn.ensemble import RandomForestRegressor

   # Your setup code here
   dml_plr = DoubleMLPLR(obj_dml_data, ml_l=RandomForestRegressor(...), ml_m=RandomForestRegressor(...))
   dml_plr.fit()
   print(dml_plr.summary)
   ```

   Report the ATE estimate and its 95% confidence interval.

4. **Compare** your three estimates (Naive OLS, Naive LASSO, DML) in a single coefficient plot: each estimate as a point with error bars showing the 95% confidence interval.

5. **Interpret**: In 3–5 sentences, explain *why* the DML estimate might differ from the naive OLS estimate. What role does the nuisance model play, and what assumption must hold for the DML estimate to be a valid causal effect?

---

## Submission Instructions

Submit a single `.zip` file containing:

- A Jupyter Notebook (`.ipynb`) with all code and answers. The notebook should run top-to-bottom without errors on any computer.
- A `requirements.txt` or `environment.yml` so that the environment is reproducible.
  - To export with conda: `conda env export --no-builds --file environment.yml`
  - To export with pip: `pip freeze > requirements.txt`

