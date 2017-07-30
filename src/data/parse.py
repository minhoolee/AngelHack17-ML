import json
import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import pickle
import math

dataset = list()

def calc_view_max():
    v_max = 0
    for e in dataset:
        v = e['view_count']
        if v > v_max:
            v_max = v
    return v_max

def calc_impact_scores():
    v_max = calc_view_max()
    a = []
    i_mean = 0
    for e in dataset:
        l = e['like_count']
        d = e['dislike_count']
        v = e['view_count']
        print('Parsing - {:s}'.format(e['title']))
        e['impact_score'] = (float((l-d))/(l+d) + float(v) / v_max)
        a.append(e['impact_score'])
    min_val = min(a)
    max_val = max(a)
    a = [(x - min_val)/(max_val - min_val) for x in a]

    for i in range(len(dataset)):
        dataset[i]['impact_score'] = a[i]

def save_as_hdf5():
    with open('dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)

def append_to_json(dir):
    i = 0
    for f in glob.glob(dir + '/*.json'):
        # s = dict()
        # with open(f, 'r') as infile:
        #     s = json.load(infile)
        #     s['impact_score'] = dataset[i]['impact_score']

        # print ('\n')
        # print (dataset[i]['like_count'])
        # print (dataset[i]['dislike_count'])
        # print (dataset[i]['title'])
        # print (dataset[i]['uploader'])
        # print (dataset[i]['view_count'])
        # print (dataset[i]['duration'])
        # print (dataset[i]['thumbnail'])
        with open(f, 'w') as outfile:
            json.dump(dataset[i], outfile)
        i += 1

def parse(dir):
    for f in glob.glob(dir + '/*.json'):
        with open(f, 'r') as infile:
            s = json.load(infile)

            # Thumbnail is possibly in a dict embedded in a list
            if isinstance (s['thumbnails'], list):
                s['thumbnails'] = s['thumbnails'][0]
            if isinstance (s['thumbnails'], dict):
                s['thumbnails'] = s['thumbnails']['url']

            entry = dict([
                ('like_count', s['like_count']),
                ('dislike_count', s['dislike_count']),
                ('title', s['title'].encode('utf-8')),
                ('uploader', s['uploader'].encode('utf-8')),
                ('view_count', s['view_count']),
                ('duration', s['duration']),
                ('thumbnail', s['thumbnails'].encode('utf-8'))
            ])
            dataset.append(entry)
    calc_impact_scores()
    save_as_hdf5()

def main(argv):
    parse(argv[0])
    append_to_json(argv[0])

if __name__ == '__main__':
    main(sys.argv[1:])
