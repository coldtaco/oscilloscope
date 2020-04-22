import traceback
import wave
import numpy as np
from tqdm import tqdm
from PIL import Image
import sys
from scipy.io import wavfile
import cv2
from playsound import playsound
import time
from traversal import Traversal
import copy
import random
from clusters import Clusters
sys.setrecursionlimit(160000)


def main():
    im = Image.open("feelsgoodman.png").convert('L')
    width, height = im.size
    nwidth, nheight = 400, 400
    im.thumbnail((nwidth,nheight), Image.ANTIALIAS)
    edges = cv2.Canny(np.array(im),250,255)
    c = Clusters(edges)
    results = c.imgTraversal()
    moves = (np.array(results)-nheight/2)/(nheight/2)
    moves = np.array(moves).astype('float32')
    wavfile.write('stestfile.wav',44100,moves)
"""
clusters of pixel (filter out small clusters)
take middle of clusters and find closest
find closest pixels by using most extreme pixels
"""
def opencv(arg, sigma=0.33):
    try:
        if isinstance(arg,int) or arg.isdigit():
            arg = int(arg)
        cap = cv2.VideoCapture(arg)
        for x in range(12):
            if cap.isOpened():
                break
            print("unopened, retrying")
            time.sleep(5)
        if not cap.isOpened():
            raise Exception("Video source failed, quitting")
        print('starting')
        while True:
            ret, frame = cap.read()
            frame = cv2.resize(frame, dsize=(54, 140), interpolation=cv2.INTER_CUBIC)
            v = np.median(frame)
            # apply automatic Canny edge detection using the computed median
            lower = int(max(0, (1.0 - sigma) * v))
            upper = int(min(255, (1.0 + sigma) * v))
            edges = cv2.Canny(frame, lower, upper)
            c = Clusters(edges)
            results = c.imgTraversal()
            nheight, nwidth = edges.shape
            moves = (np.array(results)-nheight/2)/(nheight/2)
            moves = np.array(moves).astype('float32')
            wavfile.write('stestfile.wav',44100,moves)
            playsound('stestfile.wav')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()