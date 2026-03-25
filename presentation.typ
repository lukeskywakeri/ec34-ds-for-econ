// Python for Social Scientists — Typst Presentation using Touying
// Compile: typst compile presentation.typ

#import "@preview/touying:0.6.1": *
#import themes.university: *

#show: university-theme.with(
  aspect-ratio: "16-9",
  config-info(
    title: [Python for Social Scientists],
    subtitle: [A Practical Introduction for Researchers],
    author: [EC34: Data Science for Economists],
    date: [Spring 2026],
    institution: [Swarthmore College],
  ),
  config-colors(
    primary: rgb("#6D1D44"),
    secondary: rgb("#2D6A4F"),
    tertiary: rgb("#264653"),
  ),
)

#set text(size: 20pt)
#show raw: set text(size: 16pt)

// ============================================================
// Title Slide
// ============================================================

#title-slide()

// ============================================================
// PART I: Why Python?
// ============================================================

= Why Python?

// --- Slide 2 ---

== The Reproducibility Crisis

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === The Problem
    - You finish a paper. A referee asks: "What happens if you drop observations before 1990?"
    - You open your Excel file. You can't remember which cells you edited, which columns you deleted, or in what order
    - _60% of economics papers_ cannot be reproduced, even with the original data (Chang & Li, 2022)
  ],
  [
    === The Solution: Code
    - A script is a *complete record* of every step from raw data to final result
    - Anyone can re-run it and get the _exact same output_
    - Change one assumption? Edit one line, re-run everything
    - Your future self will thank you
  ],
)

#align(center)[
  #text(fill: rgb("#6D1D44"), weight: "bold", size: 22pt)[
    If your analysis cannot be reproduced, it cannot be verified.
  ]
]

// --- Slide 3 ---

== Why Python?

- *Free and open-source* — no license fees, no institutional restrictions, runs anywhere
- *The most widely used language in data science* — more tutorials, answers, and community support than any alternative
- *Not just statistics* — the same language can scrape websites, call APIs, process text, analyze satellite images, and run machine learning models
- *Readable* — Python reads almost like English, making it easier to learn and share with collaborators
- *Interoperable* — you can call Stata and R _from within_ Python, so nothing is lost

#v(0.5em)

```python
# This is valid Python — readable, concise, expressive
df = pd.read_csv("survey_data.csv")
avg_income = df.groupby("region")["income"].mean()
```

// --- Slide 4 ---

== Python vs. Other Tools

#align(center)[
#table(
  columns: (auto, auto, auto, auto, auto),
  inset: 8pt,
  align: center,
  stroke: 0.5pt,
  table.header([], [*Stata*], [*R*], [*Excel*], [*Python*]),
  [Cost], [Expensive], [Free], [Paid], [Free],
  [Econometrics], [Excellent], [Excellent], [Limited], [Very Good],
  [Machine Learning], [Limited], [Good], [None], [Excellent],
  [Data Wrangling], [Good], [Excellent], [Poor], [Excellent],
  [Visualization], [Good], [Excellent], [Good], [Excellent],
  [Web Scraping], [None], [Moderate], [None], [Excellent],
  [Text / NLP / AI], [None], [Good], [None], [Excellent],
  [Scalability], [Limited], [Moderate], [Very Limited], [Excellent],
)
]

#text(size: 18pt)[
  Python is not the best at any single task — it is the best _general-purpose_ tool for modern social science.
]

// --- Slide 5 ---

== The Python Ecosystem for Social Science

There is a mature Python library for nearly everything a social scientist needs:

#v(0.5em)

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 1.5em,
  [
    === Data & Econometrics
    - *pandas* — data manipulation
    - *statsmodels* — regression, MLE
    - *pyfixest* — panel fixed effects
    - *rdrobust* — regression discontinuity
  ],
  [
    === Visualization & Mapping
    - *matplotlib / seaborn* — static plots
    - *plotly* — interactive charts
    - *geopandas / folium* — maps
    - *geemap* — satellite imagery
  ],
  [
    === ML, Text & AI
    - *scikit-learn* — machine learning
    - *doubleml / econml* — causal ML
    - *openai* — LLM APIs
    - *pytorch* — deep learning
  ],
)

#v(0.5em)

You don't need to learn all of these. Most projects use only 3-4.

// --- Slide 6 ---

== Jupyter Notebooks: Your Lab Notebook

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    Jupyter notebooks let you combine *writing*, *code*, and *results* in a single interactive document — like a lab notebook for data analysis.

    - Write explanations in plain English alongside your code
    - See tables, plots, and maps appear _immediately_ below each code cell
    - Share the notebook on GitHub — anyone can read your analysis and reproduce it
    - Export to PDF for journal submission
  ],
  [
    ```python
    # Load the data
    df = pd.read_csv("survey_data.csv")

    # Average income by region
    df.groupby("region")["income"].mean()
    ```
    #v(0.3em)
    #text(size: 16pt, fill: gray)[
      A formatted table appears here instantly.
    ]
    #v(0.3em)
    ```python
    # Visualize the distribution
    df["income"].plot(kind="hist")
    ```
    #text(size: 16pt, fill: gray)[
      A histogram appears here instantly.
    ]
  ],
)

// ============================================================
// PART II: Working with Data
// ============================================================

= Working with Data

// --- Slide 7 ---

== DataFrames: Programmable Spreadsheets

The core idea: a *DataFrame* is a table — rows are observations, columns are variables — but every operation is a _function call_ rather than a mouse click.

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    *What you can do:*
    - Load data from CSV, Excel, Stata, SQL databases, APIs, and the web
    - Inspect your data: see the first few rows, summary statistics, missing values
    - Filter, sort, and subset with one line
    - Handles _millions_ of rows without crashing (try that in Excel)
  ],
  [
    ```python
    df = pd.read_csv("data/census.csv")

    # Summary statistics in one line
    df.describe()

    # Filter to just one state
    ca = df.query("state == 'California'")
    ```
  ],
)

// --- Slide 8 ---

== Cleaning Messy Data

Real-world data is _always_ messy — missing values, inconsistent formatting, duplicates, wrong types. Python gives you systematic tools to handle all of this reproducibly.

#v(0.5em)

- *Missing values* — detect, drop, or impute them programmatically
- *Duplicates* — identify and remove in one line
- *Type conversion* — turn strings into dates, fix numeric columns stored as text
- *Standardization* — clean up inconsistent names, capitalization, whitespace

#v(0.5em)

#align(center)[
  #text(fill: rgb("#6D1D44"), size: 20pt)[
    In most projects, _80% of the work_ is cleaning data. Python makes this reproducible rather than ad-hoc.
  ]
]

// --- Slide 9 ---

== Merging, Grouping & Reshaping

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === Merging Datasets
    Combine a household survey with census tract data by matching on FIPS codes — like Stata's `merge` or Excel's VLOOKUP, but for millions of rows.

    === Grouping & Aggregation
    "What is the average income by state and year?" becomes one line of code. Compute means, medians, standard deviations, or custom functions across any grouping.
  ],
  [
    === Reshaping
    Convert between *long* format (one row per observation-year) and *wide* format (one row per observation, years as columns) — essential for panel data.

    === Method Chaining
    String operations together in readable pipelines:
    ```python
    result = (df
        .query("year >= 2000")
        .groupby("region")["income"]
        .mean())
    ```
  ],
)

// --- Slide 10 ---

== Working with Text Data

Social scientists increasingly work with *unstructured text* — survey responses, legislative transcripts, historical documents, news articles, social media.

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    *What Python can do with text:*
    - Extract structured data (dates, dollar amounts, names) from free text
    - Search for keywords and patterns across thousands of documents
    - Clean and standardize messy text fields
    - Classify documents by topic or sentiment
  ],
  [
    ```python
    # Extract all 4-digit years
    df["year"] = df["text"].str.extract(
        r"(\d{4})"
    )

    # Flag documents about inflation
    df["about_inflation"] = (
        df["text"].str.contains(
            "inflation|CPI|prices"
        )
    )
    ```
  ],
)

// --- Slide 11 ---

== Panel Data

Panel data — repeated observations of the same units over time — is the backbone of empirical social science. Python handles it natively.

#v(0.5em)

- *Index by unit and time* — track households, firms, or countries across years
- *Within-group operations* — demean variables, compute lags, calculate growth rates, all by group
- *Reshape freely* — switch between long and wide formats for different analyses
- *Merge in time-varying covariates* — match external data by unit-year

#v(0.5em)

```python
# Create a lagged income variable for each household
df["lag_income"] = df.groupby("household_id")["income"].shift(1)

# Demean income within each household (for fixed effects intuition)
df["income_demean"] = df.groupby("household_id")["income"].transform("mean")
```

// ============================================================
// PART III: Visualization
// ============================================================

= Visualization

// --- Slide 12 ---

== Publication-Quality Plots

Python can produce *journal-ready figures* — scatter plots, line charts, histograms, bar charts, box plots, and more — with full control over every visual element.

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    - *Seaborn* generates beautiful statistical graphics in a single function call — regression lines with confidence bands, distribution plots, correlation heatmaps
    - *Matplotlib* gives fine-grained control when you need to customize every axis label, annotation, and color
    - Export directly to PDF, PNG, or SVG for LaTeX
  ],
  [
    ```python
    # Scatter plot with regression line
    # and 95% confidence band
    sns.lmplot(
        x="education", y="income",
        data=df, hue="gender", ci=95
    )
    plt.savefig("figure1.pdf", dpi=300)
    ```
    #text(size: 16pt, fill: gray)[
      One function call produces a publication-ready figure.
    ]
  ],
)

// --- Slide 13 ---

== Interactive Visualization

Static plots are great for papers, but *interactive charts* are powerful for exploration and presentations.

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    *With Plotly, you can:*
    - *Hover* over data points to see details (country name, exact value)
    - *Zoom* into regions of interest
    - *Animate* over time — watch trends unfold year by year
    - *Filter* by category interactively
    - Embed in Jupyter notebooks, websites, or presentations
  ],
  [
    === The "Hans Rosling" Plot
    ```python
    px.scatter(
        gapminder,
        x="gdpPercap", y="lifeExp",
        size="pop", color="continent",
        animation_frame="year",
        hover_name="country"
    )
    ```
    GDP vs. life expectancy for every country, animated from 1952 to 2007, with population as bubble size.
  ],
)

// --- Slide 14 ---

== Maps & Geospatial Analysis

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === Choropleth Maps
    Color states, counties, or countries by any variable — poverty rates, election margins, treatment intensity.

    - Load shapefiles (geographic boundaries)
    - Merge with your economic data by FIPS code or country name
    - Generate interactive maps: zoom, click, hover for details
    - No GIS software needed — everything in Python
  ],
  [
    === Satellite Imagery
    Access *Google Earth Engine* from Python to work with:
    - *Nighttime lights* — a proxy for economic activity where official GDP data is unreliable
    - *Vegetation indices* — measure agricultural productivity
    - *Urban expansion* — track development over decades
    - *Deforestation* — monitor environmental policy impacts

    All from a Jupyter notebook.
  ],
)

// ============================================================
// PART IV: Econometrics in Python
// ============================================================

= Econometrics in Python

// --- Slide 15 ---

== Regression Analysis

Python supports the full toolkit of regression analysis that social scientists rely on, with syntax that feels familiar if you know Stata or R.

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    *What's available:*
    - *OLS* with R-style formulas
    - Heteroskedasticity-robust standard errors (HC0--HC3)
    - Cluster-robust standard errors
    - Weighted least squares
    - Instrumental variables (2SLS)
    - Full regression tables with coefficients, SEs, $t$-stats, $R^2$
  ],
  [
    ```python
    import statsmodels.formula.api as smf

    # Familiar formula syntax
    model = smf.ols(
        "wage ~ education + experience",
        data=df
    ).fit(cov_type="HC3")

    model.summary()
    ```
    $ "wage"_i = beta_0 + beta_1 "educ"_i + beta_2 "exper"_i + u_i $
  ],
)

// --- Slide 16 ---

== Panel Data & Fixed Effects

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    Fixed effects models are the workhorse of applied microeconomics — control for all time-invariant unobserved heterogeneity.

    $ y_(i t) = beta x_(i t) + alpha_i + delta_t + epsilon_(i t) $

    - *Entity fixed effects* ($alpha_i$) — absorb unobserved unit characteristics
    - *Time fixed effects* ($delta_t$) — absorb common shocks
    - *Clustered SEs* — account for within-group correlation
  ],
  [
    Python's `pyfixest` is the equivalent of Stata's `reghdfe`:

    ```python
    import pyfixest as pf

    # Two-way fixed effects
    mod = pf.feols(
        "wage ~ education"
        " | worker + year",
        data=panel
    )
    mod.summary()
    ```

    Handles high-dimensional fixed effects efficiently — thousands of entities and time periods.
  ],
)

// --- Slide 17 ---

== Causal Inference: The Identification Problem

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    The central challenge of empirical social science: *correlation is not causation.*

    - Does education _cause_ higher wages, or do high-ability people both earn more and stay in school longer?
    - Does a policy _cause_ the outcome, or did treated units differ from control units all along?

    Python has mature tools for every major identification strategy.
  ],
  [
    === The Causal Toolkit
    #v(0.5em)
    #table(
      columns: (auto, auto),
      inset: 6pt,
      stroke: 0.5pt,
      [*Strategy*], [*Python Package*],
      [Fixed Effects], [`pyfixest`],
      [Difference-in-Differences], [`pyfixest`],
      [Instrumental Variables], [`linearmodels`],
      [Regression Discontinuity], [`rdrobust`],
      [Matching], [`causalml`],
      [Synthetic Control], [`SparseSC`],
    )
  ],
)

// --- Slide 18 ---

== Difference-in-Differences

*The idea:* compare the change in outcomes for a treated group to the change for a control group. The key assumption is that both groups would have followed *parallel trends* without treatment.

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    $ y_(i t) = beta_0 + beta_1 "Treat"_i + beta_2 "Post"_t + beta_3 ("Treat"_i times "Post"_t) + epsilon_(i t) $

    $beta_3$ is the *treatment effect* — the causal impact of the policy.

    *Applications:* minimum wage laws, healthcare expansions, environmental regulations, school funding changes.
  ],
  [
    *Modern advances* (available in Python):
    - *Event studies* — estimate dynamic effects before and after treatment
    - *Staggered adoption* — units adopt treatment at different times; new estimators (Callaway & Sant'Anna) avoid bias from "forbidden comparisons"
    - *Synthetic DiD* — combine matching with DiD
  ],
)

// --- Slide 19 ---

== Regression Discontinuity

*The idea:* when treatment is assigned by a cutoff in a running variable (test scores, vote margins, income thresholds), units _just above_ and _just below_ the cutoff are effectively randomized.

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    $ tau = lim_(x -> c^+) E[Y | X = x] - lim_(x -> c^-) E[Y | X = x] $

    *Applications:*
    - Class size effects (Maimonides' Rule)
    - Close elections and incumbency advantage
    - Eligibility cutoffs for social programs
    - GPA thresholds for academic probation
  ],
  [
    The `rdrobust` package handles everything:
    - *Data-driven bandwidth selection* — automatically chooses how close to the cutoff to focus
    - *Local polynomial estimation* — flexible functional form near the cutoff
    - *Robust confidence intervals*
    - *Built-in visualization* — see the discontinuity

    The exact same package used by researchers in Stata and R.
  ],
)

// --- Slide 20 ---

== Simulation & Bootstrap

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === Monte Carlo Simulation
    Generate data where you *know the truth*, then test whether your estimator recovers it.

    - Is my estimator unbiased?
    - How large a sample do I need to detect an effect? (*power analysis*)
    - What happens when my assumptions are violated?
    - Essential for evaluating _any_ new method
  ],
  [
    === Bootstrap Inference
    When analytical standard errors are unreliable:

    - *Few clusters* — wild bootstrap gives better inference than cluster-robust SEs
    - *Complex estimators* — bootstrap gives standard errors even when formulas don't exist
    - *Heteroskedasticity* — robust to distributional assumptions

    Python makes it trivial to run 10,000 bootstrap replications.
  ],
)

// --- Slide 21 ---

== Maximum Likelihood & Beyond

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === Maximum Likelihood Estimation
    Many models in social science — logit, probit, Tobit, selection models — are estimated via MLE.

    $ hat(theta)_("MLE") = arg max_theta sum_(i=1)^n log f(y_i | x_i, theta) $

    In Python, you can use *built-in models* (logit, probit) or *define your own likelihood function* and let the optimizer find the parameters.
  ],
  [
    === Generalized Method of Moments
    - Estimate models defined by *moment conditions* rather than a full likelihood
    - IV estimation as a special case
    - Overidentification tests

    #v(0.5em)
    Python gives you the building blocks to implement _any_ estimator — standard or custom — in a reproducible, testable way.
  ],
)

// ============================================================
// PART V: Machine Learning & AI
// ============================================================

= Machine Learning & AI

// --- Slide 22 ---

== What Machine Learning Offers Social Scientists

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === Prediction
    - Which students are at risk of dropping out?
    - What will unemployment be next quarter?
    - Where should we target inspections?

    #v(0.5em)
    ML excels at finding complex patterns in data, even when you don't know the functional form in advance.
  ],
  [
    === Strengthening Causal Inference
    - *Variable selection* — which controls matter among hundreds of candidates?
    - *Nuisance estimation* — flexibly estimate confounding without imposing parametric assumptions
    - *Heterogeneity* — who benefits most from a policy?

    #v(0.5em)
    ML is not a substitute for identification — it is a _tool that strengthens it._
  ],
)

// --- Slide 23 ---

== The ML Workflow

The key discipline of machine learning: *never evaluate a model on the data it was trained on.*

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    + *Split* the data into training and test sets
    + *Train* the model on the training set
    + *Evaluate* on the held-out test set
    + *Cross-validate* to tune hyperparameters

    This prevents *overfitting* — the model learning noise rather than signal.
  ],
  [
    ```python
    from sklearn.model_selection import (
        train_test_split
    )
    from sklearn.linear_model import LassoCV

    X_train, X_test, y_train, y_test = (
        train_test_split(X, y)
    )

    # LASSO: automatic variable selection
    model = LassoCV(cv=5).fit(
        X_train, y_train
    )
    ```
  ],
)

// --- Slide 24 ---

== Causal Machine Learning: Double ML

*The problem:* you want the causal effect of $D$ on $Y$, but you have hundreds of potential confounders $X$. Which controls should you include?

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    *Double ML* (Chernozhukov et al., 2018):
    + Use ML to predict $Y$ from $X$ (flexibly)
    + Use ML to predict $D$ from $X$ (flexibly)
    + Regress the _residuals_ of $Y$ on the _residuals_ of $D$
    + The coefficient is the *causal effect* of $D$

    No need to choose a parametric specification for the confounders. ML handles the "nuisance" so you can focus on the causal question.
  ],
  [
    ```python
    from doubleml import (
        DoubleMLData, DoubleMLPLR
    )

    dml = DoubleMLPLR(
        data,
        ml_l=LassoCV(),  # predict Y
        ml_m=LassoCV(),  # predict D
        n_folds=5
    )
    dml.fit()
    print(dml.summary)
    ```
  ],
)

// --- Slide 25 ---

== Who Benefits? Heterogeneous Treatment Effects

A policy might help some people and hurt others. Traditional methods estimate *one average effect*. Causal forests let you ask: *for whom is the effect largest?*

#v(0.5em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    *Causal Forests* (Athey & Wager, 2019):
    - Estimate a _personalized_ treatment effect $tau(x)$ for each individual based on their characteristics
    - Data-driven — the algorithm discovers which subgroups matter
    - *SHAP values* explain _why_ the model predicts larger effects for certain groups
  ],
  [
    *Applications:*
    - Which patients benefit most from a drug?
    - Which job seekers benefit most from a training program?
    - Where should a government target a subsidy?
    - How should an NGO allocate limited resources?

    These questions were very hard to answer before causal ML.
  ],
)

// --- Slide 26 ---

== Text as Data

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    Text is everywhere in social science — but it used to be nearly impossible to analyze at scale. Python changes that.

    *Applications:*
    - Measure *political polarization* from congressional speeches
    - Classify *sentiment* in consumer reviews or earnings calls
    - Extract *policy positions* from party manifestos
    - Analyze *media framing* of events across outlets
  ],
  [
    *Tools available:*
    - *Pattern matching* — find dates, dollar amounts, names in documents
    - *Keyword classification* — flag documents by topic
    - *Sentiment analysis* — positive vs. negative language
    - *Large Language Models* — use GPT-4 or Claude to classify, summarize, or extract information from text at scale, via Python API calls
  ],
)

// --- Slide 27 ---

== Computer Vision & Historical Data

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === Digitizing the Past
    Many historical sources exist only as scanned images — census forms, newspaper advertisements, handwritten ledgers, maps.

    Python can:
    - *OCR* — extract text from scanned documents
    - *Segment images* — identify tables, figures, handwriting
    - *Classify* — sort documents by type automatically
    - Build datasets that would take _years_ to create manually
  ],
  [
    === Satellite & Aerial Imagery
    - Measure *land use change* over decades
    - Detect *informal settlements* in developing countries
    - Track *infrastructure development* (roads, buildings)
    - Classify *crop types* for agricultural economics
    - All using image classification models trained in Python

    #v(0.5em)
    Economists are increasingly using images as data — and Python is the primary tool for this work.
  ],
)

// --- Slide 28 ---

== Deep Learning: When and Why

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    === When Deep Learning

    - *Unstructured data* — images, audio, text
    - *Very large datasets* — hundreds of thousands of observations
    - *Prediction* is the primary goal
    - Feature engineering would be prohibitively complex

    #v(0.5em)
    Python (via *PyTorch*) is the dominant language for deep learning — the same tool used by OpenAI, Google DeepMind, and Meta AI.
  ],
  [
    === When Econometrics

    - *Causal questions* require identification strategies, not just pattern recognition
    - *Small/medium datasets* — where overfitting is a real concern
    - *Interpretability* is essential for policy implications
    - *Theory* guides the model specification

    #v(0.5em)
    The two approaches are _complements_, not substitutes. The best empirical work increasingly uses both.
  ],
)


// ============================================================
// PART VII: Interoperability
// ============================================================

= Interoperability

// --- Slide 32 ---

== You Don't Have to Abandon Stata

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    If you have years of Stata code, you don't need to rewrite it. *pystata* lets you run Stata commands _from within_ a Python notebook.

    *Use cases:*
    - Keep your existing `.do` files and call them from Python
    - Use Stata for estimation, Python for data wrangling and visualization
    - Transfer data seamlessly between the two environments
    - Gradually learn Python without giving up your current workflow
  ],
  [
    ```python
    from pystata import stata

    # Run Stata commands directly
    stata.run("sysuse auto, clear")
    stata.run("reg price mpg weight")

    # Send your Python data to Stata
    stata.pdataframe_to_data(df)

    # Get Stata results back in Python
    df = stata.pdataframe_from_data()

    # Run an existing .do file
    stata.run("do my_analysis.do")
    ```
  ],
)

// --- Slide 33 ---

== You Don't Have to Abandon R Either

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    R has excellent packages for certain tasks — `ggplot2` for visualization, `sf` for spatial data, Bayesian methods with `Stan`. With *rpy2*, you can use them all from Python.

    *Use cases:*
    - Access the *tidyverse* when it fits your workflow
    - Use specialized R packages that have no Python equivalent
    - Run R code in the _same notebook_ as your Python analysis
    - Share data between R and Python seamlessly
  ],
  [
    ```python
    import rpy2.robjects as ro
    from rpy2.robjects import pandas2ri
    pandas2ri.activate()

    # Pass your DataFrame to R
    ro.globalenv["df"] = df

    # Use R packages
    ro.r("""
    library(ggplot2)
    ggplot(df, aes(x=income, y=health))
      + geom_point()
      + geom_smooth(method="lm")
    """)
    ```
  ],
)

// --- Slide 34 ---

== Conclusion

#v(1em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  [
    + *Python is a complement*, not a replacement — use it alongside Stata and R

    + *Reproducibility* comes from scripted, version-controlled workflows

    + *Data wrangling* at scale — clean, merge, reshape millions of rows

    + *Visualization* from static journal figures to interactive animated maps
  ],
  [
    5. *Econometrics* in Python is mature — OLS, fixed effects, DiD, RDD, MLE

    6. *Machine learning* strengthens causal inference — Double ML, causal forests

    7. *New frontiers* — text as data, satellite imagery, LLMs, computer vision

    8. *Interoperability* — call Stata and R from within Python
  ],
)

#v(1em)

#align(center)[
  #text(fill: rgb("#6D1D44"), weight: "bold", size: 22pt)[
    Python is not about replacing your toolkit — it is about expanding it.
  ]
]
