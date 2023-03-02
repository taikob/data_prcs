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
        if i is not None:
            for j in range(len(data)):
                if not np.float128(data[j][i]) in prm: prm=np.append(prm,np.float128(data[j][i]))
        else: prm=np.append(prm,0)
        param.append(np.sort(prm))

    nump=[]
    for p in param: nump.append(len(p))

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

    for t in title:
        if len(re.findall(pattern, t))==0:
            print('Some parameters do not contain numerical values. Please check and delete them.')
            print('all parameter is shown: ',title)
            exit()

    if sw==0: out=[re.findall(pattern, t)[0] for t in title]
    if sw==1: out=[int(re.findall(pattern, t)[0]) for t in title]
    if sw==2: out=[float(re.findall(pattern, t)[0]) for t in title]

    return out

def stat_data(path, statdataneme,dellist=None):

    data = []

    for dir in natsorted(chk_havedata(get_folderlist(path), statdataneme)):
        dir=dir+'/'+statdataneme
        name=dir.replace('/','_')
        if dellist is not None:
            for s in dellist: name=name.replace(s.replace('/','_')+'_','')

        para = readtitleparam(name)
        with open(dir, "r") as c:
            for row in csv.reader(c, delimiter=','): data.append(para+row)


    with open((path + '/stat_' + statdataneme.split('/')[-1]), 'w') as f:
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
        if os.path.exists(dir + '/' + data):
            newlist.append(dir)
    return newlist

import math as m

def chk_havefilename(follist,name):
    newlist=[]
    for dir in follist:
        filelist=[]
        for file in os.listdir(dir):
            if name in file: filelist.append(file)
        if len(filelist)!=0: newlist.append([dir]+filelist)
    return newlist

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