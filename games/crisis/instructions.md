
# 📂 MISSION DOSSIER: PROTOCOL DECIMATION

**TO:** All Junior Data Officers

**FROM:** Central Bank Oversight Committee

**PRIORITY:** **CRITICAL // IMMEDIATE ACTION REQUIRED**

**SUBJECT:** SYSTEM FAILURE IMMINENT

---

### 1. THE SITUATION

A catastrophic data corruption event has hit the Global Trade Network. The Central Bank's "Market Health" dashboard (visible on the main screen) is decaying by **2% every minute**.

If System Integrity reaches **0%**, the global economy collapses.

The corruption has isolated **10 Regional Districts**. Each district's transaction logs are flawed in a unique way. We cannot stabilize the market until all 10 districts are cleaned and verified.

### 2. YOUR OBJECTIVE

You have been assigned to a specific **Regional District**. Your team must:

1. **ACQUIRE:** Download your specific CSV file (e.g., `district_4.csv`).
2. **CLEAN:** Use Python/Pandas to identify and remove the corruption (the flaw described on your mission card).
3. **DECRYPT:** Calculate the "Stability Key" (a specific statistic) from the clean data.
4. **UPLOAD:** Shout the key to the Central Bank Commander (Professor) to lock it into the mainframe.

**VICTORY CONDITION:** All 10 District Keys must be entered before Market Health reaches 0%.

---

### 3. THE PROTOCOLS (RULES OF ENGAGEMENT)

**⚠️ DIRECTIVE 1: THE "CONSULTANT" PROTOCOL**
If your team successfully stabilizes your market (enters the correct key), you are immediately drafted as **Global Consultants**.

* You **MUST** stand up and find a team that is struggling.
* You **MAY** explain logic, syntax, and debugging strategies.
* You **MAY NOT** touch their keyboard or write the code for them.

**⚠️ DIRECTIVE 2: THE FINAL INTEGRATION**
Once all 10 markets are stable, a **Master Equation** will appear on the main screen.

* This equation requires data from **ALL** districts.
* You will need to communicate with other teams to solve it.
* The game is not over until the Master Equation is solved.

---

**Group 1: District 1**

* **File:** `district_1.csv`
* **Mission:** Sensors are failing. The price feed has random blanks (`NaN`).
* **Action:** Drop all rows with missing prices. Calculate the **SUM** of the clean prices. (Integer).

**Group 2: District 2**

* **File:** `district_2.csv`
* **Mission:** A loop error caused transactions to record twice.
* **Action:** Drop duplicate rows. Calculate the **SUM** of the unique prices. (Integer).

**Group 3: District 3**

* **File:** `district_3.csv`
* **Mission:** The legacy system put a `$` sign on all prices (e.g., `$50.00`).
* **Action:** Remove the `$` and convert to float. Calculate the **MEAN** price. (Integer).

**Group 4: District 4**

* **File:** `district_4.csv`
* **Mission:** The prices are strings with commas (e.g., `"1,200.50"`).
* **Action:** Remove the `,` and convert to float. Calculate the **SUM** of prices. (Integer).

**Group 5: District 5**

* **File:** `district_5.csv`
* **Mission:** A bug is generating negative prices.
* **Action:** Filter the data to keep only prices **greater than 0**. Calculate the **MEAN** of the valid prices. (Integer).

**Group 6: District 6**

* **File:** `district_6.csv`
* **Mission:** Massive outliers (Prices > 90,000) are skewing the data.
* **Action:** Filter data to keep prices **under 1,000**. Find the **MAXIMUM** remaining price. (Integer).

**Group 7: District 7**

* **File:** `district_7.csv`
* **Mission:** Micro-transactions (under $5.00) are noise.
* **Action:** Filter data to keep prices **greater than 5**. Find the **MINIMUM** remaining price. (Integer).

**Group 8: District 8**

* **File:** `district_8.csv`
* **Mission:** We only care about Category 'A'.
* **Action:** Filter the dataset for `category == 'A'`. Calculate the **SUM** of those prices. (Integer).

**Group 9: District 9**

* **File:** `district_9.csv`
* **Mission:** We need the transaction volume for the year 2025 only.
* **Action:** Convert the date column. Filter for the year 2025. **COUNT** how many rows exist. (Integer).

**Group 10: District 10**

* **File:** `district_10.csv`
* **Mission:** We are missing the Revenue column.
* **Action:** Create a new column: `Revenue = Price * Quantity`. Calculate the **SUM** of the Revenue. (Integer).

---

### 4. PANDAS SURVIVAL GUIDE (TECHNICAL REFERENCE)

*Use these snippets to restore system integrity.*

#### 🔍 INSPECTING THE DAMAGE

* **See the first 5 rows:** `df.head()`
* **Check data types & missing values:** `df.info()`
* **Count missing values:** `df.isna().sum()`
* **See summary statistics:** `df.describe()`

#### 🧹 CLEANING THE DATA

* **Drop rows with missing values:**
`df_clean = df.dropna()`
* **Drop duplicate rows:**
`df_clean = df.drop_duplicates()`
* **Remove characters (e.g., '\$' or ',') and convert to number:**
`df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)`
* **Convert a date column:**
`df['date'] = pd.to_datetime(df['date'])`

#### 🛡️ FILTERING (QUERIES)

* **Keep only prices greater than 0:**
`df_clean = df[df['price'] > 0]`
* **Keep only 'Sector A':**
`df_clean = df[df['category'] == 'Sector A']`
* **Keep only the year 2025:**
`df_clean = df[df['date'].dt.year == 2025]`

#### 🔑 CALCULATING THE KEY

* **Sum:** `df['price'].sum()`
* **Mean (Average):** `df['price'].mean()`
* **Maximum:** `df['price'].max()`
* **Minimum:** `df['price'].min()`
* **Count rows:** `len(df)` or `df['price'].count()`

