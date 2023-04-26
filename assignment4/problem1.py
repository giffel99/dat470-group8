from mrjob.job import MRJob
import math
import time
import numpy as np

centroids_in = np.Array([[301, 127],
                        [840, 506],
                        [839, 542],
                        [728, 394],
                        [307, 522]])

class SingleStepKMeans(MRJob):
    def nearestCentroid(datum, centroids):
    # norm(a-b) is Euclidean distance, matrix - vector computes difference
    # for all rows of matrix
        dist = np.linalg.norm(centroids - datum)
        return np.argmin(dist)

    def mapper(self, _, line):
        x, y = line.strip().split(' ')

        yield self.nearestCentroid((x,y), np.array(centroids_in)), (x, y, 1)

    def reducer(self, _, values):
        x_total, y_total, count = 0, 0, 0
        for x, y, n in values:
            x_total += x
            y_total += y
            count += n
        yield x_total/count, y_total/count


if __name__ == '__main__':
    SingleStepKMeans.run()