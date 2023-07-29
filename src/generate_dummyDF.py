import numpy as np
import pandas as pd
import random
from pathlib import Path

PATH = Path(__file__).parent.parent.joinpath("data")


def generate(n: int, research_size: int, method_size: int):
    weights = np.random.random((n, 2))
    research = np.random.randint(0, 2, (n, research_size))
    methods = np.random.randint(0, 2, (n, method_size))

    data = np.hstack((weights, research, methods))
    df = pd.DataFrame(data)
    df.to_csv(PATH / "dummy.csv", index=True)


if __name__ == "__main__":
    generate(35, 20, 10)
