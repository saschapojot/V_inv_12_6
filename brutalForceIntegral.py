import numpy as np
import scipy.integrate as integrate
import pandas as pd
from datetime import datetime
import json
#this script benchmarks the mc computation by brutal force integration
#This script computes Z
rowNum=0
inParamFileName="./V_inv_12_6Params.csv"

inDf=pd.read_csv(inParamFileName)
oneRow=inDf.iloc[rowNum,:]
a1=float(oneRow.loc["a1"])
b1=float(oneRow.loc["b1"])
a2=float(oneRow.loc["a2"])
b2=float(oneRow.loc["b2"])

shift=271

def V(L, y0, z0, y1):
    # L, y0, z0, y1 = x
    val=a1*y0**(-12)-b1*y0**(-6)\
        +a2*z0**(-12)-b2*z0**(-6)\
        + a1*y1**(-12)-b1*y1**(-6)\
        + a2*(-y0-z0-y1+L)**(-12)-b2*(-y0-z0-y1+L)**(-6)+shift


    return val

#minimizers of V
r1=(2*a1/b1)**(1/6)
r2=(2*a2/b2)**(1/6)

eps=(r1+r1)/20

y0Range=[r1-eps,r1+eps]

z0Range=[r2-eps,r2+eps]

y1Range=[r1-eps,r1+eps]

LRange=[2*r1+2*r2-eps,2*r1+2*r2+eps]

def Z(L, y0, z0, y1, beta):
    #
    return np.exp(-beta * V(L, y0, z0, y1))


T=1
beta = 1/T
# result, error = integrate.nquad(lambda L, y0, z0, y1: Z(L, y0, z0, y1, beta), [LRange, y0Range, z0Range, y1Range])
#
# print("Integral result:", result)
# print("Estimated error:", error)


# rstV,errV=integrate.nquad(lambda  L, y0, z0, y1: V(L, y0, z0, y1)*Z(L, y0, z0, y1, beta), [LRange, y0Range, z0Range, y1Range])
#
# print("Integral result of V:", rstV)
# print("Estimated error of EV:", errV)
#
# EV=rstV/result-shift
# print(EV)
def ZIntVal(T):
    beta = 1/T
    result, error = integrate.nquad(lambda L, y0, z0, y1: Z(L, y0, z0, y1, beta), [LRange, y0Range, z0Range, y1Range])
    return [result,error]


TVals=[0.1,0.3]
ZVals=[]
errVals=[]
tIntStart=datetime.now()
for T in TVals:
    rst,err=ZIntVal(T)
    ZVals.append(rst)
    errVals.append(err)


tIntEnd=datetime.now()

outData={"T":list(TVals),
         "Z":list(ZVals),
         "err":list(errVals),
         "shift":str(shift)}

fileName="T"+str(TVals[0])+"_"+str(TVals[-1])+"Z.json"

with open(fileName,"w+") as fptr:
    json.dump(outData,fptr,indent=4)