import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import ks_2samp
from scipy.stats import rv_continuous

#this script tests reject-sampling

sigma=0.1


a=1
b=3.1


xi=a+0.5

def Q(y):
    """

    :param y:
    :return: N(xi, sigma)
    """
    val=1/np.sqrt(2*np.pi*sigma**2)*np.exp(-1/(2*sigma**2)*(y-xi)**2)

    return val


def f(y):
    if a<y and y<b:
        return np.exp(-1/(2*sigma**2)*(y-xi)**2)
    else:
        return 0
M=np.sqrt(2*np.pi*sigma**2)*1.001

rst=quad(f,a,b)

zi=rst[0]

def S(y):
    """

    :param y:
    :return: proposal probability function
    """
    return 1/zi*f(y)

print(quad(S,a,b))

def genOneData():
    y=np.random.normal(xi,sigma,1)[0]
    u=np.random.uniform(0,1)
    while u>=f(y)/(M*Q(y)):
        y=np.random.normal(xi,sigma,1)[0]
        u=np.random.uniform(0,1)
    return y


loopToWrite=10000
xjAll=[genOneData() for j in range(0,loopToWrite)]

xPltAll=np.linspace(a,b,5000)
densityAll=[S(x)  for x in xPltAll]

plt.figure()
plt.hist(xjAll,bins=100, density=True, alpha=0.6, color='g', label='Numerical')
plt.plot(xPltAll,densityAll,color="red",label="theory")
plt.savefig("hist.png")
plt.close()


class S_class(rv_continuous):
    def _pdf(self, x):
        return S(x)

S_obj=S_class(a=a,b=b)

S_rand_vals=S_obj.rvs(size=len(xjAll))

result=ks_2samp(xjAll,S_rand_vals)
print(result)