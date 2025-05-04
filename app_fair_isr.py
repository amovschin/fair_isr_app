import numpy as np
import pandas as pd
import streamlit as st
from fair_isr_utils import calcul_impot_foyer, calcul_impot_indiv

# --- Title ---
st.title("Calcul de l'impôt sur le revenu individuel")

### Impôt 
st.header("Calcul de l'impôt individuel")

if 'show_impot' not in st.session_state:
    st.session_state['show_impot'] = False
if 'show_rap' not in st.session_state:
    st.session_state['show_rap'] = False

if 'name_1' not in st.session_state:
    st.session_state['name_1'] = "Déclarant 1"
if 'name_2' not in st.session_state:
    st.session_state['name_2'] = "Déclarant 2"
if 'salaire_1' not in st.session_state:
    st.session_state['salaire_1'] = 0.0
if 'salaire_2' not in st.session_state:
    st.session_state['salaire_2'] = 0.0
if 'nb_parts' not in st.session_state:
    st.session_state['nb_parts'] = 0.0

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Déclarant 1")
    name_1 = st.text_input("Nom du déclarant 1", key='name_1')
    salaire_1 = st.number_input(f"Revenus du déclarant 1", 
                                min_value=0.0, format="%.0f", key="salaire_1")

with col2:
    st.subheader("Déclarant 2")
    name_2 = st.text_input("Nom du déclarant 2", key='name_2')
    salaire_2 = st.number_input(f"Revenus du déclarant 2", 
                                min_value=0.0, format="%.0f", key="salaire_2")

nb_parts = st.number_input(f"Nombre de parts pour le foyer", min_value=0.0, format="%.1f", key="nb_parts")

# --- Other parameters  ---
# barème d'imposition
bareme_2025 = pd.DataFrame({"seuil": [11498, 29316, 83824, 180295, 1e15], "taux": [0, 11, 30, 41, 45]}) 

# plafond du quotient familial pour une demi-part
plafond_demi_part_2025 = 1791

# plafond de dépense par enfant gardé
plafond_depense_par_enfant_gardé = 3500

if 'impot_1' not in st.session_state:
    st.session_state['impot_1'] = 0
if 'impot_2' not in st.session_state:
    st.session_state['impot_2'] = 0
if 'rni_1' not in st.session_state:
    st.session_state['rni_1'] = 0
if 'rni_2' not in st.session_state:
    st.session_state['rni_2'] = 0

# --- Compute ---
if st.button("Calculer l'impôt individuel"):
    # Here, call your script functions
    rni_1 = st.session_state['salaire_1'] * 0.9
    rni_2 = st.session_state['salaire_2'] * 0.9
    ii_1, ii_2 = calcul_impot_indiv(rni_1, rni_2, nb_parts, bareme=bareme_2025, plafond_demi_part=plafond_demi_part_2025)
    st.session_state['rni_1'] = rni_1
    st.session_state['rni_2'] = rni_2
    st.session_state['impot_1'] = ii_1
    st.session_state['impot_2'] = ii_2
    st.session_state['show_impot'] = True

if st.session_state['show_impot']:
    st.success(f"Revenu net imposable: {name_1} --> {st.session_state['rni_1']:.0f}, "
               f"{name_2} --> {st.session_state['rni_2']:.0f}, "
               f"total --> {abs(st.session_state['rni_1'] + st.session_state['rni_2']):.0f}")
    st.success(f"Impôt sur le revenu: {name_1} --> {abs(st.session_state['impot_1']):.0f}, "
               f"{name_2} --> {abs(st.session_state['impot_2']):.0f}, "
               f"total --> {abs(st.session_state['impot_1'] + st.session_state['impot_2']):.0f}")


### Reste à payer / récupérer
st.header("Calcul du reste à payer / récupérer")

if 'pas_1' not in st.session_state:
    st.session_state['pas_1'] = 0.0
if 'pas_2' not in st.session_state:
    st.session_state['pas_2'] = 0.0
if 'case_7UD_1' not in st.session_state:
    st.session_state['case_7UD_1'] = 0.0
if 'case_7UD_2' not in st.session_state:
    st.session_state['case_7UD_2'] = 0.0
if 'case_7UF_1' not in st.session_state:
    st.session_state['case_7UF_1'] = 0.0
if 'case_7UF_2' not in st.session_state:
    st.session_state['case_7UF_2'] = 0.0
if 'case_7GA' not in st.session_state:
    st.session_state['case_7GA'] = 0.0
if 'case_7DB' not in st.session_state:
    st.session_state['case_7DB'] = 0.0
if 'case_7DR' not in st.session_state:
    st.session_state['case_7DR'] = 0.0
if 'avance' not in st.session_state:
    st.session_state['avance'] = 0.0

if 'reduc_1' not in st.session_state:
    st.session_state['reduc_1'] = 0.0
if 'reduc_2' not in st.session_state:
    st.session_state['reduc_2'] = 0.0
if 'credit_1' not in st.session_state:
    st.session_state['credit_1'] = 0.0
if 'credit_2' not in st.session_state:
    st.session_state['credit_2'] = 0.0
if 'rap_1' not in st.session_state:
    st.session_state['rap_1'] = 0.0
if 'rap_2' not in st.session_state:
    st.session_state['rap_2'] = 0.0
if 'rap_corrige_1' not in st.session_state:
    st.session_state['rap_corrige_1'] = 0.0
if 'rap_corrige_2' not in st.session_state:
    st.session_state['rap_corrige_2'] = 0.0

col1, col2 = st.columns(2)

with col1:
    st.subheader("Déclarant 1")
    pas_1 = st.number_input(f"Impôt déjà prélevé à la source pour le déclarant 1", 
                            min_value=0.0, format="%.0f", key="pas_1")
    case_7UD_1 = st.number_input(f"Dons aux personnes en difficulté  (case 7UD, donnant droit à 75% de réduction d'impôt, "
                                 f"limité à 1000€ pour le foyer)", 
                                 min_value=0.0, format="%.0f", key="case_7UD_1")
    case_7UF_1 = st.number_input(f"Dons versés à d'autres organismes d'intérêt général (case 7UF, donnant droit à "
                                 f"66% de réduction d'impôt)", 
                                 min_value=0.0, format="%.0f", key="case_7UF_1")

with col2:
    st.subheader("Déclarant 2")
    pas_2 = st.number_input(f"Impôt déjà prélevé à la source pour le déclarant 2", 
                            min_value=0.0, format="%.0f", key="pas_2")
    case_7UD_2 = st.number_input(f"Dons aux personnes en difficulté  (case 7UD, donnant droit à 75% de réduction d'impôt, "
                                 f"limité à 1000€ pour le foyer)", 
                                 min_value=0.0, format="%.0f", key="case_7UD_2")
    case_7UF_2 = st.number_input(f"Dons versés à d'autres organismes d'intérêt général (case 7UF, donnant droit à "
                                 f"66% de réduction d'impôt)", 
                                 min_value=0.0, format="%.0f", key="case_7UF_2")

case_7GA = st.number_input(f"frais de garde (e.g. crèche, périscolaire) (case 7GA)", 
                           min_value=0.0, format="%.0f", key="case_7GA")
case_7DB = st.number_input(f"dépenses aide à domicile (e.g. nounou) (case 7DB)", 
                           min_value=0.0, format="%.0f", key="case_7DB")
case_7DR = st.number_input(f"aides perçues pour l'emploi à domicile (e.g. CAF) (case 7DR)", 
                           min_value=0.0, format="%.0f", key="case_7DR")
avance = st.number_input(f"Avance perçue sur les réductions et crédits d'impot", 
                         min_value=0.0, format="%.0f", key="avance")

# --- Compute ---
if st.button("Calculer le reste à payer / récupérer"):
    # impot
    impot_1 = st.session_state['impot_1']
    impot_2 = st.session_state['impot_2']
    pas_1 = st.session_state['pas_1']
    pas_2 = st.session_state['pas_2']
    
    # Réduction d'impôt
    reduc_1 = st.session_state['case_7UD_1'] * 0.75 + st.session_state['case_7UF_1'] * 0.66
    reduc_2 = st.session_state['case_7UD_2'] * 0.75 + st.session_state['case_7UF_2'] * 0.66
    st.session_state['reduc_1'] = reduc_1
    st.session_state['reduc_2'] = reduc_2

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
    st.session_state['credit_1'] = credit_1
    st.session_state['credit_2'] = credit_2

    rap_1 = impot_1 - reduc_1 - credit_1 - pas_1
    rap_2 = impot_2 - reduc_2 - credit_2 - pas_2
    rap_foyer = rap_1 + rap_2
    rap_corrige_1 = rap_1 + avance / 2
    rap_corrige_2 = rap_2 + avance / 2
    rap_corrige_foyer = rap_corrige_1 + rap_corrige_2
    st.session_state['rap_1'] = rap_1
    st.session_state['rap_2'] = rap_2
    st.session_state['rap_corrige_1'] = rap_corrige_1
    st.session_state['rap_corrige_2'] = rap_corrige_2

    st.session_state['show_rap'] = True

if st.session_state['show_rap']:
    reduc_1 = st.session_state['reduc_1']
    reduc_2 = st.session_state['reduc_2']
    reduc_foyer = reduc_1 + reduc_2
    credit_1 = st.session_state['credit_1']
    credit_2 = st.session_state['credit_2']
    credit_foyer = credit_1 + credit_2
    rap_1 = st.session_state['rap_1']
    rap_2 = st.session_state['rap_2']
    rap_foyer = rap_1 + rap_2
    rap_corrige_1 = st.session_state['rap_corrige_1']
    rap_corrige_2 = st.session_state['rap_corrige_2']
    rap_corrige_foyer = rap_corrige_1 + rap_corrige_2
    
    st.success(f"réduction d'impôt: {name_1} --> **{reduc_1:.0f}**, {name_2} --> **{reduc_2:.0f}** (total --> {reduc_foyer:.0f})")
    st.success(f"crédit d'impôt: {name_1} --> **{credit_1:.0f}**, {name_2} --> **{credit_2:.0f}** (total --> {credit_foyer:.0f})")
    st.success(f"Avant avance perçue, {name_1} doit **{'payer' if rap_1>0 else 'récupérer'} {abs(rap_1):.0f}**, "
               f"{name_2} doit **{'payer' if rap_2>0 else 'récupérer'} {abs(rap_2):.0f}** "
               f"(le foyer doit {'payer' if rap_foyer>0 else 'récupérer'} {abs(rap_foyer):.0f})")
    st.success(f"Après avance perçue, {name_1} doit **{'payer' if rap_corrige_1>0 else 'récupérer'} {abs(rap_corrige_1):.0f}**, "
               f"{name_2} doit **{'payer' if rap_corrige_2>0 else 'récupérer'} {abs(rap_corrige_2):.0f}** "
               f"(le foyer doit encore {'payer' if rap_corrige_foyer>0 else 'récupérer'} {abs(rap_corrige_foyer):.0f})")


