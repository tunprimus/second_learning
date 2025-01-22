import numpy as np

def get_arithmetic_mean(df):
    return np.mean(df)

def get_geometric_mean(df):
    return np.exp(np.mean(np.log(df)))
