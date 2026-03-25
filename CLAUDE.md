# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

University course repository for **EC34: Data Science for Economists** (Spring 2026, Swarthmore College). Contains Jupyter notebook lectures, assignments, exams, interactive Streamlit games, and Quarto presentations covering Python-based data science and econometrics.

## Commands

```bash
uv sync                                    # Install all dependencies
uv add <package>                           # Add a new dependency
uv run streamlit run games/crisis/app.py   # Run a Streamlit game
quarto render lectures/<topic>/file.qmd    # Render Quarto slides/docs
```

Python version: 3.10 (specified in `.python-version`). No formal test suite or linter is configured.

## Architecture

- **`lectures/`**: Each subfolder is a topic (e.g., `pandas/`, `causal-machine-learning/`). Contains `.ipynb` notebooks, optional `data/` subfolders, and some `.qmd` Quarto presentations. Notebooks must maintain sequential cell execution order and mix Markdown explanations with code.
- **`assignments/`** and **`exams/`**: Jupyter notebooks for student work. Submitted as reproducible `.zip` packages.
- **`games/`**: Interactive Streamlit apps for teaching. Structure: `app.py` (UI) + `data.py` (logic/data generation). Use `st.session_state` for persistence.
- **`problem-sets/`**: Markdown problem descriptions with optional `assets/`.

## Code Conventions

- **Paths**: ALWAYS use relative paths (e.g., `pd.read_csv("data/file.csv")`), never absolute.
- **Standard aliases**:
  ```python
  import pandas as pd
  import numpy as np
  import statsmodels.formula.api as smf
  import matplotlib.pyplot as plt
  import seaborn as sns
  ```
- **Econometrics**: Prefer `pyfixest` for high-dimensional fixed effects, `statsmodels` for standard reporting.
- **Visualization**: Static (`matplotlib`, `seaborn`), interactive (`plotly`), maps (`geopandas`, `folium`, `geemap`).
- **Reproducibility is the highest priority** for all code in this repo.


## Exam Writing

When writing exams for this class, ask: 

1. What is the last topic covered before the midterm?

After this, check the syllabus to check every topic covered before the midterm.

The exam should be completed in one hour and can include question types:

1. True/False questions
2. Multiple-part questions around a table of data 
3. Short answer questions (e.g. "What is the difference between a confounder and a collider?")
4. More conceptual questions
5. Giving code that will end in an error and asking to explain the error and how to fix it.
6. Giving code that will run and asking to explain the output.


### Structure

The structure of the exam should be:

1. A cover page with instructions and an honor code statement
2. A set of T/F questions that should be completed by everyone. These questions should be relatively easy and test basic understanding of the material. They should be worth a small portion of the exam grade (e.g. 20%).
2. 5 questions that test deeper understanding of the material. These questions should be more difficult and require students to apply their knowledge to new situations. They should be worth a larger portion of the exam grade (e.g. 80%).
3. The instructions should state that students only need to answer 4 out of the 5 questions in part 2.
4. The exam should be designed to be completed in one hour, so the questions should be appropriately difficult and not too time-consuming.
5. Do not assume that students have memorized specific code syntax or functions. Instead, focus on testing their understanding of concepts and their ability to apply them. If a special function is needed to answer a question, provide the function definition in the question itself.

### Workflow

1. Write the exam in a `.typ` file in the `exams/` directory. 
2. Once the exam is written, render it to PDF with `typst` and save the PDF in the same directory.
3. Write an answer key for the exam in a separate `.typ` file and render it to PDF as well.

Once the exam is completed, put yourself in the shoes of a student taking the exam. Try to answer the questions without looking at your notes or the textbook. If you find that some questions are too difficult or too easy, adjust them accordingly. If you find that some questions are ambiguous or unclear, rewrite them to be more clear.

