import wave
import numpy as np
from tqdm import tqdm
from PIL import Image
import sys
from scipy.io import wavfile
sys.setrecursionlimit(160000)

class Traversal:
    def __init__(self, matrix, start):
        start[0] += 1
        start[1] += 1
        self.matrix = np.pad(matrix,1)
        print(self.matrix.shape)
        self.coords = start
        self.start = start
        self.results = []
        self.direction = None #0,1,2,3 : N,E,S,W
        self.floodcalls = 0
    
    def rotateClockwise(self):
        y,x = self.coords
        self.direction = (self.direction + 1)%4

    def rotateCounterClockwise(self):
        self.direction = (self.direction - 1)%4

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
    
    def flood4(self,y,x):
        if y > self.matrix.shape[0] or x > self.matrix.shape[1]:
            return
        self.matrix[y][x] = 0
        #img = Image.fromarray(np.uint8(self.matrix * 240) , 'L')
        #img.save(f'./debug/m{self.floodcalls}.png')
        self.floodcalls += 1
        #print(f'{self.floodcalls},y={y} x= {x}',end='\r')
        if self.matrix[y+1][x]:
            self.flood4(y+1,x)
        if self.matrix[y-1][x]:
            self.flood4(y-1,x)
        if self.matrix[y][x+1]:
            self.flood4(y,x+1)
        if self.matrix[y][x-1]:
            self.flood4(y,x-1)
        return


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

    def traverse(self, dir = 'left'):
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
        print(f"It took {iters} steps")

    def nextStart(self,prevy,prevx):
        for x in range(prevx,self.matrix.shape[1]):
            if self.matrix[prevy][x]:
                self.start = [prevy,x]
                return 0
        for y in range(prevy,self.matrix.shape[0]):
            for x in range(0,self.matrix.shape[1]):
                if self.matrix[y][x]:
                    print(f'starting at {y},{x}')
                    self.start = [y,x]
                    return 0
        return 1

    def fullTraversal(self,iters = 25):
        iterations = 0
        print('full traversal')
        while self.matrix.sum() and iterations < iters:
            print(self.matrix.sum())
            iterations += 1
            self.traverse()
            leftStart = list(self.start)
            #self.traverse('right')
            print(f"left start = {leftStart}, right start = {self.start}")
            self.flood4(*leftStart)
            #self.flood4(*self.start)
            if self.nextStart(*leftStart):
                break
            img = Image.fromarray(np.uint8(self.matrix * 240) , 'L')
            img.save(f'm{iterations}.png')
        print("matrix sum =")
        print(self.matrix.sum())
