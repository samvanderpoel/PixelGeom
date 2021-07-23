import argparse
import cv2
import numpy as np
import sys

# Run:  python rendervid.py --file='anim.npy'

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True)
file = parser.parse_args().file

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('anim_out.mp4', fourcc, 15, (1000, 1000))
imgs = np.load(file)

n = len(imgs)
m = len(str(n))
for idx, image in enumerate(imgs):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame: ' + str(idx+1) + (m-len(str(idx+1)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame ' + str(n-1-idx) + (m-len(str(n-1-idx)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
for idx, image in enumerate(imgs):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame ' + str(idx) + (m-len(str(idx+1)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame ' + str(n-1-idx) + (m-len(str(n-1-idx)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
print('\n')
