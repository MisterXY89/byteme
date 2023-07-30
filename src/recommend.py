from bayespy.nodes import Categorical, Dirichlet, Beta, Mixture, Bernoulli
from bayespy.inference import VB
import bayespy.plot as bpplt
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np


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
        self._df = pd.read_csv(dataPATH)
        self.model = {}
        self._method_cols = (str(x) for x in np.arange(22, 32, 1))
        self._research_cols = (str(x) for x in np.arange(2, 22, 1))

    def fit(self, cluster_size: int = 6):
        """_summary_"""
        self.model["research"] = self._BernoulliMixture(
            self._df.loc[:, self._research_cols].astype("int").values,
            cluster_size=cluster_size,
        )

        self.model["methods"] = self._BernoulliMixture(
            self._df.loc[:, self._method_cols].astype("int").values,
            cluster_size=cluster_size,
        )
        # params = self.model["research"]["candidate group assignment probs"].get_parameters()[0].reshape(35,5)

    def _BernoulliMixture(self, x, cluster_size):
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

        # conjugate Beta priors for Bernoulli Distribution
        P = Beta([0.5, 0.5], plates=(D, cluster_size), name="P")

        # uninformative Dirichlet prior for Multinomial Discrete Variables
        R = Dirichlet(cluster_size * [1e-5], name="R")

        # categorical distribution for the group assignments
        Z = Categorical(R, plates=(N, 1), name="Z")

        # Constructing Model with Bayes Theorem
        # Bernoulli mixture likelihood with beta prior
        X = Mixture(Z, Bernoulli, P)

        # Bayesian Inference: Expectation Maximization
        Q = VB(Z, R, X, P)

        # random initialization for the group probability patterns
        P.initialize_from_random()

        # fit data
        X.observe(x)

        # run inference
        Q.update(repeat=1000, verbose=False)

        result = dict(
            {
                "candidate group assignment probs": Z,  # .get_parameters()[0].reshape(N, cluster_size),
                "group assignment probs": R,  # .get_parameters()[0],
                "group pattern probs": P,  # .get_parameters()[0],
                "answers": X,
            }
        )

        return result

    def plot(self):
        # plot effective number of found groups
        bpplt.hinton(self.R)

        # plot group for each of the participants
        bpplt.hinton(self.Z)
        plt.show()

    def recommend_similar(round: str):
        if round == "similar":
            raise NotImplementedError()
        if round == "different":
            raise NotImplementedError()
        if round == "random":
            raise NotImplementedError()


if __name__ == "__main__":
    model = Recommender(sim=True)
    model.fit()
    model.plot()
