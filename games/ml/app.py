"""
PROJECT OVERFIT
===============
EC34: Data Science for Economists — Machine Learning Assignment

The Federal Reserve's ML system, ECONBOT-3000, has been deployed with five
catastrophic configurations. You are an ML Emergency Responder. For each module,
run the provided code in your own Python/Jupyter environment, answer the question
based on your results, and submit the answer to unlock the next module.

Run with:
    uv run streamlit run games/ml/app.py
"""

import time
import streamlit as st

st.set_page_config(
    page_title="PROJECT OVERFIT",
    layout="wide",
    page_icon="🚨",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Answers (loaded once at startup, never displayed in the UI)
# ---------------------------------------------------------------------------
@st.cache_data
def load_answers():
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from data import ANSWERS
    return ANSWERS

ANSWERS = load_answers()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
MISSIONS = [1, 2, 3, 4, 5]
MISSION_NAMES = {
    1: "The Leaky Pipeline",
    2: "The High-Dimensional Trap",
    3: "Tree Depth Disaster",
    4: "The Cluster Conundrum",
    5: "Bagging from Scratch",
}

def _init():
    for key, default in [
        ("start_time", time.time()),
        ("completed", set()),
        ("current_mission", 1),
        ("attempts", {m: 0 for m in MISSIONS}),
        ("wrong_flash", {}),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

_init()

# ---------------------------------------------------------------------------
# Timer
# ---------------------------------------------------------------------------
LIMIT = 60 * 60  # 1 hour

def remaining():
    return max(0, LIMIT - (time.time() - st.session_state.start_time))

def fmt(secs):
    m, s = divmod(int(secs), 60)
    return f"{m:02d}:{s:02d}"

# ---------------------------------------------------------------------------
# Answer validation (tolerant float comparison)
# ---------------------------------------------------------------------------
def validate(mission, raw):
    correct = ANSWERS[mission]
    raw = raw.strip()
    try:
        return abs(float(raw) - float(correct)) < 0.005
    except ValueError:
        return raw.upper() == correct.upper()

# ---------------------------------------------------------------------------
# Reusable answer widget
# ---------------------------------------------------------------------------
def answer_box(mission, fmt_hint):
    if mission in st.session_state.completed:
        st.success(f"✅ Correct! The answer was **{ANSWERS[mission]}**")
        return

    st.markdown(f"**Format:** `{fmt_hint}`")
    col_in, col_btn = st.columns([3, 1])
    with col_in:
        user = st.text_input("Your answer", key=f"input_{mission}", label_visibility="collapsed")
    with col_btn:
        st.markdown("<div style='margin-top:0px'>", unsafe_allow_html=True)
        submit = st.button("Submit →", key=f"submit_{mission}", type="primary")

    if submit and user:
        st.session_state.attempts[mission] += 1
        if validate(mission, user):
            st.session_state.completed.add(mission)
            if mission + 1 in MISSIONS:
                st.session_state.current_mission = mission + 1
            st.rerun()
        else:
            n = st.session_state.attempts[mission]
            st.error(f"Incorrect — attempt {n}. Check your seeds and re-run the code.")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown("## 🚨 MISSION CONTROL")
        r = remaining()
        color = "green" if r > 1800 else "orange" if r > 600 else "red"
        st.markdown(
            f"<h2 style='color:{color}; font-family:monospace'>⏱ {fmt(r)}</h2>",
            unsafe_allow_html=True,
        )
        st.progress(r / LIMIT)
        st.markdown("---")
        st.markdown("### System Modules")
        for m in MISSIONS:
            done = m in st.session_state.completed
            current = m == st.session_state.current_mission
            icon = "✅" if done else ("🔧" if current else "🔒")
            label = f"{icon} {m}. {MISSION_NAMES[m]}"
            if done or current:
                if st.button(label, key=f"nav_{m}"):
                    st.session_state.current_mission = m
                    st.rerun()
            else:
                st.caption(f"🔒 {m}. {MISSION_NAMES[m]}")
        st.markdown("---")
        n = len(st.session_state.completed)
        st.markdown(f"**Progress:** {n} / {len(MISSIONS)} modules fixed")
        st.progress(n / len(MISSIONS))
        st.markdown("---")
        st.markdown("""
**How to play**
1. Read the mission brief
2. Use the provided notebook and fill in the missing pieces
3. Run it — inspect the output
4. Enter your answer above
""")

# ---------------------------------------------------------------------------
# Missions
# ---------------------------------------------------------------------------

def mission_1():
    st.markdown("""
## 🔴 Module 1 — The Leaky Pipeline

> **ECONBOT diagnostic:** Training R² = 0.89 on a dataset of **pure random noise**.
> Something is very wrong.

The intern who built ECONBOT's preprocessing pipeline selected the "best" features
by correlating them with the target — *before* doing the train/test split.
This is **data leakage**: the test set silently informed the feature selection,
so the model appears to generalise when it doesn't.

Your task is to run **both** pipelines below, compare their test R², and
report what the leaky pipeline claims to achieve.
""")

    st.code("""\
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

np.random.seed(99)
X = np.random.randn(100, 500)   # 500 features — ALL pure noise
y = np.random.randn(100)        # target   — also pure noise

# ── PIPELINE A  (leaky) ─────────────────────────────────────────────────────
# Select the 25 features most correlated with y … using ALL 100 observations.
corrs   = np.abs(np.corrcoef(X.T, y)[-1, :-1])
top_idx = np.argsort(corrs)[-25:]
X_sel   = X[:, top_idx]

X_tr_a, X_te_a, y_tr_a, y_te_a = train_test_split(X_sel, y, test_size=0.3, random_state=7)
model_a = LinearRegression().fit(X_tr_a, y_tr_a)
r2_a    = r2_score(y_te_a, model_a.predict(X_te_a))

# ── PIPELINE B  (correct) ────────────────────────────────────────────────────
# Split FIRST, then select features using training data only.
X_tr_b, X_te_b, y_tr_b, y_te_b = train_test_split(X, y, test_size=0.3, random_state=7)
corrs_b   = np.abs(np.corrcoef(X_tr_b.T, y_tr_b)[-1, :-1])
top_idx_b = np.argsort(corrs_b)[-25:]
model_b   = LinearRegression().fit(X_tr_b[:, top_idx_b], y_tr_b)
r2_b      = r2_score(y_te_b, model_b.predict(X_te_b[:, top_idx_b]))

print(f"Pipeline A (leaky)   test R²: {r2_a:.2f}")
print(f"Pipeline B (correct) test R²: {r2_b:.2f}")
""", language="python")

    st.markdown("""
> **Reminder:** Both datasets contain **zero true signal** — X and y are independent
> random noise. Any positive R² from Pipeline A is entirely an artefact of leakage.

---
### What to submit
""")
    st.markdown("**Question:** What is the test R² reported by **Pipeline A** (the leaky one)?")
    answer_box(1, "a decimal rounded to 2 places, e.g. 0.34")


def mission_2():
    st.markdown("""
## 🔴 Module 2 — The High-Dimensional Trap

> **ECONBOT diagnostic:** GDP forecasting model trained with **200 economic indicators**
> on only **100 quarterly observations**. OLS was used. Training R² was near-perfect.
> The next out-of-sample quarter: complete disaster.

When the number of features exceeds the number of observations, OLS can always
fit the training data perfectly — but it memorises noise instead of signal.
This is the **overfitting** failure mode: low bias, catastrophically high variance.

**Lasso** adds an L1 penalty that forces most coefficients to exactly zero,
keeping only the features that genuinely predict the target.
Your job: fit LassoCV and find out how many features survive.
""")

    st.code("""\
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(0)
X, y = make_regression(noise=4, random_state=0, n_samples=100, n_features=200)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=123)

# ── Scale on training data only ───────────────────────────────────────────────
scaler = StandardScaler().fit(X_tr)
X_tr_s = scaler.transform(X_tr)
X_te_s = scaler.transform(X_te)

# ── Fit LassoCV (cross-validates over alpha automatically) ────────────────────
lasso = LassoCV(alphas=np.linspace(0.1, 1, 30), random_state=0, max_iter=10000)
lasso.fit(X_tr_s, y_tr)

# ── Count surviving features ──────────────────────────────────────────────────
n_nonzero = (np.abs(lasso.coef_) >= 1e-6).sum()
print(f"Optimal alpha  : {lasso.alpha_:.3f}")
print(f"Non-zero coefs : {n_nonzero} out of 200")
print(f"Train R²       : {lasso.score(X_tr_s, y_tr):.3f}")
print(f"Test  R²       : {lasso.score(X_te_s, y_te):.3f}")
""", language="python")

    st.info("""
**Tip:** The features with `|coef| < 1e-6` have been shrunk to exactly zero by Lasso.
The rest are the features ECONBOT actually needs to predict GDP growth.
""")

    st.markdown("---")
    st.markdown("**Question:** How many features have **non-zero** Lasso coefficients?")
    answer_box(2, "a whole number, e.g. 45")


def mission_3():
    st.markdown("""
## 🔴 Module 3 — Tree Depth Disaster

> **ECONBOT diagnostic:** The inflation forecasting module uses a decision tree
> with `max_depth=20`. Train R² = 0.99. Test R² = 0.04. Classic overfit.

The intern hard-coded the deepest possible tree. Deeper trees fit training data
better but generalise worse — the classic **bias–variance tradeoff**.

You need to find the optimal `max_depth` using **5-fold cross-validation**:
try depths 1 through 10, compute the mean CV R² for each, and pick the winner.
""")

    st.code("""\
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score

np.random.seed(1)
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel()
y[::5] += 3 * (0.5 - np.random.rand(16))   # add noise to every 5th point

# ── 5-fold CV over depths 1–10 ────────────────────────────────────────────────
cv_scores = {}
for depth in range(1, 11):
    scores = cross_val_score(
        DecisionTreeRegressor(max_depth=depth),
        X, y, cv=5, scoring="r2"
    )
    cv_scores[depth] = scores.mean()
    print(f"max_depth={depth:2d}  mean CV R² = {scores.mean():.4f}")

best_depth = max(cv_scores, key=cv_scores.get)
print(f"\\nBest max_depth: {best_depth}")
""", language="python")

    st.markdown("""
> **Interpretation guide**
> - A depth that's **too low** → high bias, low variance → mean CV R² is modest
>   because the tree misses the true pattern.
> - A depth that's **too high** → low bias, high variance → mean CV R² drops
>   because each fold's tree memorises its own training noise.
> - The **best depth** balances both.

---
""")
    st.markdown("**Question:** What `max_depth` achieves the **highest** mean 5-fold CV R²?")
    answer_box(3, "a whole number between 1 and 10")


def mission_4():
    st.markdown("""
## 🔴 Module 4 — The Cluster Conundrum

> **ECONBOT diagnostic:** The country-segmentation module was set to `k=1`.
> One cluster for 195 countries. Every nation gets the same policy recommendation.

ECONBOT needs to segment countries into economically homogeneous groups for
targeted policy. Your task: use the **elbow method** to find the right number of
clusters, then fit K-Means with that k and report the resulting inertia.

**Remember:** K-Means should always be applied to standardised features —
otherwise variables measured in large units dominate the distance calculation.
""")

    st.code("""\
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
X_raw, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=42)

# ── Standardise ───────────────────────────────────────────────────────────────
X = StandardScaler().fit_transform(X_raw)

# ── Elbow plot: compute inertia for k = 1 … 8 ────────────────────────────────
inertias = {}
for k in range(1, 9):
    km = KMeans(n_clusters=k, random_state=42, n_init="auto")
    km.fit(X)
    inertias[k] = km.inertia_
    print(f"k={k}  inertia={km.inertia_:.1f}")

plt.figure(figsize=(7, 4))
plt.plot(list(inertias.keys()), list(inertias.values()), "o-")
plt.xlabel("k"); plt.ylabel("Inertia"); plt.title("Elbow Plot"); plt.grid(alpha=0.3)
plt.show()

# ── After choosing the optimal k, fit and inspect ────────────────────────────
# TODO: replace ??? with the k you identified from the elbow
best_k = ???
km_best = KMeans(n_clusters=best_k, random_state=42, n_init="auto").fit(X)
print(f"\\nInertia at k={best_k}: {km_best.inertia_:.0f}")
print(f"Cluster sizes: {np.bincount(km_best.labels_)}")
""", language="python")

    st.warning("""
**Note on standardisation:** The code above standardises `X_raw` before clustering.
Make sure you fit K-Means on `X` (standardised), not `X_raw`.
The inertia you report should come from the standardised version.
""")

    st.markdown("""
> **Reading the elbow:** Look for the value of k where adding one more cluster
> gives much smaller inertia reduction than the step before it.

---
""")
    st.markdown("**Question:** Fit `KMeans(n_clusters=4, random_state=42)` on the **standardised** data. "
                "What is the inertia rounded to the **nearest whole number**?")
    answer_box(4, "a whole number")


def mission_5():
    st.markdown("""
## 🔴 Module 5 — Bagging from Scratch

> **ECONBOT diagnostic:** The volatility-forecasting module is a single
> fully-grown decision tree (`max_depth=None`). Train R² = 1.00. Test R² ≈ 0.
> High variance. Memorising noise.

A fully-grown decision tree has near-zero bias but extremely high variance —
each new training set produces a wildly different tree.

**Bagging** (Bootstrap Aggregating) fixes this by:
1. Drawing 50 bootstrap samples (sample with replacement) from the training set
2. Fitting one fully-grown tree on each
3. Averaging their predictions

Averaging over many trees trained on slightly different data cancels out the
idiosyncratic noise each tree fits, reducing variance without increasing bias.

Your task: implement bagging from scratch using the loop below.
""")

    st.code("""\
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

np.random.seed(2026)
X = np.sort(5 * np.random.rand(80, 1), axis=0)
y = np.sin(X).ravel() + np.random.normal(0, 0.2, 80)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=7)

# ── Baseline: single fully-grown tree ────────────────────────────────────────
single = DecisionTreeRegressor(max_depth=None).fit(X_tr, y_tr)
print(f"Single tree  train R²: {r2_score(y_tr, single.predict(X_tr)):.3f}")
print(f"Single tree  test  R²: {r2_score(y_te, single.predict(X_te)):.3f}")

# ── Bagging: 50 trees on bootstrap samples ───────────────────────────────────
np.random.seed(0)                           # fix this seed!
bag_preds = np.zeros((len(X_te), 50))

for i in range(50):
    idx = np.random.randint(0, len(X_tr), len(X_tr))   # bootstrap indices
    t   = DecisionTreeRegressor(max_depth=None).fit(X_tr[idx], y_tr[idx])
    bag_preds[:, i] = t.predict(X_te)

bagged_pred = bag_preds.mean(axis=1)        # average across all 50 trees
r2_bag = r2_score(y_te, bagged_pred)
print(f"\\nBagged ensemble (50 trees) test R²: {r2_bag:.3f}")
""", language="python")

    st.markdown("""
> **What to look for:**
> - The single tree's train R² should be 1.000 (perfect memorisation).
> - Its test R² will be much lower — that gap is the variance problem.
> - Bagging's test R² should be noticeably higher — variance reduced.
>
> **Why does this work?** Each bootstrap sample omits ~37% of the training points
> at random, so each tree fits slightly different data and makes slightly different
> errors. Averaging cancels those errors out.

---
""")
    st.markdown("**Question:** What is the **test R²** of the 50-tree bagged ensemble?")
    answer_box(5, "a decimal rounded to 3 places, e.g. 0.863")


# ---------------------------------------------------------------------------
# Victory
# ---------------------------------------------------------------------------
def victory():
    elapsed = time.time() - st.session_state.start_time
    m, s = divmod(int(elapsed), 60)
    total_attempts = sum(st.session_state.attempts.values())

    st.balloons()
    st.markdown(f"""
<div style="text-align:center; padding:2rem; border:3px solid #51cf66;
            border-radius:12px; background:#0d2b0d; margin-bottom:2rem">
  <h1 style="color:#51cf66; font-family:monospace; margin:0">
    ✅ ECONBOT-3000 STABILISED
  </h1>
  <h3 style="color:white">All five modules repaired. The FOMC meeting is saved.</h3>
  <p style="color:#aaa; font-size:1.1rem">
    Time: <strong style="color:white">{m}m {s}s</strong>
    &nbsp;|&nbsp;
    Total attempts: <strong style="color:white">{total_attempts}</strong>
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
### What you diagnosed and fixed

| Module | Bug | ML concept | Fix |
|--------|-----|-----------|-----|
| 1 | Feature selection before split | **Data leakage** | Always fit preprocessing inside the training fold |
| 2 | OLS with p > n | **Overfitting / high variance** | Lasso regularisation forces irrelevant β → 0 |
| 3 | max_depth hard-coded to 20 | **Bias–variance tradeoff** | Choose hyperparameters with cross-validation |
| 4 | k = 1 for all countries | **Unsupervised learning** | Use the elbow method to select k |
| 5 | Single deep tree | **High variance** | Bagging averages over bootstrap samples |

These five failure modes appear constantly in applied economic ML research.
You now know how to spot and fix all of them.
""")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
def header():
    st.markdown("""
<div style="border-left:4px solid #ff6b6b; padding:0.5rem 1rem; margin-bottom:1.5rem;
            background:#1a0a0a;">
  <h1 style="color:#ff6b6b; font-family:monospace; margin:0">🚨 PROJECT OVERFIT</h1>
  <p style="color:#aaa; margin:0.2rem 0 0">
    Federal Reserve ML Emergency — ECONBOT-3000 System Repair
  </p>
</div>
""", unsafe_allow_html=True)

    st.info("""
**How this works:** Each module gives you a scenario, an explanation, and a code block.
Use the provided notebook, run it, inspect the output,
and enter the answer below. The seeds are fixed — your numbers will match exactly.
""")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    render_sidebar()

    if remaining() == 0:
        st.error("⏰ Time's up — ECONBOT is presenting garbage forecasts at the FOMC meeting.")

    if len(st.session_state.completed) == len(MISSIONS):
        victory()
        return

    header()

    m = st.session_state.current_mission
    {1: mission_1, 2: mission_2, 3: mission_3, 4: mission_4, 5: mission_5}[m]()


main()
