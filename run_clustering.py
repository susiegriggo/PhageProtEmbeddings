"""
Run clustering

Currently saves the best labels based on the silhouette score. May change to use whichever score is best
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
    print('reading in the embeddings')
    embeddings = pickle.load(open(data, 'rb'))
    #print(list(embeddings.values())[:4]) 

    # array to store data
    print('preparing arrays')
    inertia = np.zeros(bootstraps)
    #silhouette = np.zeros(bootstraps)
    #ch = np.zeros(bootstraps)


    # store the best silhouette score and labels
    best_score = np.inf
    best_labels = None

    # loop through the bootstraps
    print('Running bootstraps')
    for b in range(bootstraps):

        # print an update
        print(b, flush = True)

        # get a subsample of the data
        print('generate subsample index', flush = True )
        #idx = np.random.randint(0, len(embeddings), n_samples)
        #embedding_subset = np.array(list(embeddings.values()))[idx].astype(np.float32)
        #embedding_subset = [list(embeddings.values())[i] for i in idx]
        #embedding_subset = np.array(embedding_subset).astype(np.float32)
        idx = np.random.choice(list(embeddings.keys()), n_samples, replace=True)
        print('generate subsample', flush = True )
        embedding_subset = np.array([embeddings[i] for i in idx], dtype=np.float32)

        # turn array into a dask array
        print('make dask array', flush = True)
        embedding_dask = da.from_array(embedding_subset, chunks=(batch_size, 1280))

        # run through the clustering
        print('run kmeans', flush = True)
        start = time.time() 
        kmeans = KMeans(n_clusters=k_clusters, random_state=42) #TODO see if there are other parameters that should be included here
        kmeans.fit(embedding_dask)
        kmeans_labels = kmeans.labels_
        end = time.time() 
        print(end - start)

        # get silhouette and ch score score
        print('compute scores', flush = True)
        #start = time.time()
        #s_score = silhouette_score(embedding_subset, kmeans_labels, metric = 'cosine')
        #ch_score = calinski_harabasz_score(embedding_subset, kmeans_labels, metri = 'cosine')

        # store the scores
        inertia[b] = kmeans.inertia_
        #silhouette[b] = s_score
        #ch[b] = ch_score
        #end = time.time() 
        #print(end - start)

        # if the clustering is better update the saved labels
        print('update labels', flush = True)
        if kmeans.inertia_ < best_score:

            #best_labels = dict(zip([list(embeddings.keys())[i] for i in idx], list(np.asarray(kmeans_labels)))) 
            best_labels = dict(zip(idx, list(np.asarray(kmeans_labels))))
            #best_labels = best_labels = dict(zip(np.random.choice(list(embeddings.keys()), n_samples, replace=False), kmeans_labels))
            best_score = kmeans.inertia_

    # form a dataframe for these metrics and save it
    print('save scores to file', flush = True)
    #scores = pd.DataFrame({"inertia": inertia, "silhouette": silhouette, "calinski_harabasz": ch})
    scores = pd.DataFrame({"inertia": inertia}) 

    # save the dataframe
    scores.to_csv(out + '_scores.tsv')

    # save the best labels
    pickle.dump(best_labels, open(out + '_bestlabels.pkl', 'wb'))


if __name__ == "__main__":
    main()



