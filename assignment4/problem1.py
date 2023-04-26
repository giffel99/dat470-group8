from mrjob.job import MRJob
import math
import time

centroids_in = [[692, 835],
[696, 417],
[83, 797],
[934, 918],
[691, 204]]

class SingleStepKMeans(MRJob):

    def mapper(self, _, line):
        data_x, data_y = line.strip().split(' ')
        data_x = float(data_x)
        data_y = float(data_y)
        current_index = 0
        min_dist = float('inf')
        min_dist_index = 0
        for centroid_x, centroid_y in centroids_in:
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
        for x, y, n in values:
            x_total += x
            y_total += y
            count += n
            yield index, (x, y)
        yield f"Centroid {index} has coordinates:" , (x_total/count, y_total/count)


if __name__ == '__main__':
    SingleStepKMeans.run()