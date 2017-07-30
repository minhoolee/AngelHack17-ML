import cv2
import numpy as np
import sys
import os

from subprocess import call
from os import listdir
from os.path import isfile

def find_mp4(dir):
    return [f for f in listdir(dir) if isfile(f) and f.endswith('.mp4')]

def split_videos(file_list=[]):
    for f in file_list:
        cap = cv2.VideoCapture(f)
        vid = []
        while cap.isOpened():
            print("File {:s}".format(f))
            ret, img = cap.read()
            if not ret:
                print("Break")
                break
            # vid.append(cv2.resize(img, (256, 256)))
            cv2.imshow("img", img)
            k = cv2.waitKey(50)
        vid = np.array(vid, dtype=np.float32)

def vid_to_img(dir, file_list=[]):
    for f in file_list:
        src = dir + '/' + f
        file_no_ext = f.rsplit('.', 1)[0]
        print(file_no_ext)
        if not os.path.exists(dir + '/' + file_no_ext):
            os.makedirs(dir + '/' + file_no_ext)
            os.rename(dir + '/' + file_no_ext + '.info.json', 
                      dir + '/' + file_no_ext + '/' + file_no_ext + '.info.json')
            dst = dir + '/' + file_no_ext + '/' + file_no_ext + '-%04d.jpg'
            call(['ffmpeg', '-i', src, '-r', '1', dst])

def main(argv):
    file_list = find_mp4(argv[0])
    # split_video(file_list)
    vid_to_img(argv[0], file_list)

if __name__ == '__main__':
    main(sys.argv[1:])
