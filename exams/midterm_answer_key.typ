#set page(
  paper: "us-letter",
  margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
  numbering: "1",
)
#set text(size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: none)
#show raw: set text(size: 10pt)

#align(center)[
  #v(1em)
  #text(size: 18pt, weight: "bold")[EC34: Data Science for Economists]
  #v(0.4em)
  #text(size: 14pt, weight: "bold")[Midterm Examination --- Spring 2026]
  #v(0.3em)
  #text(size: 12pt, weight: "bold", fill: rgb("#B22222"))[ANSWER KEY --- NOT FOR DISTRIBUTION]
  #v(0.3em)
  #text(size: 11pt)[March 4, 2026 #h(2em) Swarthmore College]
]

#v(1.5em)
#line(length: 100%)
#v(1em)

= Part I: True / False --- Answers

#let ans(n, verdict, body) = block(width: 100%, inset: (left: 0.5em))[
  #grid(
    columns: (2em, auto, 1fr),
    gutter: 0.5em,
    [*#n.*],
    [#text(weight: "bold", fill: if verdict == "T" { rgb("#1a7a1a") } else { rgb("#B22222") })[#verdict]],
    body,
  )
  #v(0.5em)
]

#ans(1, "T")[Lists are mutable (elements can be changed); tuples are immutable.]
#ans(2, "F")[`np.linalg.inv()` requires a *square* matrix. Calling it on a non-square matrix raises `LinAlgError`.]
#ans(3, "F")[The `@` operator performs *matrix multiplication* (dot product), not element-wise multiplication. Element-wise multiplication uses the `*` operator.]
#ans(4, "F")[Seaborn works best with *tidy (long-format)* data --- one row per observation per variable.]
#ans(5, "F")[`.groupby()` does *not* modify the original DataFrame. It creates a temporary `GroupBy` object; the original `df` is unchanged until you explicitly assign the result.]
#ans(6, "F")[`BeautifulSoup` only parses static HTML. *Selenium* is needed to execute JavaScript and retrieve dynamically rendered content.]
#ans(7, "T")[A pure function is side-effect-free and deterministic: same inputs always produce same outputs, with no external mutation.]
#ans(8, "T")[Broadcasting rules: dimensions are compared right-to-left. `(3,1)` and `(1,4)` are compatible; each 1-dimension expands, giving `(3,4)`.]
#ans(9, "F")[Lambda functions *can* be assigned to variables: `square = lambda x: x**2` is valid Python.]
#ans(10, "F")[`robots.txt` is a convention, not law. U.S. courts (e.g., _hiQ Labs v. LinkedIn_, 2022) have held that scraping publicly accessible data is generally not illegal, though it may violate a site's Terms of Service.]

#pagebreak()

= Part II: Long Answer --- Answers

== Question 1: Python Fundamentals

*(a) [4 pts]*

The code iterates over `data`, appending `x**2` only when `x` is even (divisible by 2). Even elements are 2 and 4.

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
[4, 16]
```
]

_Grading:_ Full credit for exact output. Deduct 2 pts if student includes odd numbers or squares them incorrectly.

#v(0.5em)

*(b) [4 pts]*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
result = [x ** 2 for x in data if x % 2 == 0]
```
]

_Grading:_ Full credit. Accept any valid equivalent form. Deduct 2 pts if the filter condition is missing or wrong.

#v(0.5em)

*(c) [6 pts]*

*i.* (2 pts) Both `my_list` and `new_list` point to the same list object. Output:

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```
[1, 2, 3, 4]
[1, 2, 3, 4]
```
]

*ii.* (4 pts) Yes, `add_element` has a side effect. A *side effect* is when a function modifies state that exists outside its own local scope. Here, `lst.append(x)` mutates the list in place, which also modifies `my_list` in the caller's scope --- even though the function did not explicitly receive permission to do so. Both variables then point to the same mutated object.

_Grading:_ 2 pts for correct output, 4 pts for explanation. A complete answer defines side effects and correctly identifies the mutation of `my_list`.

#v(0.5em)

*(d) [6 pts]*

Step-by-step:
- `filter(lambda x: x % 2 == 0, numbers)` keeps only even numbers: `[2, 4, 6]`
- `map(lambda x: x ** 2, evens)` squares each: `[4, 16, 36]`

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```
[4, 16, 36]
```
]

_Grading:_ 2 pts for correctly identifying the evens `[2, 4, 6]`, 2 pts for squaring them, 2 pts for exact output format (list brackets, correct values).

#pagebreak()

== Question 2: Pandas

*(a) [4 pts]*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
df["gdp_per_cap"] = df["gdp"] / df["population"]
# or equivalently:
df = df.assign(gdp_per_cap=df["gdp"] / df["population"])
```
]

*(b) [5 pts]*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
df.groupby("country")["gdp"].mean()
```
]

Result: a Series with index `["Canada", "Mexico", "USA"]` and mean GDP values.

_Grading:_ 3 pts for correct `groupby` + `mean`, 2 pts for selecting the right column.

*(c) [4 pts]*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
df[df["gdp_per_cap"] > 40]
# or equivalently:
df.query("gdp_per_cap > 40")
```
]

Only USA rows pass (gdp_per_cap ≈ 63--69). Canada is ~45--47, which also passes. Mexico is ~8--9.

*(d) [7 pts]*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
df.pivot(index="country", columns="year", values="gdp")
```
]

The resulting DataFrame has `country` as the row index and column headers `[2020, 2021]` (the unique values of the `year` column).

_Grading:_ 5 pts for correct `.pivot()` call, 2 pts for correctly describing the resulting column headers.

#pagebreak()

== Question 3: Visualization

*(a) [7 pts]*

*Wide format* has one row per entity and multiple columns for each variable--time combination:

#align(center)[
  #table(
    columns: (auto, auto, auto),
    inset: 7pt,
    stroke: 0.5pt,
    align: center,
    table.header([*country*], [*gdp_2020*], [*gdp_2021*]),
    [USA], [21000], [23000],
    [Mexico], [1100], [1200],
  )
]

*Tidy (long) format* has one row per observation (one country--year pair):

#align(center)[
  #table(
    columns: (auto, auto, auto),
    inset: 7pt,
    stroke: 0.5pt,
    align: center,
    table.header([*country*], [*year*], [*gdp*]),
    [USA], [2020], [21000],
    [USA], [2021], [23000],
    [Mexico], [2020], [1100],
  )
]

Seaborn (and plotly) prefer tidy data because they map single column names to visual properties (`x=`, `y=`, `hue=`). Wide data would require manually unpacking multiple columns.

_Grading:_ 3 pts for correct sketch/description of each format, 1 pt for explaining seaborn's preference.

*(b) [6 pts]*

*Bug:* `color="education_level"` should be `hue="education_level"`. The `color` parameter in seaborn expects a single color string (like `"red"` or `"#3498db"`), not a column name. To color points by a categorical variable, use `hue=`.

*Corrected line:*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
sns.scatterplot(data=df, x="age", y="income", hue="education_level", ax=ax)
```
]

_Grading:_ 3 pts for identifying the bug, 3 pts for the correct fix.

*(c) [7 pts]*

Use `ipywidgets`. Import `interact` from `ipywidgets`, define a function that takes `year` as a parameter, filters the DataFrame inside the function, and creates/displays the plot. Decorate the function with `@interact(year=list_of_years)`. Jupyter will automatically render a slider; when the user moves it, the function is called with the new value and the plot updates.

_Grading:_ 2 pts for naming `ipywidgets`, 5 pts for a coherent description of the workflow (function takes parameter, filters data, plots, decorated with `@interact`).

#pagebreak()

== Question 4: Text Analysis

*(a) [6 pts]* What is the utility of using regular expressions for text analysis? Give an example of a task that would be difficult to accomplish without regexes, and briefly describe how a regex could help.

Regular expressions allow you to search for complex patterns in text, beyond simple substring matching. They can match variable-length patterns, optional elements, and character classes. For example, extracting all email addresses from a document would be difficult without regexes. A regex like `r"[\w.]+@[\w.]+"` can match the general structure of an email address  regardless of the specific characters used, making it easy to find all emails in a large text.


*(b) [5 pts]*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
['support@example.com', 'sales@company.org']
```
]

`[\w.]+` matches one or more word characters or dots; `@` matches a literal `@`; `[\w.]+` matches the domain. `re.findall()` returns a list of all non-overlapping matches.

_Grading:_ Full credit for exact output including the list format and both strings. Deduct 2 pts for minor formatting errors.

*(c) [9 pts]*

*i.* (3 pts) The `domain` column contains:

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```
gmail.com
yahoo.com
school.edu
```
]

*ii.* (4 pts) The parentheses define a *capture group*. `.str.extract()` returns *only* the content matched inside the capture group(s), not the full pattern match. Here, the `@` symbol is matched but not captured, so the returned values contain only the domain portion after `@`.

*iii.* (2 pts) Without parentheses, `.str.extract()` would raise a `ValueError: pattern contains no capture groups`. The function requires at least one capture group to know what to return.

_Grading:_ 3 pts for part i, 4 pts for part ii (must mention capture group concept), 2 pts for part iii.

#pagebreak()

== Question 5: Web Scraping

*(a) [9 pts]* (3 pts per scenario)

*i.* *REST API.* A public JSON API is available, so it should be used directly --- it is faster, more reliable, returns structured data, and avoids the overhead and fragility of HTML parsing.

*ii.* *Selenium.* The content is rendered by JavaScript after page load; `requests` only downloads the initial HTML (which is nearly empty). Selenium controls a real browser that executes JavaScript and gives access to the fully rendered page.

*iii.* *`requests` + `BeautifulSoup`.* The page is static HTML with no JavaScript involved. `requests` fetches the HTML and BeautifulSoup parses it to find all `<a>` tags and extract their `href` attributes.

*(b) [6 pts]*

*Bug:* `BeautifulSoup(response, "html.parser")` passes a `Response` object instead of an HTML string. `requests.get()` returns a `Response` object; you must call `.text` (or `.content`) to get the HTML.

*Corrected line:*

#block(fill: luma(230), inset: 8pt, radius: 4pt)[
```python
soup = BeautifulSoup(response.text, "html.parser")
```
]

_Grading:_ 3 pts for identifying the bug (passing `response` instead of `response.text`), 3 pts for the correct fix.

*(c) [5 pts]*

*Problem:* Sending 500 rapid requests can overload the server, cause it to throttle or ban your IP address, violate the site's Terms of Service, and is generally considered poor digital citizenship.

*Strategy 1:* Use `time.sleep(seconds)` inside the loop to pause between requests, giving the server time to recover (e.g., 1--2 seconds per request).

*Strategy 2:* Use the `backoff` library with `@backoff.on_exception()` to implement *exponential backoff* --- automatically retrying failed requests with increasing delays, which prevents hammering the server after an error.

Other acceptable answers: checking `robots.txt` first, limiting concurrent connections, scraping during off-peak hours.

_Grading:_ 2 pts for the problem explanation, 1.5 pts per strategy (must be specific, not just "be nice").
