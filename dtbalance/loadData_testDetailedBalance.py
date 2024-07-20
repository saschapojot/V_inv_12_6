import numpy as np
import pandas as pd
import re
import glob
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import ks_2samp
import json
#This script loads raw data and take effective data
inPath="./testS/"
flushAll=[]
inCsvFilesAll=[]
for file in glob.glob(inPath+"/*.csv"):
    matchFlsh=re.search(r"flush(\d+)",file)
    if matchFlsh:
        flushAll.append(int(matchFlsh.group(1)))
        inCsvFilesAll.append(file)


sortedInds=np.argsort(flushAll)

sortedCsvFiles=[inCsvFilesAll[ind] for ind in sortedInds]

xCombined=np.array([])

# x=pd.read_csv(sortedCsvFiles[0])
# xVec=np.array(x.iloc[:,0])

for file in sortedCsvFiles:
    xVecTmp=pd.read_csv(file)
    xVecNp=np.array(xVecTmp.iloc[:,0])
    xCombined=np.r_[xCombined,xVecNp]

# plt.figure()
# plt.scatter(xCombined,color="black")
# plt.savefig("tmp.png")
# plt.close()


xEqPosition=800000

xTruncated=xCombined[xEqPosition:]

corr_eps=1e-3
NLags=int(len(xTruncated*6/7))

acf_xTruncated=sm.tsa.acf(xTruncated,nlags=NLags)
acf_xTruncatedAbs=np.abs(acf_xTruncated)
plt.figure()
plt.xlabel("lag")
plt.ylabel("|acf|")
plt.plot(list(range(30000,NLags)),acf_xTruncatedAbs[30000:],color="red")
plt.title("|acf|")
plt.savefig("acf.png")
plt.close()

min_acf_x=np.min(acf_xTruncatedAbs)
if min_acf_x<corr_eps:
    lag_x=np.where(acf_xTruncatedAbs<=corr_eps)[0][0]
    xSelected=xTruncated[::lag_x]
    lengthTmp=len(xSelected)
    if lengthTmp%2==1:
        lengthTmp-=1

    lenPart=int(lengthTmp/2)
    xVecValsToCompute=xSelected[-lengthTmp:]

    #test x
    selected_xVecPart0=xVecValsToCompute[:lenPart]
    selected_xVecPart1=xVecValsToCompute[lenPart:]

    result_x=ks_2samp(selected_xVecPart0,selected_xVecPart1)
    numDataPoints=len(selected_xVecPart0)+len(selected_xVecPart1)
    print("ks test p value: "+str(result_x.pvalue))
    print("numDataPoints="+str(numDataPoints))

    outFile="./eff.json"
    jsonOut={"xEff":list(xVecValsToCompute)}
    with open(outFile,"w+")as fptr:
        json.dump(jsonOut,fptr,indent=4)


