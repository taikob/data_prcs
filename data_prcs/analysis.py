import numpy as np
import sys

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