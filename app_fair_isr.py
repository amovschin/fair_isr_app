import streamlit as st

# --- Title ---
st.title("Cost Repartition Calculator")

# --- User Inputs ---
person1_name = st.text_input("Person 1 Name")
person2_name = st.text_input("Person 2 Name")

cost_1 = st.number_input(f"Cost incurred by {person1_name}", min_value=0.0, key="cost_1")
cost_2 = st.number_input(f"Cost incurred by {person2_name}", min_value=0.0, key="cost_2")

# Any other parameters you need can be added similarly

# --- Compute ---
if st.button("Compute Fair Repartition"):
    # Here, call your script functions
    total_cost = cost_1 + cost_2
    fair_share = total_cost / 2
    person1_balance = fair_share - cost_1
    person2_balance = fair_share - cost_2
    
    st.success(f"{person1_name} should {'receive' if person1_balance > 0 else 'pay'} {abs(person1_balance):.2f}")
    st.success(f"{person2_name} should {'receive' if person2_balance > 0 else 'pay'} {abs(person2_balance):.2f}")


