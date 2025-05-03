import numpy as np
import pandas as pd
import streamlit as st
from fair_isr_utils import calcul_impot_foyer, calcul_impot_indiv

# --- Title ---
st.title("Calcul de l'impôt sur le revenu individuel")

# --- User Inputs ---
person1_name = st.text_input("Nom du déclarant 1")
person2_name = st.text_input("Nom du déclarant 2")

salaire_1 = st.number_input(f"Revenus de {person1_name}", min_value=0.0, key="rni_1")
salaire_2 = st.number_input(f"Revenus de {person2_name}", min_value=0.0, key="rni_2")

nb_parts = st.number_input(f"Nombre de parts pour le foyer", min_value=0.0, key="nb_parts")

# --- Other parameters  ---
# barème d'imposition
bareme_2025 = pd.DataFrame({"seuil": [11498, 29316, 83824, 180295, 1e15], "taux": [0, 11, 30, 41, 45]}) 

# plafond du quotient familial pour une demi-part
plafond_demi_part_2025 = 1791

# plafond de dépense par enfant gardé
plafond_depense_par_enfant_gardé = 3500

# --- Compute ---
if st.button("Calculer l'impôt individuel"):
    # Here, call your script functions
    rni_1 = salaire_1 * 0.9
    rni_2 = salaire_2 * 0.9
    print(f"Revenu net imposable de {person1_name}: {rni_1}")
    print(f"Revenu net imposable de {person2_name}: {rni_2}")
    impot_1, impot_2 = calcul_impot_indiv(rni_1, rni_2, nb_parts, bareme=bareme_2025, plafond_demi_part=plafond_demi_part_2025)
    
    st.success(f"L'impôt sur le revenu de {person1_name} est {abs(impot_1):.2f}")
    st.success(f"L'impôt sur le revenu de {person2_name} est {abs(impot_2):.2f}")

pas_1 = st.number_input(f"Impôt déjà prélevé à la source pour {person1_name}", min_value=0.0, key="pas_1")
pas_2 = st.number_input(f"Impôt déjà prélevé à la source pour {person2_name}", min_value=0.0, key="pas_2")

