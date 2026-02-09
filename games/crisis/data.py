import pandas as pd
import numpy as np
import os

# Create folder for game files
if not os.path.exists('game_data'):
    os.makedirs('game_data')

np.random.seed(42) # Deterministic seed so answers are always the same

def generate_district(id, flaw):
    n = 1000
    df = pd.DataFrame({
        'transaction_id': range(n),
        'price': np.random.uniform(10, 100, n),
        'quantity': np.random.randint(1, 10, n),
        'category': np.random.choice(['A', 'B', 'C'], n),
        'status': 'confirmed'
    })
    
    # Round prices for neatness
    df['price'] = df['price'].round(2)

    # --- INJECT FLAWS ---
    if flaw == 'nans': # District 1: Drop NaNs
        df.loc[::10, 'price'] = np.nan
        answer = int(df['price'].sum())
        
    elif flaw == 'dupes': # District 2: Drop Duplicates
        df = pd.concat([df, df.iloc[:100]])
        answer = int(df.drop_duplicates()['price'].sum())
        
    elif flaw == 'currency_sign': # District 3: Remove '$'
        # Calculate answer BEFORE messing up data
        answer = int(df['price'].mean()) 
        df['price'] = df['price'].apply(lambda x: f"${x:.2f}")
        
    elif flaw == 'commas': # District 4: Remove ',' (e.g., "1,000")
        df.loc[0, 'price'] = 1500.00 # Make sure at least one needs a comma
        answer = int(df['price'].sum())
        df['price'] = df['price'].apply(lambda x: f"{x:,.2f}")

    elif flaw == 'negatives': # District 5: Filter out negative errors
        df.loc[::20, 'price'] = df.loc[::20, 'price'] * -1
        answer = int(df[df['price'] > 0]['price'].mean())
        
    elif flaw == 'outliers_high': # District 6: Filter < 1000
        df.loc[0:5, 'price'] = 99999
        answer = int(df[df['price'] < 1000]['price'].max())
        
    elif flaw == 'outliers_low': # District 7: Filter > 5
        df.loc[0:5, 'price'] = 0.01
        answer = int(df[df['price'] > 5]['price'].min())
        
    elif flaw == 'wrong_cat': # District 8: Filter Category == 'A' only
        answer = int(df[df['category'] == 'A']['price'].sum())
        
    elif flaw == 'dates': # District 9: Filter Year == 2025
        dates = pd.date_range('2024-01-01', periods=n, freq='D')
        df['date'] = dates
        target_df = df[df['date'].dt.year == 2025]
        answer = int(target_df['price'].count())
        
    elif flaw == 'calc': # District 10: Calculate Revenue (P * Q) then Sum
        answer = int((df['price'] * df['quantity']).sum())

    df.to_csv(f'game_data/district_{id}.csv', index=False)
    return answer

# Generate and print answers for the Teacher Key
print("--- TEACHER ANSWER KEY ---")
flaws = ['nans', 'dupes', 'currency_sign', 'commas', 'negatives', 
         'outliers_high', 'outliers_low', 'wrong_cat', 'dates', 'calc']
answers = {}

for i, flaw in enumerate(flaws):
    ans = generate_district(i+1, flaw)
    answers[f"District {i+1}"] = str(ans)
    print(f"District {i+1}: {ans} ({flaw})")

print("--------------------------")