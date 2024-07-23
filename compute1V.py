import pandas as pd

import numpy as np

#This script checks one data point and compute energy
L=4.59871
y0=0.974317
z0=1.02131
y1=1.61761

inCsvFile="./V_inv_12_6Params.csv"

df=pd.read_csv(inCsvFile)

row0=df.iloc[0,:]
a1=float(row0.loc["a1"])
b1=float(row0.loc["b1"])
a2=float(row0.loc["a2"])
b2=float(row0.loc["b2"])
print("a1="+str(a1))
print("b1="+str(b1))
print("a2="+str(a2))
print("b2="+str(b2))

def V(LVal,y0Val,z0Val,y1Val):
    val=a1/y0Val**12-b1/y0Val**6\
    +a2/z0Val**12-b2/z0Val**6\
    +a1/y1Val**12-b1/y1Val**6\
    +a2/(-y0Val-z0Val-y1Val+LVal)**12\
    -b2/(-y0Val-z0Val-y1Val+LVal)**6

    print("a1/y0Val**12-b1/y0Val**6="+str(a1/y0Val**12-b1/y0Val**6))
    print("a2/z0Val**12-b2/z0Val**6="+str(a2/z0Val**12-b2/z0Val**6))
    print("a1/y1Val**12-b1/y1Val**6="+str(a1/y1Val**12-b1/y1Val**6))
    print("a2/(-y0Val-z0Val-y1Val+LVal)**12-b2/(-y0Val-z0Val-y1Val+LVal)**6="+str(a2/(-y0Val-z0Val-y1Val+LVal)**12 \
                                                                                 -b2/(-y0Val-z0Val-y1Val+LVal)**6))
    return val


print(V(L,y0,z0,y1))