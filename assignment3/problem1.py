#!/usr/bin/env python3
#
# File: kmeans.py
# Author: Originally by Alexander Schliep (alexander@schlieplab.org), updated by Matti Karppa (karppa@chalmers.se)
# 
# Requires scikit-learn (sklearn), numpy, matplotlib
#

import logging
import argparse
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import time

def generateData(n, c):
    """generates Gaussian blobs, 
    see https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_blobs.html
    """
    logging.info(f"Generating {n} samples in {c} classes")
    X, y = make_blobs(n_samples=n, centers = c, cluster_std=1.7, shuffle=False,
                      random_state = 2122)
    return X


def nearestCentroid(data, centroids):
    """computes the distance of the data vector to the centroids and returns 
    the closest one as an (index,distance) pair
    """
    # norm(a-b) is Euclidean distance, matrix - vector computes difference
    # for all rows of matrix
    cluster_sizes = np.zeros(len(centroids))
    clusters = np.zeros(len(data))
    for i in range(len(data)):
            dist = np.linalg.norm(centroids - data[i], axis=1)
            cluster = np.argmin(dist)
            clusters[i] = int(cluster)
            cluster_sizes[cluster] += 1
   

    return (clusters, cluster_sizes)

def get_mean_point(c_split, data_split, centroids):
    for i in range(len(c_split)):
        centroids[c_split[i]] += data_split[i]        
    return centroids



def kmeans(k, data,num_workers, nr_iter = 100):
    """computes k-means clustering by fitting k clusters into data
    a fixed number of iterations (nr_iter) is used
    you should modify this routine for making use of multiple threads
    """
    N = len(data)

    # Choose k random data points as centroids
    centroids = data[np.random.choice(np.array(range(N)),size=k,replace=False)]
    logging.debug("Initial centroids\n", centroids)

    # The cluster index: c[i] = j indicates that i-th datum is in j-th cluster

    for j in range(nr_iter):
        logging.debug("=== Iteration %d ===" % (j+1))

        # Assign data points to nearest centroid

        data_split = np.array_split(data,num_workers)
        with mp.Pool(num_workers) as p:
            result = p.starmap(nearestCentroid, [(data_split[i], centroids) for i in range(num_workers)]) 
        c = []
        cluster_sizes = np.zeros(len(centroids))
        for ret_c,ret_c_s in result:
            c = np.concatenate((c, ret_c))
            cluster_sizes += ret_c_s
        c = [int(item) for item in c]
        # Recompute centroids
        centroids = np.zeros((k,2)) # This fixes the dimension to 2
        c_split = np.array_split(c,num_workers)

        with mp.Pool(num_workers) as p: 
            result = p.starmap(get_mean_point, [(c_split[i], data_split[i], centroids) for i in range(num_workers)])
        for res in result:
            centroids += res
        centroids = centroids / cluster_sizes.reshape(-1,1)
        
        logging.debug(cluster_sizes)
        logging.debug(c)
        logging.debug(centroids)
    
    return c


def computeClustering(args):
    if args.verbose:
        logging.basicConfig(format='# %(message)s',level=logging.INFO)
    if args.debug: 
        logging.basicConfig(format='# %(message)s',level=logging.DEBUG)
    logging.info(args.workers)
    X = generateData(args.samples, args.classes)

    start_time = time.time()
    #
    # Modify kmeans code to use args.worker parallel threads
    assignment = kmeans(args.k_clusters, X,args.workers, nr_iter = args.iterations)
    #
    #
    end_time = time.time()
    logging.info("Clustering complete in %3.2f [s]" % (end_time - start_time))

    if args.plot: # Assuming 2D data
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(X[:, 0], X[:, 1], c=assignment, alpha=0.2)
        plt.title("k-means result")
        #plt.show()        
        fig.savefig(args.plot)
        plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute a k-means clustering.',
        epilog = 'Example: kmeans.py -v -k 4 --samples 10000 --classes 4 --plot result.png'
    )
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes to use (NOT IMPLEMENTED)')
    parser.add_argument('--k_clusters', '-k',
                        default='3',
                        type = int,
                        help='Number of clusters')
    parser.add_argument('--iterations', '-i',
                        default='100',
                        type = int,
                        help='Number of iterations in k-means')
    parser.add_argument('--samples', '-s',
                        default='10000',
                        type = int,
                        help='Number of samples to generate as input')
    parser.add_argument('--classes', '-c',
                        default='3',
                        type = int,
                        help='Number of classes to generate samples from')   
    parser.add_argument('--plot', '-p',
                        type = str,
                        help='Filename to plot the final result')   
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Print verbose diagnostic output')
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        help='Print debugging output')
    args = parser.parse_args()
    computeClustering(args)

