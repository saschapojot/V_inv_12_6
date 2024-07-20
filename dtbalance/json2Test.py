import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

from scipy.stats import rv_continuous
#This computes statistics of effective data
a=1

b=4

def f(x):
    return -4/(b-a)**2*(x-a)*(x-b)

def p(x):
    return -6/(b-a)**3*(x-a)*(x-b)


inJsonFile="./eff.json"

with open(inJsonFile,"r") as fptr:
    data=json.load(fptr)

xVec=np.array(data["xEff"])

plt.figure()
plt.scatter(range(0,len(xVec)),xVec,color="black",s=1)
plt.savefig("xEffScatter.png")
plt.close()


plt.figure()
plt.hist(xVec, bins=60, density=True, alpha=0.6, color='g', label='Data Histogram')

theory_xValsAll=np.linspace(a,b,100)
theory_pValsAll=[p(x) for x in theory_xValsAll]
plt.plot(theory_xValsAll,theory_pValsAll,color="red")

plt.xlabel("x")
plt.ylabel("Density")
plt.savefig("hist.png")
plt.close()


class p_dist_class(rv_continuous):
    def _pdf(self, x):
        return p(x)


p_obj=p_dist_class(a=a,b=b)

p_rand_vals=p_obj.rvs(size=len(xVec))

result=ks_2samp(xVec,p_rand_vals)
print(result)