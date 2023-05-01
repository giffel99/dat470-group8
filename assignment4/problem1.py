from mrjob.job import MRJob
from mrjob.step import MRStep
import math
import time


class SingleStepKMeans(MRJob):

    def configure_args(self):
        super(SingleStepKMeans, self).configure_args()
        self.add_file_arg('--centroids', default='/home/2023/felhja/dat470-group8/assignment4/centroids_in.txt', help='Path to the centroids file')

    def mapper_init(self):
        self.centroids = []
        with open(self.options.centroids, 'r') as f:
            for line in f:
                centroid_x, centroid_y = map(float, line.strip().split(','))
                self.centroids.append([centroid_x, centroid_y])

    def mapper(self, _, line):
        data_x, data_y = map(float, line.strip().split(','))
        current_index = 0
        min_dist = float('inf')
        min_dist_index = 0

        for centroid_x, centroid_y in self.centroids:
            delta_x = centroid_x - data_x
            delta_y = centroid_y - data_y
            dist = (math.sqrt(delta_x ** 2 + delta_y ** 2))  
            if dist < min_dist:
                min_dist = dist
                min_dist_index = current_index
            current_index += 1
        
        yield min_dist_index, (data_x, data_y, 1)

    def reducer(self, index, values):
        x_total, y_total, count = 0, 0, 0
        data_points = []
        
        for x, y, n in values:
            x_total += x
            y_total += y
            count += n
            data_points.append((x, y))
        
        centroid_coordinates = (x_total / count, y_total / count)
        yield f"Centroid {index} has coordinates:", centroid_coordinates
       
        for x, y in data_points:
            yield index, (x, y)


if __name__ == '__main__':
    SingleStepKMeans.run()