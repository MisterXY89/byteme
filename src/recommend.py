from bayespy.nodes import Categorical, Dirichlet, Beta, Mixture, Bernoulli
from bayespy.inference import VB
import bayespy.plot as bpplt
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches
import random

try:
    from simData import generate
except Exception as e:
    from .simData import generate


class Recommender:
    """Class implementing a cluster algorithm
    in an unsupervised setting.
    """

    def __init__(self, sim: bool = False):
        dataPATH = Path(__file__).parent.parent.joinpath("data").joinpath("data.csv")
        if sim:
            self._df = generate(30, 55, 20)
        else:
            self._df = pd.read_csv(dataPATH, sep=";")
        self._effort_col = "effort"
        self._pref_col = "preference"
        self._method_cols = [
            col for col in self._df.columns if col.startswith("METHOD")
        ]
        self._research_cols = [
            col for col in self._df.columns if col.startswith("RESEARCH")
        ]
        self._df["preference_weighted"] = self._normalise(
            self._df[self._pref_col], max_val=0.7, min_val=0.3
        )
        self._df["effort_weighted"] = self._normalise(
            self._df[self._effort_col], max_val=0.6, min_val=0.4
        )

    def _normalise(self, col, max_val: int, min_val: int):
        return (col - min(col)) / (max(col) - min(col)) * (max_val - min_val) + min_val

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
        xrange = np.arange(0, self._research.shape[1], 1)
        labels = [str(x + 1) for x in range(self._methods.shape[1])]

        with plt.style.context("seaborn-whitegrid"):
            fig, ax = plt.subplots(
                1, 2, constrained_layout=True, figsize=(10, 3), sharey=True
            )
            for xe, ye in zip(xrange, self._methods.T):
                x = np.linspace(xe - 0.2, xe - 0.05, len(ye))
                ax[0].scatter(x, ye, c="green")
            for xe, ye in zip(xrange, self._research.T):
                x = np.linspace(xe + 0.05, xe + 0.2, len(ye))
                ax[0].scatter(x, ye, c="orange")
            for xe, ye in zip(xrange, self._weighted.T):
                x = np.linspace(xe - 0.2, xe + 0.2, len(ye))
                ax[1].scatter(x, ye, c="gray")

            orange_patch = mpatches.Patch(color="orange", label="Research Clusters")
            green_patch = mpatches.Patch(color="green", label="Method Clusters")

            ax[0].legend(handles=[green_patch, orange_patch])

            ax[0].set_xticks(xrange)
            ax[1].set_xticks(xrange)
            ax[0].set_xticklabels(labels)
            ax[1].set_xticklabels(labels)
            ax[0].set_title("Comparison of Cluster Output for both topics")
            ax[1].set_title("Comparison of weighted Cluster Output")
            fig.supylabel("Probability of belonging to Cluster")
            fig.supxlabel("Cluster")
            plt.show()

    def explainProbabilities(self, person: int):
        ticks = np.arange(0, self._methods.shape[1], 1)
        labels = [str(x + 1) for x in range(self._methods.shape[1])]

        with plt.style.context("seaborn-whitegrid"):
            fig, ax = plt.subplots(
                1, 2, constrained_layout=True, figsize=(10, 3), sharey=True
            )
            ax[0].scatter(
                ticks - 0.1,
                self._methods[person, :],
                label="Method Cluster",
                color="green",
            )
            ax[0].scatter(
                ticks + 0.1,
                self._research[person, :],
                label="Research Group",
                color="orange",
            )
            ax[1].scatter(ticks, self._weighted[person, :], color="gray")
            ax[0].legend()
            ax[0].set_title("Comparison of Cluster Output for both topics")

            ax[0].set_xticks(ticks)
            ax[1].set_xticks(ticks)
            ax[0].set_xticklabels(labels)
            ax[1].set_xticklabels(labels)
            ax[1].set_title("Comparison of weighted Cluster Output")
            fig.supylabel("Probability of belonging to Cluster")
            fig.supxlabel("Cluster")
            plt.show()

    def plotEffort(self):
        with plt.style.context("seaborn-whitegrid"):
            fig, ax = plt.subplot_mosaic(
                "B", tight_layout=True, figsize=(3, 3), sharey=True
            )
            ax["B"].boxplot(
                self._df.loc[:, self._effort_col],
                notch=True,
                flierprops=dict(markerfacecolor="b", marker="D"),
            )
            # ax["B"].hlines(y=[np.quantile()])

            ax["B"].set_xticklabels("")
            ax["B"].set_ylabel("Willingness to put in effort")
            x = np.linspace(0.9, 1.1, len(self._df))
            ax["B"].scatter(x, self._df.loc[:, self._effort_col], alpha=0.2, c="gray")
            plt.show()

    def recommend(self, kind: str, group_size: int) -> dict:
        if kind == "similar":
            recommendations = self._proposeSimilar(max_size=7, min_size=3)

        if kind == "motivation":
            recommendations = self._proposeMotivation(group_size)

        if kind == "random":
            recommendations = self._proposeRandom(group_size)

        return recommendations

    def _proposeRandom(self, group_size: int = 6) -> dict:
        groups = {}
        n = self._weighted.shape[0]
        mylist = np.arange(0, n, 1)
        random.shuffle(mylist)
        return {
            f"Group {idx+1}": mylist[i : i + group_size]
            for idx, i in enumerate(range(0, len(mylist), group_size))
        }

    def _proposeSimilar(
        self, max_size: int = 7, min_size: int = 3, group_size: int = 6
    ) -> dict:
        weighted_df = pd.DataFrame(self._weighted)
        recommendations = {f"Group {i}": [] for i in range(1, weighted_df.shape[1] + 1)}

        for idx, participant in weighted_df.iterrows():
            recommendations[f"Group {participant.idxmax()+1}"].append(
                {"Person": idx, "Prob": participant.max()}
            )

        for k, v in recommendations.items():
            newlist = sorted(v, key=lambda d: d["Prob"], reverse=True)
            recommendations[k] = [v["Person"] for v in newlist]

        big = {
            k: len(v) - max_size
            for k, v in recommendations.items()
            if len(v) > max_size
        }
        small = {
            k: min_size - len(v)
            for k, v in recommendations.items()
            if len(v) < min_size
        }

        while len(small) > 0:
            mmax = max(big, key=big.get)
            mmin = min(small, key=small.get)
            for participant in range(big[mmax]):
                part = recommendations[mmax].pop()
                recommendations[mmin].append(part)
                big = {
                    k: len(v) - max_size
                    for k, v in recommendations.items()
                    if len(v) > max_size
                }
                small = {
                    k: len(v) - min_size
                    for k, v in recommendations.items()
                    if len(v) < min_size
                }
        return recommendations

    def _proposeMotivation(self, group_size: int = 5) -> dict:
        data = self._df.copy()
        data = pd.qcut(data.effort, q=group_size).reset_index()
        groups = {}
        for idx, group in enumerate(data.effort.unique()):
            groups[f"Group {idx+1}"] = data.loc[data.effort == group, "index"].values

        return groups


if __name__ == "__main__":
    model = Recommender(sim=True)
    model.fit()
    model.plot()
