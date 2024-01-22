"""
Run clustering

Currently saves the best labels based on the inertia as silhouette score and calinski harabasz index are too slow
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
#from sklearn.metrics import silhouette_score, calinski_harabasz_score
import numpy as np
from dask_ml.cluster import KMeans
import dask.array as da
import pickle
import time 

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
    print('Reading in protein embeddings located at : ' + str(data))
    embeddings = pickle.load(open(data, 'rb'))

    # array to store data
    inertia = np.zeros(bootstraps)

    # store the best silhouette score and labels
    best_score = np.inf
    best_labels = None

    # compute the sample size - if its not specified we take the entire dataset
    subset = True
    if n_samples == 0:

        print('You have not specified a sample size for clustering. Using all data for clustering')
        n_samples = len(embeddings)
        subset =  False

    # loop through the bootstraps
    print(str(bootstraps) + ' boostraps have been specified. Looping ...')
    for b in range(bootstraps):

        # print an update
        print( '\t bootstrap: ' + str(b), flush = True)

        # get a subsample of the data
        if subset:
            print('\t generating subsample of size ' + str(n_samples), flush = True )
            idx = np.random.choice(list(embeddings.keys()), n_samples, replace=True)
            embedding_subset = np.array([embeddings[i] for i in idx], dtype=np.float32)
        else:
            print('\t transforming embeddings', flush = True)
            embedding_subset = np.array(list(embeddings.values()),  dtype=np.float32)

        # turn array into a dask array
        embedding_dask = da.from_array(embedding_subset, chunks=(batch_size, 1280))

        # run through the clustering
        print('\t running kmeans for k=' + str(k_clusters), flush = True)
        start = time.time() 
        kmeans = KMeans(n_clusters=k_clusters, random_state=42) #TODO see if there are other parameters that should be included here
        kmeans.fit(embedding_dask)
        kmeans_labels = kmeans.labels_
        end = time.time() 
        print('\t clustering completed in ' + str(end - start) + ' seconds')

        # get silhouette and ch score score
        print('\t computing clustering scores', flush = True)
        #s_score = silhouette_score(embedding_subset, kmeans_labels, metric = 'cosine')
        #ch_score = calinski_harabasz_score(embedding_subset, kmeans_labels, metri = 'cosine')

        # store the scores
        inertia[b] = kmeans.inertia_

        # if the clustering is better update the saved labels
        print('\t updating labels\n', flush = True)
        if kmeans.inertia_ < best_score:

            best_labels = dict(zip(idx, list(np.asarray(kmeans_labels))))
            best_score = kmeans.inertia_

    # form a dataframe for these metrics and save it
    print('\n DONE\n saving output to ' + out, flush = True)
    scores = pd.DataFrame({"inertia": inertia}) 

    # save the dataframe
    scores.to_csv(out + '_scores.tsv')

    # save the best labels
    pickle.dump(best_labels, open(out + '_bestlabels.pkl', 'wb'))

if __name__ == "__main__":
    main()



