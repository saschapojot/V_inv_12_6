import pandas as pd
import numpy as np
from  sympy import *
import math
#Using sympy, this script checks  properties of the potential function

inCsvFile="./V_inv_12_6Params.csv"

df=pd.read_csv(inCsvFile)

row0=df.iloc[0,:]
a1=float(row0.loc["a1"])
b1=float(row0.loc["b1"])
a2=float(row0.loc["a2"])
b2=float(row0.loc["b2"])


r=symbols("r",cls=Symbol,positive=True)
#min V1

r1=(2*a1/b1)**(1/6)

#min V2

r2=(2*a2/b2)**(1/6)

V1=a1/r**12-b1/r**6

### 1st order derivative
d1V1=diff(V1,(r,1))

d1V1Val=d1V1.subs([(r,r1)])

d1V1Val=d1V1Val.evalf()


#2nd order derivative
d2V1=diff(V1,(r,2))

d2V1Val=d2V1.subs([(r,r1)])

d2V1Val=d2V1Val.evalf()
print(d2V1Val/math.factorial(2))

#3rd order derivative
d3V1=diff(V1,(r,3))
d3V1Val=d3V1.subs([(r,r1)])
d3V1Val=d3V1Val.evalf()

#4th order derivative
d4V1=diff(V1,(r,4))
d4V1Val=d4V1.subs([(r,r1)])
d4V1Val=d4V1Val.evalf()

print(d4V1Val/math.factorial(4))