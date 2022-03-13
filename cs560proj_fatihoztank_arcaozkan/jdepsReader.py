import json
import re
import os
import subprocess

from GraphClass import DependencyGraph
from elasticsearch_test import getTagName
from glob import glob
from karateclub import Graph2Vec, FeatherGraph

import numpy as np

from sklearn.cluster import DBSCAN, OPTICS
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler 


graphs = []
classname = "org.elasticsearch.action.admin.indices.validate.query"
logFiles = glob("elasticsearchReports/*")
for log in logFiles:
    graph = DependencyGraph(log,className=classname, 
        depth=3)
    graphs.append(graph.graph)

model = FeatherGraph()
model.fit(graphs)

graphlist = (model.get_embedding())
for listt in graphlist:
    print(len(listt), listt[:10])


clust = OPTICS().fit(graphlist)
labels = clust.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)

cluster_dict = {}
for i in range(55):
    if labels[i] in cluster_dict:
        cluster_dict[labels[i]].append(getTagName(logFiles[i][-10:]))
    else:
        cluster_dict[labels[i]] = ([getTagName(logFiles[i][-10:])])


for key, value in cluster_dict.items():
    print(key, ' : ', value)
