import numpy as np
import scipy.integrate as integrate
# import pandas as pd
#this script benchmarks the mc computation by brutal force integration

rowNum=0
inParamFileName="./V_inv_12_6Params.csv"

# inDf=pd.read_csv(inParamFileName)
# oneRow=inDf.iloc[rowNum,:]
a1=25
b1=80
a2=15
b2=67

shift=265

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

eps=(r1+r1)/30

y0Range=[r1-eps,r1+eps]

z0Range=[r2-eps,r2+eps]

y1Range=[r1-eps,r1+eps]

LRange=[2*r1+2*r2-eps,2*r1+2*r2+eps]

def Z(L, y0, z0, y1, beta):
    #
    return np.exp(-beta * V(L, y0, z0, y1))

T=0.5
beta = 1/T
result, error = integrate.nquad(lambda L, y0, z0, y1: Z(L, y0, z0, y1, beta), [LRange, y0Range, z0Range, y1Range])

print("Integral result:", result)
print("Estimated error:", error)


rstV,errV=integrate.nquad(lambda  L, y0, z0, y1: V(L, y0, z0, y1)*Z(L, y0, z0, y1, beta), [LRange, y0Range, z0Range, y1Range])

EV=rstV/result-shift
print(EV)
# limits =[LRange,y0Range,z0Range,y1Range]
# # Define the integrand with the beta parameter
# integrandZ = lambda x: Z(x, beta)
#
# # Perform the 4-dimensional integral using vegas
# integ = vegas.Integrator(limits)
# result = integ(integrandZ, nitn=100, neval=100000)

# print("Integral result:", result.mean)
# print("Estimated error:", result.sdev)

# integrandV=lambda x: V(x)*Z(x,beta)
#
# rstV=integ(integrandV,nitn=100, neval=100000)
#
# EV=rstV.mean/result.mean-shift
#
# print(EV)