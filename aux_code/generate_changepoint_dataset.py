"""
Generates a dataset with a changepoint
"""
import numpy as np
import pandas as pd

def gen_changepoint_dataset(mu0, sigma0, n0, mu1, sigma1, n1, seed=2):
    """
    :param mu0: mean of the first chunk of the dataset
    :param sigma0: standard deviation of the first chunk of the dataset
    :param n0: size of the first chunk of the dataset
    :param mu1: mean of the second chunk of the dataset
    :param sigma1: standard deviation of the second chunk of the dataset
    :param n1: size of the second chunk of the dataset
    :param seed: random seed
    :return: Dataset of size n0+n1 with a changepoint
    """
    sample0 = np.random.normal(mu0, sigma0, n0)
    sample1 = np.random.normal(mu1, sigma1, n1)
    return np.concatenate([sample0, sample1])

if __name__=='__main__':
    mu0 = 105
    sigma0 = 1.5
    n0 = 60
    mu1 = 108
    sigma1 = 1.5
    n1 = 40
    output_file = '../data/changepoint.csv'
    X = gen_changepoint_dataset(mu0, sigma0, n0, mu1, sigma1, n1)
    df = pd.DataFrame({'Measure': X})
    df.to_csv(output_file, index=None)
