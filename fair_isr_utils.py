import numpy as np
import pandas as pd

# une fonction pour remplir progressivement et équitablement les tranches du barème
def fill_buckets(inputs, buckets):
    """
    Distributes multiple input values equally across a list of bucket sizes.
    Inputs fill equally as much as possible until depleted.
    Any leftover is assigned to an additional infinite bucket.

    Parameters:
    - inputs (list or np.ndarray of float): List of values to distribute (e.g., [x1, x2, x3, ...]).
    - buckets (list or np.ndarray of float): List of bucket capacities.

    Returns:
    - np.ndarray: A 2D array where each row corresponds to one input,
                  and each column to a bucket (including an extra bucket if needed).
    """
    inputs = np.array(inputs, dtype=float)
    buckets = np.array(buckets, dtype=float)

    n_inputs = len(inputs)
    filled = []

    x = inputs.copy()

    for b in buckets:
        allocation = np.zeros(n_inputs)
        remaining = b

        active = x > 0  # inputs still having remaining value
        
        while remaining > 0 and active.any():
            n_active = active.sum()
            share = remaining / n_active

            # Find how much each active input can provide
            contrib = np.minimum(x, share)
            allocation += contrib
            x -= contrib
            remaining -= contrib.sum()
            active = x > 0  # update active inputs

        filled.append(allocation)

    # If there are leftovers, put them into an infinite bucket
    if x.sum() > 0:
        filled.append(x.copy())

    filled_array = np.array(filled).T  # shape (n_inputs, n_buckets)

    return filled_array


# une fonction pour soustraire équitablement les plafond de réduction pour les demi-parts
def subtract_d(xs, d, min_keep=None):
    """
    Subtract a total amount `d` from the elements of a list `xs`,
    distributing the subtraction equally among nonzero elements, 
    stopping elements at zero when needed.

    Parameters:
    xs (list of float or int): List of input numbers.
    d (float or int): The total amount to subtract.
    min_keep (list of float or int): minimum to keep in each input. Default is None, 
                                     corresponding to 0 for each input.

    Returns:
    tuple of floats: The new values after subtraction.
    
    Example:
    >>> subtract_d([1000, 800], 400)
    (800.0, 600.0)
    
    >>> subtract_d([1000, 100], 400)
    (700.0, 0.0)
    """
    x = np.array(xs, dtype=float)
    if min_keep is None:
        min_keep = np.zeros(len(x),)
    else:
        min_keep = np.array(min_keep, dtype=float)
    while d > 0 and np.any(x > min_keep):
        active = x > min_keep
        n_active = active.sum()
        if n_active == 0:
            break
        share = d / n_active
        to_subtract = np.minimum(x[active] - min_keep[active], share)
        x[active] -= to_subtract
        d -= to_subtract.sum()
    return tuple(x)


def calcul_impot_foyer_sans_plafond(rni, nb_parts, seuil, taux):
    quotient = rni / nb_parts
    buckets = seuil.copy()
    buckets[1:] -= buckets[:-1]
    tranches = fill_buckets([quotient], buckets)[0]
    return np.sum(tranches * taux / 100) * nb_parts

def calcul_impot_foyer(rni, nb_parts, bareme, plafond_demi_part):
    ''' 
    rni: revenu net imposable
    nb_parts: nombre de parts
    bareme: barème des seuils et taux par tranche
    plafond_demi_part: plafond de l'avantage lié au quotient familial par demi-part
    ''' 
    seuil = bareme["seuil"].values.copy()
    taux = bareme["taux"].values.copy()
    nb_parts_sans_enfants = 2
    impot_sans_plafond = calcul_impot_foyer_sans_plafond(rni=rni, nb_parts=nb_parts, seuil=seuil, taux=taux)
    impot_avec_plafond = calcul_impot_foyer_sans_plafond(rni=rni, nb_parts=nb_parts_sans_enfants, seuil=seuil,
                                                   taux=taux)
    impot_avec_plafond -= nb_parts_sans_enfants * (nb_parts - nb_parts_sans_enfants) * plafond_demi_part
    return max(impot_sans_plafond, impot_avec_plafond)


def calcul_impot_indiv_sans_plafond(rni_1, rni_2, nb_parts, seuil, taux):
    quotient_1 = rni_1 / nb_parts
    quotient_2 = rni_2 / nb_parts
    buckets = seuil.copy()
    buckets[1:] -= buckets[:-1]
    tranches_1, tranches_2 = fill_buckets([quotient_1, quotient_2], buckets)
    iisp_1 = np.sum(tranches_1 * taux / 100) * nb_parts
    iisp_2 = np.sum(tranches_2 * taux / 100) * nb_parts
    return (iisp_1, iisp_2)

def calcul_impot_indiv(rni_1, rni_2, nb_parts, bareme, plafond_demi_part):
    ''' 
    rni: revenu net imposable
    nb_parts: nombre de parts
    bareme: barème des seuils et taux par tranche
    plafond_demi_part: plafond de l'avantage lié au quotient familial par demi-part
    ''' 
    seuil = bareme["seuil"].values.copy()
    taux = bareme["taux"].values.copy()
    nb_parts_sans_enfants = 2
    iisp_1, iisp_2 = calcul_impot_indiv_sans_plafond(rni_1, rni_2, nb_parts, seuil, taux)
    iiap_1, iiap_2 = calcul_impot_indiv_sans_plafond(rni_1, rni_2, nb_parts_sans_enfants, seuil, taux)
    iiap_1, iiap_2 = subtract_d([iiap_1, iiap_2], 
                                nb_parts_sans_enfants * (nb_parts - nb_parts_sans_enfants) * plafond_demi_part, 
                                min_keep = [iisp_1, iisp_2])
    
    ii_1 = max(iisp_1, iiap_1)
    ii_2 = max(iisp_2, iiap_2)
    return (ii_1, ii_2)
