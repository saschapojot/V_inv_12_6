import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import quad
import pandas as pd
from pathlib import Path
from datetime import datetime

#This script test detailed balance condition S(x|y)
#this script generates data
a=1

b=4

def f(x):
    return -4/(b-a)**2*(x-a)*(x-b)

def p(x):
    return -6/(b-a)**3*(x-a)*(x-b)



# xValsAll=np.linspace(a,b,100)
#
# funcValsAll=[f(x) for x in xValsAll]
#
# pValsAll=[p(x) for x in xValsAll]
#
# plt.figure()
# plt.plot(xValsAll,pValsAll,color="black")
# plt.axvline(x=(a+b)/2, color='r', linestyle='--', linewidth=2)
# plt.savefig("tmp.png")
# plt.close()




def generate_nearby_uni(x,epsilon):
    """

    :param x: current value
    :param epsilon: half length of interval
    :return: uniform distribution on (x-epsilon,x+epsilon) \cap (a,b)
    """
    leftEnd=np.max([x-epsilon,a])
    rightEnd=np.min([x+epsilon,b])

    return np.random.uniform(leftEnd,rightEnd,1)[0]


def proposal(xCurr,epsilon):
    """

    :param xCurr: current value
    :param epsilon: half length of interval
    :return: proposed value
    """

    return generate_nearby_uni(xCurr,epsilon)


def S(x,y,epsilon):
    """

    :param x: generated value from U (y-epsilon, y+epsilon)\cap (a,b)
    :param y: current value
    :param epsilon: half length of interval
    :return:  S(x|y)
    """
    if a<y and y<a+epsilon:
        return 1/(y-a+epsilon)
    elif a+epsilon <= y and y<b+epsilon:
        return 1/(2*epsilon)
    else:
        return 1/(b-y+epsilon)




def acceptanceRatio(xCurr,xNext,epsilon):
    """

    :param xCurr: current value
    :param xNext: proposed value
    :param epsilon: half length of interval
    :return: acceptance ratio of detailed balance
    """

    r=np.min([
        1,
        f(xNext)*S(xCurr,xNext,epsilon)/(f(xCurr)*S(xNext,xCurr,epsilon))
    ])

    return r

def save2csv(xVec, outCsvName):
    """

    :param xVec: data
    :param outCsvName: csv file name
    :return:
    """
    df=pd.DataFrame(xVec,columns=["x_raw"])
    df.to_csv(outCsvName,index=False)


outPath="./testS/"
Path(outPath).mkdir(exist_ok=True,parents=True)

flushNum=8
loop_to_write=1000000

eps=(b-a)/50

#init x
xCurr=a+(b-a)/1.4321

for fls in range(0,flushNum):
    xValsAllPerFlush=[]
    tFlsStart=datetime.now()
    for j in range(0,loop_to_write):
        #propose a move
        xNext=proposal(xCurr,eps)

        #acceptance ratio
        r=acceptanceRatio(xCurr,xNext,eps)
        u=np.random.uniform(0,1,1)[0]
        if u<=r:
            xCurr=xNext
        xValsAllPerFlush.append(xCurr)

    tFlsEnd=datetime.now()
    print("flush "+str(fls)+" time: ",tFlsEnd-tFlsStart)
    outCsvName=outPath+"/flush"+str(fls)+".csv"
    save2csv(xValsAllPerFlush,outCsvName)
