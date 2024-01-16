"""
Script for filtering the prophage embeddings to include only proteins from representative clusters
"""
#imports
import glob
import pandas as pd
import pickle

# read in the clustering file
clusters = pd.read_csv('imgvr_clusters.csv')
# read in the embedding parts
parts = glob.glob('glm_IMGVR4_s15_phrogs/*')

# randomly select one sequence from each cluster at ANI70
clusters = clusters.sample(frac=1.0, random_state=42) # shuffle the rows
clusters_subset = clusters.drop_duplicates(subset='ANI_70') # get a single sequence from each cluster only
include_subset = clusters['contig_id'].values

# intialise dictionaries
embs_dict = dict()
ogg_dict = dict()

# loop through parts
for p in parts:
    # show update with how many parts have run through
    print(p)

    # read in the separate parts
    embs = pickle.load(open(p + "/glm_embs.pkl", "rb"))
    ogg = pickle.load(open(p + "/ogg_assignment.pkl", "rb"))

    # get the parts included in the clustering
    embs_df = pd.DataFrame.from_dict(embs).T
    embs_df['contig'] = [i[:-4] for i in embs_df.index]
    embs_df_include = embs_df[embs_df['contig'].isin(include_subset)].drop('contig', axis=1)
    embs_dict_include = dict(zip(embs_df_include.index, embs_df_include.values))

    # made dictionary with the relevant oggs only
    ogg_include = [ogg.get(i) for i in list(embs_dict_include.keys())]
    ogg_dict_include = dict(zip(embs_dict_include, ogg_include))

    ## merge the parts together
    embs_dict.update(embs_dict_include)
    ogg_dict.update(ogg_dict_include)

# save the dictionary to a file
with open('glm_IMGVR4_s15_phrogs_ANI70_proteins_embs.pkl', 'wb') as file:
    pickle.dump(embs_dict, file)

with open('glm_IMGVR4_s15_phrogs_ANI70_proteins_ogg_assignment.pkl', 'wb') as file:
    pickle.dump(ogg_dict, file)
