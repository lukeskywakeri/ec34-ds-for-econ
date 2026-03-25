#set page(
  paper: "us-letter",
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
  numbering: "1",
)
#set text(size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: none)
#show raw: set text(size: 10pt)

// ─── Cover page ───────────────────────────────────────────────────────────────

#align(center)[
  #v(1em)
  #text(size: 18pt, weight: "bold")[EC34: Data Science for Economists]
  #v(0.4em)
  #text(size: 14pt, weight: "bold")[Midterm Examination --- Spring 2026]
  #v(0.3em)
  #text(size: 11pt)[March 4, 2026 #h(2em) Swarthmore College]
]

#v(1.5em)

#v(0.8em)

#grid(
  columns: (auto, 8cm, 2em, auto, 5cm),
  align: bottom,
  gutter: 0pt,
  [*Name:*], [#line(length: 100%)], 
)

#v(0.8em)
#v(1em)

*Instructions:*

- This exam has *two parts*. Everyone completes Part I (True/False). In Part II, answer *4 of the 5* questions. Clearly cross out the number of the question you are skipping.
- The exam is worth *100 points* and you have *60 minutes*.
- Write your answers in the space provided. If you need more space, use the back of the page and note clearly where your answer continues.
- You do *not* need to memorize exact Python syntax. If you cannot recall a function name, describe in plain English what it does.
- No notes, phones, or computers. A non-programmable calculator is permitted.

#v(1em)

#table(
  columns: (1fr, auto, auto),
  inset: 8pt,
  align: (left, center, center),
  stroke: 0.5pt,
  table.header([*Section*], [*Possible*], [*Earned*]),
  [Part I: True/False (10 questions)], [20], [],
  [Part II, Q1: Python Fundamentals], [20], [],
  [Part II, Q2: Pandas], [20], [],
  [Part II, Q3: Visualization], [20], [],
  [Part II, Q4: Text Analysis], [20], [],
  [Part II, Q5: Web Scraping], [20], [],
  [*TOTAL* (Part I + best 4 of Part II)], [*100*], [],
)

#pagebreak()

// ─── Part I: True / False ─────────────────────────────────────────────────────

= Part I: True / False (20 points)

*Circle T or F for each statement. Each question is worth 2 points.*

#v(0.8em)

*1.* In Python, lists are mutable --- their elements can be changed after creation --- while tuples are immutable.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*2.* The function `np.linalg.inv(A)` will succeed for any NumPy array `A`, regardless of its shape.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*3.* The `@` operator in NumPy performs element-wise multiplication of two arrays (i.e., multiplying each pair of corresponding elements).

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*4.* Seaborn's statistical plots (e.g., `sns.barplot()`, `sns.boxplot()`) work best with data in "wide" format, where each variable has its own column.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*5.* The pandas `.groupby()` method permanently modifies the original DataFrame.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*6.* `BeautifulSoup` can execute JavaScript and return dynamically rendered web content.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*7.* A "pure function" is one that has no side effects: it does not modify any state outside its own scope and always returns the same output given the same inputs.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*8.* A NumPy array of shape `(3, 1)` can be matrix multiplied with an array of shape `(1, 4)` to produce a result of shape `(3, 4)`.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*9.* In Python, a `lambda` function cannot be assigned to a variable.

#h(1.5em) *T* #h(2em) *F*

#v(0.9em)

*10.* Checking a website's `robots.txt` file before scraping is a legal requirement under U.S. law.

#h(1.5em) *T* #h(2em) *F*

#pagebreak()

// ─── Part II ──────────────────────────────────────────────────────────────────

= Part II: Long Answer (80 points)

*Answer *4 of the 5* questions below. Each is worth 20 points. Clearly cross out the question you are skipping.*

#pagebreak()

// ─── Q1 ───────────────────────────────────────────────────────────────────────

#grid(columns: (1fr, auto), align: top,
  [== Question 1: Python Fundamentals], [*(20 points)*])

#v(0.5em)

*(a) [4 pts]* What does the following code print? Write the *exact* output.

```python
data = [1, 2, 3, 4, 5]
result = []
for x in data:
    if x % 2 == 0:
        result.append(x ** 2)
print(result)
```

*Answer:*

#v(3em)

#v(0.8em)

*(b) [4 pts]* Rewrite the loop above as a *single list comprehension* that produces the same `result`.

*Answer:*

#v(3em)

#pagebreak()

*(c) [6 pts]* Consider the following code:

```python
def add_element(lst, x):
    lst.append(x)
    return lst

my_list = [1, 2, 3]
new_list = add_element(my_list, 4)
print(my_list)
print(new_list)
```

*i.* What does this code print?

*Answer:*

#v(3em)

*ii.* Does `add_element` have a *side effect*? Explain what a side effect is and whether this function exhibits one.

*Answer:*

#v(6em)

#v(0.8em)

*(d) [6 pts]* What does the following code print? Write the *exact* output.

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
squared = list(map(lambda x: x ** 2, evens))
print(squared)
```

*Answer:*

#v(3em)

#pagebreak()

// ─── Q2 ───────────────────────────────────────────────────────────────────────

#grid(columns: (1fr, auto), align: top,
  [== Question 2: Pandas], [*(20 points)*])

#v(0.5em)

You are given the following DataFrame `df`:

#align(center)[
  #table(
    columns: (auto, auto, auto, auto),
    inset: 8pt,
    stroke: 0.5pt,
    align: center,
    table.header([*country*], [*year*], [*gdp* ], [*population* ]),
    [USA],    [2020], [21000], [330],
    [USA],    [2021], [23000], [332],
    [Mexico], [2020], [1100],  [128],
    [Mexico], [2021], [1200],  [129],
    [Canada], [2020], [1700],  [38],
    [Canada], [2021], [1800],  [38],
  )
]

*(a) [4 pts]* Write code to create a new column `gdp_per_cap` equal to `gdp / population`.

*Answer:*

#v(3.5em)

*(b) [5 pts]* Write code to compute the *average GDP* for each country across both years. The result should have `country` as the index.

*Answer:*

#v(3.5em)

*(c) [4 pts]* Using `gdp_per_cap` from part (a), write code to keep only the rows where `gdp_per_cap > 40`.

*Answer:*

#v(3.5em)

*(d) [7 pts]* Write code to *reshape* `df` so that each country is one row, the years become column headers, and the cell values are `gdp`.

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
  *Hint:* Use `.pivot()` --- see the Function Reference at the end of this exam.
]

*Answer:*

#v(10em)

What do the columns of the resulting DataFrame look like?

*Answer:*

#v(3em)

#pagebreak()

// ─── Q3 ───────────────────────────────────────────────────────────────────────

#grid(columns: (1fr, auto), align: top,
  [== Question 3: Visualization], [*(20 points)*])

#v(0.5em)

*(a) [7 pts]* Explain the difference between *tidy (long-format)* data and *wide-format* data. In the space below, sketch a small example of each format using the same underlying data, then explain why seaborn prefers tidy data.

#v(12em)

*(b) [6 pts]* The following code is meant to produce a scatter plot of `age` vs. `income` with points colored by `education_level`. It contains a bug. Identify the bug and write the corrected line.

```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
sns.scatterplot(data=df, x="age", y="income", color="education_level", ax=ax)
ax.set_title("Income by Age")
plt.show()
```

*What is the bug?*

#v(4em)

*Write the corrected line:*

#v(3em)

*(c) [7 pts]* You want to add a *slider* to a Jupyter notebook that lets a user pick a year, and the plot updates automatically to show only that year's data. Which Python library or tool would you use? Describe in 2--4 sentences how you would set it up. (You do not need to write complete code.)

#v(7em)

#pagebreak()

// ─── Q4 ───────────────────────────────────────────────────────────────────────

#grid(columns: (1fr, auto), align: top,
  [== Question 4: Text Analysis], [*(20 points)*])

#v(0.5em)

*(a) [6 pts]* What is the utility of using regular expressions for text analysis? Give an example of a task that would be difficult to accomplish without regexes, and briefly describe how a regex could help.

#v(15em)

*(b) [5 pts]* What does the following code print? Write the exact output.

```python
import re

text = "Contact us at support@example.com or sales@company.org"
pattern = r"([\w.]+@[\w.]+)"
matches = re.findall(pattern, text)
print(matches)
```

*Answer:*

#v(3.5em)

*(c) [9 pts]* Consider the following code:

```python
import pandas as pd

df = pd.DataFrame({
    "email": ["alice@gmail.com", "bob@yahoo.com", "carol@school.edu"]
})
df["domain"] = df["email"].str.extract(r"@([\w.]+)")
print(df)
```

*i.* What values does the `domain` column contain after this code runs?

*Answer:*

#v(7em)

*ii.* What do the parentheses `(...)` in the pattern `r"@([\w.]+)"` do? Why are they necessary for `.str.extract()`?

*Answer:*

#v(15em)

*iii.* What would happen if you removed the parentheses and used the pattern `r"@[\w.]+"` instead?

*Answer:*

#v(3.5em)

#pagebreak()

// ─── Q5 ───────────────────────────────────────────────────────────────────────

#grid(columns: (1fr, auto), align: top,
  [== Question 5: Web Scraping], [*(20 points)*])

#v(0.5em)

*(a) [9 pts]* For each scenario, choose the *best tool* from the options below and give a *one-sentence justification*. Options: `requests` + `BeautifulSoup` | `Selenium` | REST API

#v(0.3em)

*i.* The U.S. Bureau of Labor Statistics publishes monthly unemployment data via a public JSON endpoint.

*Tool:* #h(4cm) *Reason:*

#v(3em)

*ii.* A news website renders all of its headlines using JavaScript after the page loads; the raw HTML source returned by `requests` is nearly empty.

*Tool:* #h(4cm) *Reason:*

#v(3em)

*iii.* You want to extract every hyperlink (`href`) from a plain, static HTML government report.

*Tool:* #h(4cm) *Reason:*

#v(3em)

*(b) [6 pts]* The following code tries to scrape quotes from a website but contains a bug. Identify the bug and write the corrected line.

```python
from bs4 import BeautifulSoup
import requests

response = requests.get("http://quotes.toscrape.com")
soup = BeautifulSoup(response, "html.parser")

quotes = soup.find_all("span", {"class": "text"})
for q in quotes:
    print(q.text)
```

*What is the bug?*

#v(4em)

*Write the corrected line:*

#v(8em)

*(c) [5 pts]* You are writing a scraper that will send requests to 500 pages in a loop, as fast as possible. Why is this a problem? Name a strategy to scrape more responsibly.

*Why it is a problem:*

#v(3.5em)

*Your strategy:*


#pagebreak()

// ─── Function Reference ───────────────────────────────────────────────────────

= Function Reference

_This page may be detached and kept out during the exam._

#v(0.5em)
#line(length: 100%)
#v(0.8em)

== Python Built-ins

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  align: (left, left),
  [`x % y`], [Remainder after dividing `x` by `y`. E.g., `7 % 2` → `1`.],
  [`list.append(x)`], [Adds element `x` to the end of `list` in-place. Returns `None`.],
  [`filter(func, iterable)`], [Returns an iterator over items from `iterable` for which `func(item)` is `True`.],
  [`map(func, iterable)`], [Applies `func` to every item in `iterable`; returns an iterator of the results.],
  [`list(iterable)`], [Converts any iterable (e.g., the result of `map` or `filter`) to a list.],
)

#v(0.8em)

== NumPy (`import numpy as np`)

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  align: (left, left),
  [`A @ B`], [Matrix multiplication (dot product) of arrays `A` and `B`. Not element-wise.],
  [`A * B`], [Element-wise multiplication of `A` and `B`.],
  [`np.linalg.inv(A)`], [Returns the inverse of square matrix `A`. Raises `LinAlgError` if `A` is not square.],
)

#v(0.8em)

== Pandas (`import pandas as pd`)

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  align: (left, left),
  [`df.query("condition")`], [Returns a new DataFrame containing only rows where `condition` is `True`. ],
  [`df.groupby(col)`], [Groups `df` by unique values in `col`. Chain with an aggregation.],
  [`.mean()`], [Computes the arithmetic mean of each group after a `.groupby()`.],
  [`df.pivot(index, columns, values)`], [Reshapes `df` from long to wide: `index` → row labels, `columns` → column names, `values` → cell values.],
  [`Series.str.extract(pattern)`], [Applies regex `pattern` to each element; returns a DataFrame with one column per capture group `(...)`. *Requires at least one capture group.*],
)

#v(0.8em)

== Seaborn / Matplotlib

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  align: (left, left),
  [`sns.scatterplot(...)`], [Scatter plot. `hue="col"` colors points by a column's values. `color="red"` sets a single fixed color for all points.],
  [`plt.subplots()`], [Returns a `(fig, ax)` tuple. `ax` is the axes object on which you draw.],
)

#v(0.8em)

== ipywidgets

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  align: (left, left),
  [`@interact(param=values)`], [Decorator that creates an interactive widget (slider, dropdown) in Jupyter. Calls the decorated function with the new value of `param` whenever the widget changes.],
)

#v(0.8em)

== Regular Expressions (`import re`)

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  align: (left, left),
  [`re.findall(pattern, string)`], [Returns a list of all non-overlapping matches of `pattern` in `string`.],
  [`\w`], [Matches any word character: letters, digits, and underscore `_`.],
  [`\d`], [Matches any digit: `0`--`9`.],
  [`[\w.]`], [Character class matching a word character *or* a literal dot.],
  [`.` ], [Matches any single character except a newline.],
  [`*` / `+`], [Greedy: match 0+ / 1+ times, as *many* as possible.],
  [`*?` / `+?`], [Lazy: match 0+ / 1+ times, as *few* as possible.],
  [`(...)`], [Capture group: the matched text inside is returned by `findall` and `str.extract`.],
)

#v(0.8em)

== Web Scraping

#table(
  columns: (auto, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  align: (left, left),
  [`requests.get(url)`], [Sends an HTTP GET request to `url`. Returns a `Response` object (A response code in the 100s, 200s, 400s, 500s). Access the HTML via `.text`.],
  [`BeautifulSoup(html, parser)`], [Parses `html` (a string) into a navigable tree. Use `"html.parser"` for the built-in parser.],
  [`soup.find_all(tag, attrs)`], [Returns a list of all elements matching `tag` and optional attribute dict `attrs`. E.g., `attrs=` `{"class": "quote"}` selects elements with that CSS class.],
)
