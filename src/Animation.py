import cv2
import math
import numpy as np
import os, sys


class Animation:
    """Animation collects all aspects of the animation process including
    creation of frames and video-writing using OpenCV."""

    def __init__(
        self,
        time,
        frame_func,
        fps=30,
        n_cycles=2,
        frame_size=(1000, 1000),
        fourcc="mp4v",
        processed_fname="processed.npy",
        animation_fname="animation.mp4"
    ):
        self.time = time
        self.frame_func = frame_func
        self.fps = fps
        self.n_cycles = n_cycles
        self.nframes = len(time)
        self.frame_size = frame_size
        self.fourcc = fourcc
        self.processed_fname = processed_fname
        self.animation_fname = animation_fname

    def process_frames(self):
        frames = []
        for idx, t in enumerate(self.time):
            sys.stdout.write(f"\rProcessing frame {idx+1} of {self.nframes}")
            sys.stdout.flush()
            self.frame_func(idx, t, frames)

        np.save(self.processed_fname, frames)

    def write_video(self):
        fourcc = cv2.VideoWriter_fourcc(*self.fourcc)
        # frame size must meet or exceed resolution determined by dpi and fig
        # size specified in grid
        video = cv2.VideoWriter(
            self.animation_fname,
            fourcc,
            self.fps,
            self.frame_size
        )

        frames = np.load(self.processed_fname)
        m, n = self.nframes, len(str(self.nframes))
        message = lambda i: (
            f"\rWriting frame: {i+1}" + (n-len(str(i+1)))*" " + " to video "
        )

        for cycle in range(self.n_cycles):
            enum = (
                enumerate(frames)
                if cycle % 2 == 0
                else zip(range(m-1,-1,-1), reversed(frames))
            )

            for idx, image in enum:
                if idx % 10 == 0:
                    sys.stdout.write(message(idx))
                    sys.stdout.flush()
                video.write(image)

        print("\n")
        cv2.destroyAllWindows()
        video.release()
