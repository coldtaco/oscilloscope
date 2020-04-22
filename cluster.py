class Cluster():
    def __init__(self):
        self.pixels = []
        self.n_pixels = 0
        self.middle = None
        self.start = None
        self.end = None
        self.coords = None
        self.results = []
        self.direction = None #0,1,2,3 : N,E,S,W
        self.keyPoints = []

    def addPixel(self, coords):
        self.pixels.append(coords)
        self.n_pixels += 1

    def startPosition(self,dir):
        matrix = self.matrix
        start = self.start
        if dir == 'left':
            if matrix[start[0]-1][start[1]] == 0:
                self.direction = 1
            elif matrix[start[0]][start[1]+1] == 0:
                self.direction = 2
            elif matrix[start[0]+1][start[1]] == 0:
                self.direction = 3
            elif matrix[start[0]][start[1]-1] == 0:
                self.direction = 0
        else:
            while matrix[start[0]+1][start[1]] != 0:
                start[0] +=1
            if matrix[start[0]-1][start[1]] == 0:
                self.direction = 3
            elif matrix[start[0]][start[1]+1] == 0:
                self.direction = 0
            elif matrix[start[0]+1][start[1]] == 0:
                self.direction = 1
            elif matrix[start[0]][start[1]-1] == 0:
                self.direction = 2
        self.coords = self.start
        
    def traverse(self, matrix, dir = 'left'):
        self.matrix = matrix
        self.startPosition(dir)
        iters = 0
        if dir == 'left':
            self.moveLeft()
        else:
            self.moveRight()
        while self.coords != self.start and iters < 10000:
            iters += 1
            if dir == 'left':
                self.moveLeft()
            else:
                self.moveRight()

    def rotateClockwise(self):
        y,x = self.coords
        self.direction = (self.direction + 1)%4

    def rotateCounterClockwise(self):
        self.direction = (self.direction - 1)%4

    def moveLeft(self):
        y,x = self.coords
        if self.direction == 3:
            if self.matrix[self.coords[0]][self.coords[1]-1] == 0:
                self.rotateClockwise() 
                return
            self.results.append((y,x-1))
            self.coords = [y,x-1]
            if self.matrix[self.coords[0]+1][self.coords[1]]:
                self.rotateCounterClockwise() 
        elif self.direction == 2:
            if self.matrix[self.coords[0]+1][self.coords[1]] == 0:
                self.rotateClockwise() 
                return
            self.results.append((y+1,x))
            self.coords = [y+1,x]
            if self.matrix[self.coords[0]][self.coords[1]+1]:
                self.rotateCounterClockwise() 
        elif self.direction == 1:
            if self.matrix[self.coords[0]][self.coords[1]+1] == 0:
                self.rotateClockwise() 
                return
            self.results.append((y,x+1))
            self.coords = [y,x+1]
            if self.matrix[self.coords[0]-1][self.coords[1]]:
                self.rotateCounterClockwise() 
        elif self.direction == 0:
            if self.matrix[self.coords[0]-1][self.coords[1]] == 0:
                self.rotateClockwise() 
                return
            self.results.append((y-1,x))
            self.coords = [y-1,x]
            if self.matrix[self.coords[0]][self.coords[1]-1]:
                self.rotateCounterClockwise() 

    def moveRight(self):
        y,x = self.coords
        if self.direction == 3:
            if self.matrix[self.coords[0]][self.coords[1]-1] == 0:
                self.rotateCounterClockwise()
                return
            self.results.append((y,x-1))
            self.coords = [y,x-1]
            if self.matrix[self.coords[0]-1][self.coords[1]]:
                self.rotateClockwise()
        elif self.direction == 2:
            if self.matrix[self.coords[0]+1][self.coords[1]] == 0:
                self.rotateCounterClockwise()
                return
            self.results.append((y+1,x))
            self.coords = [y+1,x]
            if self.matrix[self.coords[0]][self.coords[1]-1]:
                self.rotateClockwise()
        elif self.direction == 1:
            if self.matrix[self.coords[0]][self.coords[1]+1] == 0:
                self.rotateCounterClockwise()
                return
            self.results.append((y,x+1))
            self.coords = [y,x+1]
            if self.matrix[self.coords[0]+1][self.coords[1]]:
                self.rotateClockwise()
        elif self.direction == 0:
            if self.matrix[self.coords[0]-1][self.coords[1]] == 0:
                self.rotateCounterClockwise()
                return
            self.results.append((y-1,x))
            self.coords = [y-1,x]
            if self.matrix[self.coords[0]][self.coords[1]+1]:
                self.rotateClockwise()