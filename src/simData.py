import numpy as np
import pandas as pd
import random
from pathlib import Path
from bayespy.utils import random

PATH = Path(__file__).parent.parent.joinpath("data")


def generate(n: int, research_size: int, method_size: int) -> pd.DataFrame:
    """
    Generates dummy data that can be used to test the model.
    For later pupuses, it will be important that the respective column
    names of the data and the model will match!

    Args:
        n (int): number of participants, e.g. rows of data
        research_size (int): number of research topics
        method_size (int): number of method topics

    Returns:
        pd.DataFrame: simulated data
    """
    # generate (n x 2) matrix representing desired effort and preference
    weights = np.random.random((n, 2))
    z = random.categorical([1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5], size=n)

    # generate research topic preferences
    r0 = np.random.choice([0.7, 0.3], size=research_size)
    r1 = np.random.choice([0.7, 0.3], size=research_size)
    r2 = np.random.choice([0.7, 0.3], size=research_size)
    r3 = np.random.choice([0.7, 0.3], size=research_size)
    r4 = np.random.choice([0.7, 0.3], size=research_size)
    r = np.array([r0, r1, r2, r3, r4])
    research = random.bernoulli(r[z])

    # generate method preferences
    m0 = np.random.choice([0.7, 0.3], size=method_size)
    m1 = np.random.choice([0.7, 0.3], size=method_size)
    m2 = np.random.choice([0.7, 0.3], size=method_size)
    m3 = np.random.choice([0.7, 0.3], size=method_size)
    m4 = np.random.choice([0.7, 0.3], size=method_size)
    m = np.array([m0, m1, m2, m3, m4])
    methods = random.bernoulli(m[z])

    # store all generated instances in DataFrame
    data = np.hstack((weights, research, methods))
    df = pd.DataFrame(data)
    effort_col = "effort"
    pref_col = "preference"
    research_cols = [f"RESEARCH{x}" for x in np.arange(0, research.shape[1], 1)]
    method_cols = [f"METHOD{x}" for x in np.arange(0, methods.shape[1], 1)]
    cols = np.hstack([effort_col, pref_col, research_cols, method_cols])
    df.columns = cols

    return df


if __name__ == "__main__":
    generate(35, 20, 10)
