import numpy as np
import pandas as pd
from gen_surv.validate import validate_gen_thmm_inputs
from gen_surv.censoring import runifcens, rexpocens

def calculate_transitions(z1: float, cens_par: float, beta: list, rate: list, rfunc) -> dict:
    """
    Calculate transition and censoring times for THMM.

    Parameters:
    - z1 (float): Covariate value.
    - cens_par (float): Censoring parameter.
    - beta (list of float): Coefficients for rate modification (length 3).
    - rate (list of float): Base rates (length 3).
    - rfunc (callable): Censoring function, e.g. runifcens or rexpocens.

    Returns:
    - dict with keys 'c', 't12', 't13', 't23'
    """
    c = rfunc(1, cens_par)[0]
    rate12 = rate[0] * np.exp(beta[0] * z1)
    rate13 = rate[1] * np.exp(beta[1] * z1)
    rate23 = rate[2] * np.exp(beta[2] * z1)

    t12 = np.random.exponential(scale=1 / rate12)
    t13 = np.random.exponential(scale=1 / rate13)
    t23 = np.random.exponential(scale=1 / rate23)

    return {"c": c, "t12": t12, "t13": t13, "t23": t23}


def gen_thmm(n, model_cens, cens_par, beta, covar, rate):
    """
    Generate THMM (Time-Homogeneous Markov Model) survival data.

    Parameters:
    - n (int): Number of individuals.
    - model_cens (str): "uniform" or "exponential".
    - cens_par (float): Censoring parameter.
    - beta (list): Length-3 regression coefficients.
    - covar (float): Covariate upper bound.
    - rate (list): Length-3 transition rates.

    Returns:
    - pd.DataFrame: Columns = ["id", "time", "state", "covariate"]
    """
    validate_gen_thmm_inputs(n, model_cens, cens_par, beta, covar, rate)
    rfunc = runifcens if model_cens == "uniform" else rexpocens
    records = []

    for k in range(n):
        z1 = np.random.uniform(0, covar)
        trans = calculate_transitions(z1, cens_par, beta, rate, rfunc)
        t12, t13, c = trans["t12"], trans["t13"], trans["c"]

        if min(t12, t13) < c:
            if t12 <= t13:
                time, state = t12, 2
            else:
                time, state = t13, 3
        else:
            time, state = c, 1  # censored

        records.append([k + 1, time, state, z1])

    return pd.DataFrame(records, columns=["id", "time", "state", "covariate"])
