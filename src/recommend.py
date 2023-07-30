from bayespy.nodes import Categorical, Dirichlet, Beta, Mixture, Bernoulli
from bayespy.inference import VB
import bayespy.plot as bpplt
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np

try:
    from src.simData import generate
except:
    from .simData import generate


class Recommender:
    """Class implementing a cluster algorithm
    in an unsupervised setting.
    """

    def __init__(self, sim: bool = False):
        dataPATH = Path(__file__).parent.parent.joinpath("data").joinpath("data.csv")
        if sim:
            self._df = generate(30, 25, 17)
        else:
            self._df = pd.read_csv(dataPATH)
        self._effort_col = "effort"
        self._pref_col = "preference"
        self._method_cols = [
            col for col in self._df.columns if col.startswith("Method")
        ]
        self._research_cols = [
            col for col in self._df.columns if col.startswith("Research")
        ]
        self._process()

    def _process(self, range: list = (0.3, 0.7)) -> None:
        pref = self._df.loc[:, self._pref_col]
        pref_weighted = (pref - min(pref)) / (max(pref) - min(pref)) * (
            range[1] - range[0]
        ) + range[0]
        self._df["preference_weighted"] = pref_weighted

    def fit(self, cluster_size: int = 6, weight: bool = True) -> dict:
        col = self._pref_col
        if weight:
            col = "preference_weighted"
        weights = self._df[col]

        research = self._BernoulliMixture(
            self._df.loc[:, self._research_cols].astype("int").values,
            cluster_size=cluster_size,
        )

        methods = self._BernoulliMixture(
            self._df.loc[:, self._method_cols].astype("int").values,
            cluster_size=cluster_size,
        )

        weighted = np.empty(methods.shape)
        for person in range(methods.shape[0]):
            weighted[person, :] = research[person, :] * weights[person] + methods[
                person, :
            ] * (1 - weights[person])
        self._methods = methods
        self._research = research
        self._weighted = weighted

        return dict({"method": methods, "research": research, "weighted": weighted})

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

        # result = dict(
        #     {
        #         # Only the candidate vaues are relevant for now
        #         "candidate probs": Z._message_to_child()[0].reshape(N, cluster_size),
        #         "group assignment probs": R,
        #         "group pattern probs": P,
        #         "answers": X,
        #     }
        # )
        result = Z._message_to_child()[0].reshape(N, cluster_size)

        return result

    def plotProbabilites(self):
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
