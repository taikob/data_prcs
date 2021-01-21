# -*- coding: utf-8 -*-
import os
import numpy as np

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