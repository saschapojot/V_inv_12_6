import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

#This script checks one data point and compute energy
#and make plots
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




def V1(r):
    return a1/r**12-b1/r**6



def V2(r):
    return a2/r**12-b2/r**6



#min V1

r1=(2*a1/b1)**(1/6)

#min V2

r2=(2*a2/b2)**(1/6)



rV1ValsAll=np.linspace(r1*0.9,3.5*r1,100)
V1ValsAll=[V1(r) for r in rV1ValsAll]

plt.figure()
plt.plot(rV1ValsAll,V1ValsAll,color="black")
plt.title("$V_{1}=$"+str(a1)+"$/r^{12}-$"+str(b1)+"$/r^{6}$")
plt.xlabel("r")
plt.savefig("V1.png")

plt.close()



rV2ValsAll=np.linspace(r2*0.9,2.5*r2,100)
V2ValsAll=[V2(r) for r in rV2ValsAll]

plt.figure()
plt.plot(rV2ValsAll,V2ValsAll,color="black")
plt.title("$V_{2}=$"+str(a2)+"$/r^{12}-$"+str(b2)+"$/r^{6}$")
plt.xlabel("r")
plt.savefig("V2.png")

plt.close()

print(2*(r1+r2))