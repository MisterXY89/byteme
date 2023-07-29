from bayespy.nodes import Categorical, Dirichlet, Beta, Mixture, Bernoulli
from bayespy.inference import VB
import bayespy.plot as bpplt
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numbers as np


class Recommender:
    """Class implementing a cluster algorithm
    in an unsupervised setting.
    """

    def __init__(self, sim: bool = False):
        path = Path(__file__).parent.parent.joinpath("data")
        if sim:
            dataPATH = path / "dummy.csv"
        else:
            dataPATH = path / "data.csv"
        self.df = pd.read_csv(dataPATH)

    def fit(self):
        """_summary_"""
        self.Z, self.R = self.BernoulliMixture(self.df.iloc[:, 7:].astype("int").values)

    def BernoulliMixture(self, x, cluster: int = 10):
        """Here, Z defines the group assignments and P the answering probability patterns for each group.
        Note how the plates of the nodes are matched: Z has plates (N,1) and P has plates (D,K), but in
        the mixture node the last plate axis of P is discarded and thus the node broadcasts plates (N,1)
        and (D,) resulting in plates (N,D) for X.

        Args:
            x (_type_): Input Data matrix of integers
            cluster (int, optional): Number of Clusters. Defaults to 10.

        Returns:
            _type_: _description_
        """

        N = x.shape[0]
        D = x.shape[1]

        # uninformative Dirichlet prior
        R = Dirichlet(cluster * [1e-5], name="R")

        # categorical distribution for the group assignments
        Z = Categorical(R, plates=(N, 1), name="Z")

        # beta priors for probability of a yes answer
        P = Beta([0.5, 0.5], plates=(D, cluster), name="P")

        # The answers of the candidates are modelled with the Bernoulli distribution:
        X = Mixture(Z, Bernoulli, P)

        Q = VB(Z, R, X, P)

        # random initialization for the group probability patterns
        P.initialize_from_random()

        # fit data
        X.observe(x)

        # run inference
        Q.update(repeat=1000, verbose=False)
        return Z, R

    def plot(self):
        # plot effective number of found groups
        bpplt.hinton(self.R)

        # plot group for each of the participants
        bpplt.hinton(self.Z)
        plt.show()


if __name__ == "__main__":
    model = Recommender(sim=True)
    model.fit()
    model.plot()
