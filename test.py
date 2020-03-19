import wave
import numpy as np
from tqdm import tqdm
from PIL import Image
import sys
from scipy.io import wavfile
import cv2
import playsound
import time
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

def main():
    wv = wave.open('./testfile.wav','w')
    wv.setnchannels(2)
    wv.setsampwidth(4)
    wv.setframerate(44100)
    im = Image.open("feelsgoodman.png").convert('L')
    width, height = im.size
    nwidth, nheight = 400, 400
    im.thumbnail((nwidth,nheight), Image.ANTIALIAS)
    im.save('tes.png')
    tim = np.array(im)
    matrix = np.empty([nwidth,nheight])
    currCoords = [0,0]
    found = True
    pixelCount = 0
    for y in tqdm(range(nheight)):
        for x in range(nwidth):
            if tim[y][x] < 50:
                if found:
                    currCoords = [y,x]
                    found = False
                matrix[y][x] = 0
            else:
                matrix[y][x] = 1
    img = Image.fromarray(np.uint8(matrix * 240) , 'L')
    img.save('m.png')
    '''traversal.traverse()
    traversal.traverse('right')'''
    traversal = Traversal(matrix, currCoords)
    traversal.fullTraversal(50)
    edges = cv2.Canny(np.array(img),250,255)
    print(edges)
    moves = (np.array(traversal.results)-nheight/2)/(nheight/2)
    print(list(moves))
    trail = np.zeros([nwidth + 1,nheight + 1])
    inum = 0
    img = Image.fromarray(np.uint8(trail) , 'L')
    for y,x in traversal.results:
        trail[y][x] = 255
        img = Image.fromarray(np.uint8(trail) , 'L')
        inum+=1
        #img.save(f'./debug/{inum}.png')
    img.save(f'trail.png')
    moves = np.array(moves).astype('float32')
    #[print(x) for x in black]
    wavfile.write('stestfile.wav',44100,moves)
    for m in moves:
        for x in range(10):
            wv.writeframes(m)
    print(20)
    wv.close()

def opencv(arg, sigma=0.33):
    try:
        if arg.isdigit():
            arg = int(arg)
        cap = cv2.VideoCapture(arg)
        for x in range(12):
            if cap.isOpened():
                break
            print("unopened, retrying")
            time.sleep(5)
        if not cap.isOpened():
            raise Exception("Video source failed, quitting")
        while True:
            ret, frame = cap.read()
            v = np.median(frame)
            # apply automatic Canny edge detection using the computed median
            lower = int(max(0, (1.0 - sigma) * v))
            upper = int(min(255, (1.0 + sigma) * v))
            edges = cv2.Canny(frame, lower, upper)
            traversal = Traversal(matrix, currCoords)
            pass
    except Exception as e:
        return

if __name__ == "__main__":
    main()