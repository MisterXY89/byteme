import numpy as np
import pandas as pd
import random
from pathlib import Path
from bayespy.utils import random

PATH = Path(__file__).parent.parent.joinpath("data")


def generate(n: int, research_size: int, method_size: int):
    weights = np.random.random((n, 2))
    z = random.categorical([1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5], size=n)

    r0 = np.random.choice([0.9, 0.1], size=research_size)
    r1 = np.random.choice([0.9, 0.1], size=research_size)
    r2 = np.random.choice([0.9, 0.1], size=research_size)
    r3 = np.random.choice([0.9, 0.1], size=research_size)
    r4 = np.random.choice([0.9, 0.1], size=research_size)
    r = np.array([r0, r1, r2, r3, r4])
    research = random.bernoulli(r[z])

    m0 = np.random.choice([0.7, 0.3], size=method_size)
    m1 = np.random.choice([0.7, 0.3], size=method_size)
    m2 = np.random.choice([0.7, 0.3], size=method_size)
    m3 = np.random.choice([0.7, 0.3], size=method_size)
    m4 = np.random.choice([0.7, 0.3], size=method_size)
    m = np.array([m0, m1, m2, m3, m4])
    methods = random.bernoulli(m[z])

    data = np.hstack((weights, research, methods))
    df = pd.DataFrame(data)
    df.to_csv(PATH / "dummy.csv", index=False)


if __name__ == "__main__":
    generate(35, 20, 10)
