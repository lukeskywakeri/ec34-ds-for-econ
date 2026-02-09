import streamlit as st
import time
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="PROTOCOL: DECIMATION", layout="wide")
START_HEALTH = 100
DECAY_RATE = 5  # Health lost per minute

# --- ANSWERS (PASTE FROM PART 1 OUTPUT) ---
# UPDATE THESE NUMBERS AFTER RUNNING THE GENERATOR SCRIPT!
CORRECT_KEYS = {
    "District 1": "48998", 
    "District 2": "54700",
    "District 3": "54",
    "District 4": "56824",
    "District 5": "56",
    "District 6": "99",
    "District 7": "10",
    "District 8": "18373",
    "District 9": "365",
    "District 10": "284037"
}

# --- STATE MANAGEMENT ---
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()
if 'unlocked' not in st.session_state:
    st.session_state['unlocked'] = []
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False

# --- UI HEADER ---
st.title("⚠️ PROTOCOL: DECIMATION")
st.markdown("### CENTRAL BANK MAINFRAME")

# --- TIMER LOGIC ---
elapsed_time = time.time() - st.session_state['start_time']
minutes_passed = int(elapsed_time // 60)
current_health = max(0, START_HEALTH - (minutes_passed * DECAY_RATE))

# Health Bar Visualization
health_color = "green" if current_health > 50 else "orange" if current_health > 20 else "red"
st.markdown(f"""
    <div style="border: 2px solid #333; border-radius: 5px; padding: 10px; text-align: center;">
        <h2 style="color:{health_color}; margin:0;">SYSTEM INTEGRITY: {current_health}%</h2>
        <p>DECAY RATE: -{DECAY_RATE}% PER MINUTE</p>
    </div>
""", unsafe_allow_html=True)
st.progress(current_health / 100)

if current_health == 0:
    st.error("SYSTEM CRITICAL. GLOBAL MARKET COLLAPSE.")
    st.stop()

# --- THE 10 REGIONS ---
st.divider()
st.subheader("REGIONAL FIREWALLS")

# Create 2 rows of 5 columns
cols = st.columns(5) + st.columns(5)

for i, (district, correct_val) in enumerate(CORRECT_KEYS.items()):
    with cols[i]:
        if district in st.session_state['unlocked']:
            st.success(f"✅ {district}")
            st.metric("KEY", correct_val)
        else:
            st.warning(f"🔒 {district}")
            user_input = st.text_input(f"Input Key", key=f"in_{i}")
            if st.button(f"Unlock", key=f"btn_{i}"):
                if user_input.strip() == correct_val:
                    st.session_state['unlocked'].append(district)
                    st.rerun()
                else:
                    st.toast(f"❌ INCORRECT KEY FOR {district}", icon="⚠️")

# --- THE FINAL BOSS (INTEGRATION) ---
st.divider()
if len(st.session_state['unlocked']) == 10:
    st.markdown("## 🔓 ALL REGIONS STABILIZED. FINAL EQUATION REVEALED.")
    st.info("CALCULATE THE GRAND EQUILIBRIUM:")
    
    st.latex(r'''
        \text{FINAL KEY} = \frac{\text{Sum(Districts 1-5)}}{\text{Sum(Districts 6-10)}}
    ''')
    
    final_input = st.text_input("ENTER GRAND EQUILIBRIUM (Round to 2 decimals):")
    
    # Calculate the real final answer based on the keys
    # (Teacher: You don't need to hardcode this, the code does it)
    keys = list(CORRECT_KEYS.values())
    top_sum = sum([float(k) for k in keys[:5]])
    bottom_sum = sum([float(k) for k in keys[5:]])
    final_answer = round(top_sum / bottom_sum, 2)
    
    if st.button("EXECUTE GLOBAL RESTORE"):
        if final_input == str(final_answer):
            st.balloons()
            st.success(f"SYSTEM RESTORED! FINAL VALUE: {final_answer}")
            st.markdown("# 🏆 CLASS VICTORY 🏆")
            st.stop()
        else:
            st.error("CALCULATION ERROR. CHECK YOUR SUMS.")
else:
    st.caption(f"Stabilize all 10 districts to reveal the Master Equation. ({len(st.session_state['unlocked'])}/10)")

# --- AUTO REFRESH LOOP ---
# This forces the page to reload every 5 seconds to update the Health Bar
# independent of student input.
time.sleep(5)
st.rerun()