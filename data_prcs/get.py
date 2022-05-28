import numpy as np
import re
import os
from natsort import natsorted
from datetime import datetime
import csv

def get_sysparam(data,paramrow):

    param=list()
    for i in paramrow:
        prm=np.empty(0)
        for j in range(len(data)):
            if not float(data[j][i]) in prm:
                prm=np.append(prm,float(data[j][i]))
        param.append(np.sort(prm))

    nump=[]
    for p in param:
        nump.append(len(p))

    return param,nump

def readtitleparam(title,sw=0,dl=1):
    #sw=0: str
    #sw=1: int
    #sw=2: float

    titleparam=[]
    title=title.split('_')
    if dl!=0:
        i=0
        while int(dl)>i:
            del title[len(title)-1]
            i+=1
    pattern = r'([+-]?[0-9]+\.?[0-9]*)'

    for t in title:
        titleparam.append(re.sub('\\D','',t))

    if sw==0: out=[re.findall(pattern, t)[0] for t in title]
    if sw==1: out=[int(re.findall(pattern, t)[0]) for t in title]
    if sw==2: out=[float(re.findall(pattern, t)[0]) for t in title]

    return out

def stat_data(path, statdataneme):

    data = []

    for savedir in natsorted(os.listdir(path)):
        savedir = path + '/' + savedir

        if os.path.exists(savedir + '/' + statdataneme):
            datarow = readtitleparam(savedir.split('/')[-1])

            with open((savedir + '/' + statdataneme), 'r') as f:
                datarow = datarow + f.read().split()

            data.append(datarow)

    savepath = path + '/stat/' + str(datetime.now().strftime('%B%d  %H:%M:%S'))
    if not os.path.exists(savepath): os.makedirs(savepath)
    with open((savepath + '/stat_' + statdataneme.split('/')[-1]), 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)


def get_folderlist(folder):
    follist = list()
    for n in natsorted(os.listdir(folder)):
        path = folder + '/' + n
        if os.path.isdir(path):
            follist.append(path)
            follist = follist + get_folderlist(path)
    return follist

def chk_havedata(follist,data):
    newlist=list()
    for dir in follist:#folder list
        #print(dir + '/' + data)
        if os.path.exists(dir + '/' + data):
            newlist.append(dir)
    return newlist

import math as m

def set_cnfl(allcnf):
    nc=len(allcnf)
    ncc=1#num of conbination
    pl=[]#period list
    cnfl=[]

    pl.append(1)
    for i in range(nc-1):
        pl.append(pl[i]*len(allcnf[i]))

    for cnf in allcnf:
        ncc*=len(cnf)

    for i in range(ncc):
        cnf=[]
        for j in range(nc):
            cnf.append(allcnf[j][(int(m.floor(i/pl[j])))%len(allcnf[j])])
        cnfl.append(cnf)

    #print(cnfl)
    return cnfl