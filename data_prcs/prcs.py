# -*- coding: utf-8 -*-
import os
import numpy as np
import math

def msr_average(path,sr=0,dm=',',uc=None,sl=0,ln=10):
    tmp = sl
    for dir in os.listdir(path):
        sl=tmp
        if os.path.isfile(path + '/' + dir) and '.txt' in dir:
            print(dir)
            data=np.loadtxt(path + '/' + dir, skiprows=sr, delimiter=dm, usecols=uc)
            if sl==-1:
                sl=data.shape[0]-ln
            ave=[np.average(data[sl:sl+ln,:], axis=0)]
            np.savetxt(path + '/' +dir.replace('.txt','_ave.txt'), ave)

def normalization(path,uc=None,dm=','):
    data=np.loadtxt(path,delimiter=dm)
    datamax=np.abs(data).max(axis=0)
    if uc is None: uc=datamax.shape[0]
    for c in uc:
        data[:,c]/=datamax[c]
    if '.txt' in path:
        np.savetxt(path.replace('.txt','_nrm.txt '), data, delimiter=',')
    if '.csv' in path:
        np.savetxt(path.replace('.csv','_nrm.csv'), data, delimiter=',')


def get_histogram(group, dx, up):
    gn = len(group)

    for i, stat_data in enumerate(group):
        data = np.loadtxt(stat_data)
        pe = 1.0 / data.shape[0]

        if not 'dist' in locals():
            nx = int(math.ceil(up / dx) + 1)
            dist = np.zeros((nx, gn + 1))
            for j in range(0, nx):
                dist[j][0] = j * dx

        for r in range(0, data.shape[0]):
            if data[r] < up:
                dist[int(math.ceil(data[r] / dx)) - 1][i + 1] += pe
            else:
                dist[-1][i + 1] += pe

    return dist