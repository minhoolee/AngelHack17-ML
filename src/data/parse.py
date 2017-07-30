import json
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt

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
        e['impact_score'] = (float((l-d))/(l+d) + float(v) / v_max)

        a.append(e['impact_score'])
    #     i_mean += e['impact_score']
    # i_mean /= len(dataset)
    # print(i_mean)
    min_val = min(a)
    max_val = max(a)
    a = [(x - min_val)/(max_val - min_val) for x in a]
    print(a)

    for i in range(len(dataset)):
        dataset[i]['impact_score'] = a[i]
        # if a[i] < 0.2:
        #     print(a[i])
        #     print(dataset[i]['title'])
        # if a[i] > 1:
        #     print('error {%s}'.format(dataset[i]['title']))

def parse(dir):
    for f in glob.glob(dir + '/*.json'):
        with open(f, 'r') as infile:
            s = json.load(infile)
            entry = dict([
                ('like_count', s['like_count']),
                ('dislike_count', s['dislike_count']),
                ('title', s['title']),
                ('uploader', s['uploader']),
                ('view_count', s['view_count']),
                ('duration', s['duration'])
            ])
            dataset.append(entry)
    calc_impact_scores()
    # print('{:s}'.format(dataset[0]['title']))
    # print('Like count: {:d}'.format(dataset[0]['like_count']))

def main(argv):
    parse(argv[1])

if __name__ == '__main__':
    main(sys.argv[1:])
