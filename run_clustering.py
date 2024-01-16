"""
Run clustering
"""

__author__ = "Susanna Grigson"
__maintainer__ = "Susanna Grigson"
__license__ = "MIT"
__version__ = "0"
__email__ = "susie.grigson@gmail.com"
__status__ = "development"


# imports
import pandas as pd
import click
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import pickle

@click.command()
@click.option(
    "-n",
    "--n_samples",
    default=0,
    show_default=True,
    help='number of samples to include ber bootstrap'
)
@click.option(
    "-k",
    "--k_clusters",
    default=30,
    show_default=True,
    help="number of clusters K to test"
)
@click.option(
    "-b",
    "--bootstraps",
    default=50,
    show_default=True,
    help="number of bootstraps to perform for each k"
)
@click.option(
    "-batch_size",
    "--batch_size",
    default=1028,
    show_default=True,
    help="batch size for KMeans clustering"
)
@click.option(
    "-d",
    "--data",
    type=click.STRING,
    default="",
    help = "path to pickle file of data"
)
@click.option(
    "-o",
    "--out",
    type=click.STRING,
    default="",
    help = "name of output dataframe"
)

def main(n_samples, k_clusters, bootstraps, data, batch_size, out):

    # read in the data
    embeddings = pickle.load(open(data, 'rb'))
    #print(list(embeddings.values())[:4]) 

    # array to store data
    inertia = np.zeros(bootstraps)
    silhouette = np.zeros(bootstraps)
    ch = np.zeros(bootstraps)

    # loop through the bootstraps
    for b in range(bootstraps):

        # get a subsample of the data
        idx = np.random.randint(0, len(embeddings), n_samples)
        embedding_subset = np.array(list(embeddings.values()))[idx]

        # run through the clustering
        kmeans = MiniBatchKMeans(n_clusters=k_clusters, random_state=42, batch_size=batch_size)
        kmeans.fit(embedding_subset)
        kmeans_labels = kmeans.fit_predict(embedding_subset)

        # get silhouette and ch score score
        s_score = silhouette_score(embedding_subset, kmeans_labels)
        ch_score = calinski_harabasz_score(embedding_subset, kmeans_labels)

        # store the scores
        inertia[b] = kmeans.inertia_
        silhouette[b] = s_score
        ch[b] = ch_score

    # form a dataframe for these metrics and save it
    scores = pd.DataFrame({"inertia": inertia, "silhouette": silhouette, "calinski_harabasz": ch})

    # save the dataframe
    scores.to_csv(out)

if __name__ == "__main__":
    main()



