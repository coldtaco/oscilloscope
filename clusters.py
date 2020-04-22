from antOptimization import AntOpt
import numpy as np
import copy
from cluster import Cluster

class Clusters:

    def __init__(self, matrix:np.array):
        self.matrix = copy.deepcopy(matrix)
        self.clusters = []
        self.order = []
        self.newMatrix = np.zeros(matrix.shape)

    def flood8(self,y,x, cluster:Cluster):
        if y > self.matrix.shape[0] or x > self.matrix.shape[1]:
            return
        self.matrix[y][x] = 0
        cluster.addPixel((y,x))
        newMatrix[y][x] = 1
        self.matrix
        if self.matrix[y+1][x]:
            self.flood8(y+1,x, cluster)
        if self.matrix[y-1][x]:
            self.flood8(y-1,x, cluster)
        if self.matrix[y][x+1]:
            self.flood8(y,x+1, cluster)
        if self.matrix[y][x-1]:
            self.flood8(y,x-1, cluster)
        if self.matrix[y+1][x+1]:
            cluster.addPixel((y,x+1))
            newMatrix[y][x+1] = 1
            self.flood8(y+1,x+1, cluster)
        if self.matrix[y-1][x-1]:
            cluster.addPixel((y,x-1))
            newMatrix[y][x-1] = 1
            self.flood8(y-1,x-1, cluster)
        if self.matrix[y-1][x+1]:
            cluster.addPixel((y,x+1))
            newMatrix[y][x+1] = 1
            self.flood8(y-1,x+1, cluster)
        if self.matrix[y+1][x-1]:
            cluster.addPixel((y,x-1))
            newMatrix[y][x-1] = 1
            self.flood8(y+1,x-1, cluster)
        return

    def clusterisePixels(self, matrix):
        pixels = sum(matrix)
        while pixels:
            for y in range(matrix.shape[0]):
                for x in range(matrix.shape[1]):
                    if (self.matrix[y][x]):
                        cluster = Cluster()
                        self.flood8(y,x,cluster)
                        self.clusters.append(cluster)
                        self.pixels -= clusters.n_pixels
                        cluster.middle = np.mean(cluster.pixels, axis = 0)
    
    def clusterDistance(self, c1:Cluster, c2:Cluster):
        x1,y1,x2,y2 = c1.middle, c2.middle
        return ((x1-x2)**2 + (y1-y2)**2)**.5

    def distance(self, p1, p2):
        x1,y1,x2,y2 = p1, p2
        return ((x1-x2)**2 + (y1-y2)**2)**.5
    
    def setDistance(self, s1, s2):
        bestDist = self.distance(s1[0],s2[0])
        bestPair = (s1[0],s2[0])
        for p1 in s2:
            for p2 in s2:
                d = self.distance(p1,p2)
                if d < bestDist:
                    bestDist = d
                    bestPair = (p1,p2)
        return bestPair

    def determineOrder(self):
        points = [list(c.middle) for c in self.clusters]
        opt = AntOpt(points)
        opt.explore()
        self.order = order

    def getImportantPoints(self):
        for c in self.clusters:
            c.pixels.sort(key = lambda x: x[0])
            c.keyPoints.append(c.pixels[0],c.pixels[-1])
            c.pixels.sort(key = lambda x: x[1])
            c.keyPoints.append(c.pixels[0],c.pixels[-1])

    def getStartEnd(self):
        for i in range(1,len(order)):
            c1,c2 = self.clusters[i-1], self.clusters[i]
            c1.end = self.setDistance(c1.keyPoints, c2.middle)
            c2.start = self.setDistance(c1.middle, c2.keyPoints)
        self.clusters[0].start = self.clusters[1].end
        self.clusters[-1].end = self.clusters[-1].start
            
    def traverseAll(self):
        for cluster in self.clusters:
            cluster.travserse()
            ind = cluster.results.index(cluster.end)
            cluster.results = cluster.result[ind:] + cluster.results + cluster.results[:ind]

    def imgTraversal(self, matrix = self.matrix):
        self.matrix = self.matrix
        self.clusterisePixels(self.matrix)
        self.determineOrder()
        self.getImportantPoints()
        self.getStartEnd()
        self.traverseAll
        result = []
        for cluster in self.clusters:
            result += cluster.results
        return result
