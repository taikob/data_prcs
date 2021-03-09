# -*- coding: utf-8 -*-
import numpy as np
import os
from natsort import natsorted
import get as g
import csv

def file_para(path,comtxt,title=None,paramnum=None):
    #comtxt : common text
    #paramum : parameter number

    for dir in natsorted(os.listdir(path)):
        if comtxt in dir:
            tprm = g.readtitleparam(dir)
            data = np.loadtxt(path + '/' + dir, dtype='float')
            if paramnum is None:
                paramnum = len(tprm)
            if data.shape is ():
                datanum=1
            else:
                datanum=data.shape[0]
            break

    out = np.empty((0, paramnum + datanum))
    for dir in natsorted(os.listdir(path)):
        if comtxt in dir:
            data = np.loadtxt(path + '/' + dir, dtype='float')
            tprm = g.readtitleparam(dir,2)
            if datanum==1:
                tprm=tprm+[data]
            else:
                tprm=tprm+data.tolist()
            out = np.append(out, np.array([tprm]), axis=0)

    if title is None: title='stat_data.csv'
    np.savetxt(path + '/' + title, out, delimiter=',')

def combine_txt(filelist,newpath='combined.txt',root='.'):

    with open(root + '/' + newpath, 'w') as tx:
        ti=0
        for fi in filelist:
            with open(root+'/'+fi,'r') as f: txe = [s.strip() for s in f.readlines()]
            for t in txe: tx.write(str(ti) + ', ' + t+'\n')
            ti += 1

def removeline(path,lnum):
    #line number
    with open(path, 'r') as f: dt = f.readlines()

    with open(path.replace('.txt','_remove.txt'), 'w') as f:
        for d in range(lnum,len(dt)):
            f.write(dt[d])

def replace(path,txt,retxt):
    with open(path, 'r') as f: dt = f.readlines()

    with open(path.replace('.txt','_rep.txt'), 'w') as f:
        for d in range(len(dt)):
            f.write(dt[d].replace(txt,retxt))

def rename(path,txt,retxt):

    for dir in os.listdir(path):
        if os.path.isfile(path + '/' + dir) and '.txt' in dir:
            os.rename(path + '/' + dir,path + '/' + dir.replace(txt,retxt))

def convert_to_plot_data(path,prmnum):

    data=np.loadtxt(path)
    prm=data[:, range(0,prmnum)]
    newd=np.ndarray([0,prmnum+2])#newdata
    for i,j in enumerate(range(prmnum,data.shape[1])):
        newr=np.ndarray([data.shape[0],1])#new row
        newr[:]=i
        tmp =np.hstack((newr, prm, data[:,j][:, np.newaxis]))
        newd=np.vstack((newd, tmp))
    name=os.path.splitext(os.path.basename(path))[0]
    folder=path.replace(os.path.basename(path),'')
    np.savetxt(folder + name + '_reshape.csv', newd, delimiter=',')
