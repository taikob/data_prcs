import numpy as np
import sys, math
from scipy import stats

def line(x, a, b):
    # ax + b
    out=np.empty(0)
    for xi in x:
        out=np.append(out, a*xi+b)
    return out

def fitline(x,coef):
    fitdata = np.linspace(min(x), max(x), 100)
    fitdata = np.hstack((fitdata.reshape(100, 1),line(fitdata, coef[0], coef[1]).reshape((100, 1))))

    return fitdata

def calc_error(data1,data2,sw=0):
    #dt: data type
        # 0 : ndarray
        # 1 : list
    #data1 must be ndarray
    #sw
    # 0 : mean square
    # 1 : error rate

    if type(data1)!=np.ndarray or type(data2)!=np.ndarray:
        print('data1 must be numpy.ndarray this type is', type(data1), type(data2))
        sys.exit('Error')

    if data2.ndim==1: dt=1
    else: dt=0

    er=0
    num=0
    for d1 in data1:
        if dt==0:
            for d2 in data2:
                if d1[0]==d2[0]:
                    if sw==0:
                        er+=(d1[1]-d2[1])**2
                    else:
                        er+=abs(d1[1]-d2[1])/d1[1]
                    num+=1
                    break
        elif dt==1:
            if sw==0:
                er+=(d1[1]-line([d1[0]], data2[0], data2[1]))**2
            else:
                er+=abs(d1[1]-line([d1[0]], data2[0], data2[1])/d1[1])
            num+=1

    return er/num

def dtm_coe(data1,data2):#coefficient of determination
    #dt: data type
        # 0 : ndarray
        # 1 : list
    #data1 is experment data, must be ndarray
    #data2 is model data

    if type(data1)!=np.ndarray or type(data2)!=np.ndarray:
        print('data1 must be numpy.ndarray this type is', type(data1), type(data2))
        sys.exit('Error')

    if data2.ndim==1: dt=1
    else: dt=0

    ave=np.mean(data1[:,1])
    er1=0
    er2=0
    for d1 in data1:
        er1+=(d1[1]-ave)**2
        if dt==0:
            for d2 in data2:
                if d1[0]==d2[0]:
                    er2+=(d2[1]-ave)**2
                    break
        elif dt==1:
            er2+=(line([d1[0]], data2[0], data2[1])-ave)**2

    return er2/er1

def get_tp_from_error(data):
    var = np.var(data, ddof=1)
    n=data.shape[0]
    ave = np.mean(data)
    t = ave/(math.sqrt(var/n))
    p = 2*(1-stats.t.cdf(abs(t),n-1))

    return t,p