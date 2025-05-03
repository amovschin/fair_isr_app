import numpy as np
import pandas as pd
import streamlit as st
from fair_isr_utils import calcul_impot_foyer, calcul_impot_indiv

# --- Title ---
st.title("Calcul de l'impôt sur le revenu individuel")

### Impôt 
st.header("Calcul de l'impôt individuel")

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Déclarant 1")
    person1_name = st.text_input("Nom du déclarant 1", value="Déclarant 1")
    salaire_1 = st.number_input(f"Revenus de {person1_name}", min_value=0.0, format="%.0f", key="rni_1")

with col2:
    st.subheader("Déclarant 2")
    person2_name = st.text_input("Nom du déclarant 2", value="Déclarant 1")
    salaire_2 = st.number_input(f"Revenus de {person2_name}", min_value=0.0, format="%.0f", key="rni_2")

nb_parts = st.number_input(f"Nombre de parts pour le foyer", min_value=0.0, format="%.1f", key="nb_parts")

# --- Other parameters  ---
# barème d'imposition
bareme_2025 = pd.DataFrame({"seuil": [11498, 29316, 83824, 180295, 1e15], "taux": [0, 11, 30, 41, 45]}) 

# plafond du quotient familial pour une demi-part
plafond_demi_part_2025 = 1791

# plafond de dépense par enfant gardé
plafond_depense_par_enfant_gardé = 3500

impot_1 = 0
impot_2 = 0

# --- Compute ---
if st.button("Calculer l'impôt individuel"):
    # Here, call your script functions
    rni_1 = salaire_1 * 0.9
    rni_2 = salaire_2 * 0.9
    st.success(f"Revenu net imposable de {person1_name}: {rni_1}")
    st.success(f"Revenu net imposable de {person2_name}: {rni_2}")
    ii_1, ii_2 = calcul_impot_indiv(rni_1, rni_2, nb_parts, bareme=bareme_2025, plafond_demi_part=plafond_demi_part_2025)
    impot_1 += ii_1
    impot_2 += ii_2
    st.success(f"L'impôt sur le revenu de {person1_name} est {abs(impot_1):.0f}")
    st.success(f"L'impôt sur le revenu de {person2_name} est {abs(impot_2):.0f}")


### Reste à payer / récupérer
st.header("Calcul du reste à payer / récupérer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Déclarant 1")
    pas_1 = st.number_input(f"Impôt déjà prélevé à la source pour {person1_name}", value=0.0, min_value=0.0, format="%.0f", key="pas_1")
    case_7UD_1 = st.number_input(f"Dons aux personnes en difficulté  (case 7UD, donnant droit à 75% de réduction d'impôt, "
                                 f"limité à 1000€ pour le foyer)", value=0.0, min_value=0.0, format="%.0f", key="case_7UD_1")
    case_7UF_1 = st.number_input(f"Dons versés à d'autres organismes d'intérêt général (case 7UF, donnant droit à "
                                 f"66% de réduction d'impôt)", value=0.0, min_value=0.0, format="%.0f", key="case_7UF_1")

with col2:
    st.subheader("Déclarant 2")
    pas_2 = st.number_input(f"Impôt déjà prélevé à la source pour {person2_name}", min_value=0.0, format="%.0f", key="pas_2")
    case_7UD_2 = st.number_input(f"Dons aux personnes en difficulté  (case 7UD, donnant droit à 75% de réduction d'impôt, "
                                f"limité à 1000€ pour le foyer)", min_value=0.0, format="%.0f", key="case_7UD_2")
    case_7UF_2 = st.number_input(f"Dons versés à d'autres organismes d'intérêt général (case 7UF, donnant droit à "
                                 f"66% de réduction d'impôt)", min_value=0.0, format="%.0f", key="case_7UF_2")

case_7GA = st.number_input(f"frais de garde (e.g. crèche, périscolaire) (case 7GA)", min_value=0.0, format="%.0f", key="case_7GA")
case_7DB = st.number_input(f"dépenses aide à domicile (e.g. nounou) (case 7DB)", min_value=0.0, format="%.0f", key="case_7DB")
case_7DR = st.number_input(f"aides perçues pour l'emploi à domicile (e.g. CAF) (case 7DR)", min_value=0.0, format="%.0f", key="case_7DR")
avance = st.number_input(f"Avance perçue sur les réductions et crédits d'impot", value=0.0, min_value=0.0, format="%.0f", key="avance")

# --- Compute ---
if st.button("Calculer le reste à payer / récupérer"):
    # Réduction d'impôt
    reduc_1 = case_7UD_1 * 0.75 + case_7UF_1 * 0.66
    reduc_2 = case_7UD_2 * 0.75 + case_7UF_2 * 0.66
    reduc_foyer = reduc_1 + reduc_2

    # Crédit d'impôt
    credit_foyer_garde = min(plafond_depense_par_enfant_gardé, case_7GA) * 0.5
    credit_foyer_aide = (case_7DB - case_7DR) * 0.5
    credit_foyer = credit_foyer_garde + credit_foyer_aide

    credit_1_garde = credit_foyer_garde * 0.5
    credit_1_aide = credit_foyer_aide * 0.5
    credit_1 = credit_1_garde + credit_1_aide
    credit_2_garde = credit_foyer_garde * 0.5
    credit_2_aide = credit_foyer_aide * 0.5
    credit_2 = credit_2_garde + credit_2_aide

    rap_1 = impot_1 - reduc_1 - credit_1 - pas_1
    rap_2 = impot_2 - reduc_2 - credit_2 - pas_2
    rap_foyer = rap_1 + rap_2

    rap_corrige_1 = rap_1 + avance / 2
    rap_corrige_2 = rap_2 + avance / 2
    rap_corrige_foyer = rap_corrige_1 + rap_corrige_2

    st.success(f"réduction d'impôt pour le déclarant 1: {reduc_1}")
    st.success(f"réduction d'impôt pour le déclarant 2: {reduc_2}")
    st.success(f"réduction d'impôt pour le foyer: {reduc_foyer}")

    st.success(f"crédit d'impôt pour le déclarant 1: {credit_1}")
    st.success(f"crédit d'impôt pour le déclarant 2: {credit_2}")
    st.success(f"crédit d'impôt pour le foyer: {credit_foyer}")

    st.success(f"reste à {'payer' if rap_1>0 else 'récupérer'} pour déclarant 1 (avant avance perçue): {rap_1}")
    st.success(f"reste à {'payer' if rap_2>0 else 'récupérer'} pour déclarant 2 (avant avance perçue): {rap_2}")
    st.success(f"reste à {'payer' if rap_foyer>0 else 'récupérer'} pour le foyer (avant avance perçue): {rap_foyer}")

    st.success(f"reste à {'payer' if rap_corrige_1>0 else 'récupérer'} pour déclarant 1 (après avance perçue): {rap_corrige_1}")
    st.success(f"reste à {'payer' if rap_corrige_2>0 else 'récupérer'} pour déclarant 2 (après avance perçue): {rap_corrige_2}")
    st.success(f"reste à {'payer' if rap_corrige_foyer>0 else 'récupérer'} pour le foyer (après avance perçue): {rap_corrige_foyer}")


