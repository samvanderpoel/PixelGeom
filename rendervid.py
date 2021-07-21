import argparse
import cv2
import numpy as np

# Run:  python rendervid.py --file='anim.npy'

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True)
file = parser.parse_args().file

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('anim_out.mp4', fourcc, 20, (1000, 1000))
imgs = np.load(file)

n = len(imgs)
for idx, image in enumerate(imgs):
    if idx % 10 == 0: print('Working on image ' + str(idx))
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0: print('Working on image ' + str(n-1-idx))
    video.write(image)
for idx, image in enumerate(imgs):
    if idx % 10 == 0: print('Working on image ' + str(idx))
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0: print('Working on image ' + str(n-1-idx))
    video.write(image)
