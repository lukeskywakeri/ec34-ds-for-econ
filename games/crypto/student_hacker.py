import requests
import time
import numpy as np  # Essential for cracking matrix encryption

# --- CONFIGURATION ---
# 1. Enter the IP address shown on the projector
SERVER_URL = "http://127.0.0.1:8000" 

# 2. Your Hacker Alias
ALIAS = "Zero_Cool"

def crack_encryption(challenge):
    """
    Decodes the security challenge from the bank mainframe.
    Returns the numeric key to bypass the firewall.
    """
    print(f"\n🔒 ENCRYPTED CHALLENGE: {challenge}")
    
    # === SECURITY LAYER 1: PYTHON BASICS ===
    
    if "2 to the power of 8" in challenge:
        # TODO: Return 2 to the power of 8
        return 0
        
    elif "SLICE" in challenge:
        # Q: Sum of last 2 items in [10, 20, 30, 40, 50]
        data = [10, 20, 30, 40, 50]
        # TODO: Use negative slicing and sum()
        return 0
        
    elif "KEYGEN" in challenge:
        # Q: Value of key 'b' in {'a': 10, 'b': 20}
        d = {'a': 10, 'b': 20}
        # TODO: Access the dictionary value
        return 0
        
    elif "LOOP" in challenge:
        # Q: Sum of squares of [1, 2, 3]
        data = [1, 2, 3]
        # TODO: Calculate 1^2 + 2^2 + 3^2
        return 0
        
    elif "STRING" in challenge:
        # Q: Length of string 'Data' multiplied by 5
        return 0

    # === SECURITY LAYER 2: NUMPY MATRICES ===
    
    elif "MATRIX" in challenge:
        # Q: Mean of [10, 20, 30, 40]
        arr = np.array([10, 20, 30, 40])
        # TODO: Return the mean
        return 0
        
    elif "VECTOR" in challenge:
        # Q: Dot Product of [1, 2] and [3, 4]
        a = np.array([1, 2])
        b = np.array([3, 4])
        # TODO: Return dot product (a @ b)
        return 0
        
    elif "BROADCAST" in challenge:
        # Q: Sum of elements in (np.array([1, 2]) + 10)
        arr = np.array([1, 2])
        # TODO: Add 10 to array, then sum results
        return 0
        
    elif "ARGMAX" in challenge:
        # Q: Index of max value in [1, 5, 2, 4]
        arr = np.array([1, 5, 2, 4])
        # TODO: Return index of max value
        return 0
        
    elif "SHAPE" in challenge:
        # Q: Number of columns in array reshaped to (2, 5)
        # HINT: A shape is (rows, cols). Return cols.
        return 0

    return 0

def hack_loop():
    print(f"💀 INITIALIZING HACK SEQUENCE FOR {ALIAS}...")
    print(f"📡 TARGETING {SERVER_URL}...")
    
    while True:
        try:
            # 1. Scan for vulnerability (Get Job)
            response = requests.get(f"{SERVER_URL}/get_target", timeout=5)
            if response.status_code != 200:
                print("⚠️  Link unstable. Retrying...")
                time.sleep(2)
                continue
                
            data = response.json()
            problem_id = data["problem_id"]
            challenge_text = data["question"]
            
            # 2. Crack the encryption (Solve)
            key = crack_encryption(challenge_text)
            
            # 3. Inject payload (Submit)
            payload = {
                "hacker_alias": ALIAS,
                "problem_id": problem_id,
                "answer": float(key)
            }
            
            print(f"   💉 Injecting Key: {key}")
            
            post_response = requests.post(f"{SERVER_URL}/inject", json=payload, timeout=5)
            res_json = post_response.json()
            
            if post_response.status_code == 200:
                print(f"   ✅ ACCESS GRANTED! {res_json.get('message')}")
            else:
                print(f"   ⛔ ACCESS DENIED: {res_json.get('message')}")
            
            time.sleep(1.5) # Avoid detection
            
        except Exception as e:
            print(f"⚠️  Connection Dropped: {e}")
            time.sleep(2)

if __name__ == "__main__":
    hack_loop()