import numpy as np
import cv2
import sys
import os
import pickle
import json
from os import listdir
from os.path import isfile
from keras import preprocessing
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import re

# Credit to Alex Thornton on stackoverflow
# https://stackoverflow.com/questions/22287375/sorting-filenames-in-numerical-order-in-python
def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s

def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]

def find_jpgs(dir):
    # print(sorted(listdir(dir), key=alphanum_key))
    # for f in sorted(listdir(dir), key=alphanum_key):
    #     print(f.endswith('.jpg'))
    return [f for f in sorted(listdir(dir), key=alphanum_key) if f.endswith('.jpg')]

def store_imgs(dir):
    dataset = []
    dirs = sorted(listdir(dir), key=alphanum_key)
    for d in dirs:
        # print(d)
        file_list = find_jpgs(dir + '/' + d)
        # entry = []
        for f in file_list:
            # print(f)
            # img = cv2.imread(dir + '/' + d + '/' + f)
            # cv2.imshow("img", img)
            # cv2.waitKey(40)
            img = load_img(dir + '/' + d + '/' + f)
            x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
            x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
            file = dir + '/' + d + '/' + f.rsplit('.', 1)[0][:-5] + '.info.json'
            with open(file, 'r') as infile:
                s = json.load(infile)
                dataset.append((x, s['impact_score']))
        # dataset.append(entry)
    return dataset

def pad_dataset(dataset):
    # preprocessing.pad_sequences(sequences=dataset,
    #                             maxlen=None)
    # for 

    return dataset

def pickle_dict(file, dataset):
    with open(file, 'wb') as f:
        pickle.dump(dataset, f)

def main(argv):
    print('Starting to fill dataset')
    dataset = store_imgs(argv[0])
    dataset = pad_dataset(dataset)
    # print(dataset)
    pickle_dict(argv[1], dataset)

if __name__ == '__main__':
    main(sys.argv[1:])
