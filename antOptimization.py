import numpy as np
import random
class AntOpt:
    def distance(self,p1,p2):
        x1,y1 = p1
        x2,y2 = p2        
        return ((x1-x2)**2 + (y1-y2)**2)**.5

    def __init__(self, points:list, Q = 4000, pI = 1, dI = 1, pDecay = 0.2, xFirst = False):
        dims = [len(points), len(points)]
        self.dims = dims
        self.pheremonesM = np.ones(dims)
        self.distanceM = np.zeros(dims)
        self.points = points
        self.n_points = len(points)
        self.Q = Q
        self.pI = pI
        self.dI = dI
        self.pDecay = pDecay
        #optimal solutions of points in indices
        self.optimalSol = list(range(self.n_points))
        #calculates distance between all points
        for y in range(len(points)):
            for x in range(y,len(points)):
                d = self.distance(self.points[y], self.points[x])
                self.distanceM[y][x] = d
                self.distanceM[x][y] = d

        self.bestDistance = np.sum([self.distanceM[i-1][i] for i in range(dims[0])])

    
    def _pxy(self, x, y):
        return self.pheremonesM[x][y]**(self.pI)*self.distanceM[x][y]**self.dI
    
    def probVector(self, start, rest):
        if len(rest) == 1:
            return 1
        eachP = [self._pxy(start,y) for y in rest]
        sums = np.sum(eachP)
        eachP = [P/(sums-P) for P in eachP]
        return eachP

    def getPath(self):
        remaining = list(range(self.n_points))
        path = []
        current = remaining.pop(random.randint(0, self.n_points - 1))
        path.append(current)
        while len(remaining):
            probV = self.probVector(current, remaining)
            pick = np.random.choice(remaining,1,probV)[0]
            remaining.remove(pick)
            path.append(pick)
            current = pick
        return path

    def updatePheromone(self, paths, distances = None):

        tPheromones = np.zeros(self.dims)
        #calculates values for update
        for path in paths:
            distance = 0
            for i in range(1, len(path)):
                distance += self.distanceM[path[i - 1]][path[i]]
            if distance < self.bestDistance:
                self.bestDistance = distance
                self.optimalSol = list(path)
            pheromones = self.Q/distance
            for i in range(1, len(path)):
                tPheromones[path[i - 1]][path[i]] += pheromones
        #updates pheronomones and decay
        for y in range(len(self.points)):
            for x in range(y,len(self.points)):
                newP = self.pheremonesM[y][x]*(1 - self.pDecay) + tPheromones[y][x]
                self.pheremonesM[y][x] = newP
                self.pheremonesM[x][y] = newP

    def explore(self, ants = 10, repitition = 10):
        for r in range(repitition):
            paths = [self.getPath() for a in range(ants)]
            self.updatePheromone(paths)
        