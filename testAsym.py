import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma, factorial
from datetime import datetime


#This script tests if asymptotic expressions are correct

def C_minus_1_over_p(fa,hpa,p):
    """

    :param fa: f(a)
    :param hpa: h^{(p)}(a)
    :param p:
    :return: C(-1/p)
    """

    val=fa*1/p*(-factorial(p)/hpa)**(1/p)*gamma(1/p)

    return val


def C_minus_2_over_p(fa,hpa,hpPlus1a,p):
    """

    :param fa: f(a)
    :param hpa: h^{(p)}(a)
    :param hpPlus1a: h^{(p+1)}(a)
    :param p:
    :return: C(-2/p)
    """

    val=fa*hpPlus1a*1/p*1/(factorial(p+1))\
        *(-factorial(p)/hpa)**((p+2)/p)*gamma((p+2)/p)

    return val


def C_minus_3_over_p(fa,hpa,hpPlus1a,hpPlus2a,p):
    """

    :param fa: f(a)
    :param hpa: h^{(p)}(a)
    :param hpPlus1a: h^{(p+1)}(a)
    :param hpPlus2a: h^{(p+2)}(a)
    :param p:
    :return: C(-3/p)
    """

    val=fa*hpPlus2a*1/p*1/(factorial(p+2))\
        *(-factorial(p)/hpa)**((p+3)/p)*gamma((p+3)/p)\
        + fa*(hpPlus1a)**2*1/(2*p)\
        *1/(factorial(p+1))**2*(-factorial(p)/hpa)**((2*p+3)/p)*gamma((2*p+3)/p)

    return val


def D_minus_qPlus1_over_p(fqa,hpa,p,q):
    """

    :param fqa: f^{(q)}(a)
    :param hpa: h^{(p)}(a)
    :param p:
    :param q:
    :return: D(-(q+1)/p)
    """
    val=1/p*1/factorial(q)*fqa*(-factorial(p)/hpa)**((q+1)/p)*gamma((q+1)/p)
    return val




def D_minus_qPlus2_over_p(fqa,fqPlus1a,hpa,hpPlus1a,p,q):
    """

    :param fqa: f^{(q)}(a)
    :param fqPlus1a: f^{(q+1)}(a)
    :param hpa: h^{(p)}(a)
    :param hpPlus1a: h^{(p+1)}(a)
    :param p:
    :param q:
    :return: D(-(q+2)/p)
    """

    val=fqa*hpPlus1a*1/p*1/factorial(q)*1/factorial(p+1)*(-factorial(p)/hpa)**((q+p+2)/p)*gamma((q+p+2)/p)\
        +fqPlus1a*1/p*1/factorial(q+1)*(-factorial(p)/hpa)**((q+2)/p)*gamma((q+2)/p)

    return val



def f(t):
    return 1+t**2


def h(t):
    return -t**2-t**3-t**4


a=0
b=1
betaExpInds=np.linspace(-1,5,50)
betaValsAll=10**betaExpInds

betaScatterVals=10**(np.linspace(0,5,5))

q=2
p=2

hpa=-2
hpPlus1a=-6
hpPlus2a=-24

fa=1
fqa=2
fqPlus1a=0

C_minus_1_over_pVal=C_minus_1_over_p(fa,hpa,p)
C_minus_2_over_pVal=C_minus_2_over_p(fa,hpa,hpPlus1a,p)
C_minus_3_over_pVal=C_minus_3_over_p(fa,hpa,hpPlus1a,hpPlus2a,p)
D_minus_qPlus1_over_pVal=D_minus_qPlus1_over_p(fqa,hpa,p,q)
D_minus_qPlus2_over_pVal=D_minus_qPlus2_over_p(fqa,fqPlus1a,hpa,hpPlus1a,p,q)

def leading_1_term(beta):
    """

    :param beta:
    :return: C(-1/p)*beta^{-1/2}
    """
    val=C_minus_1_over_pVal*beta**(-1/2)
    return val


def leading_2_terms(beta):
    """

    :param beta:
    :return: C(-1/p)*beta^{-1/2}+ C(-2/p)* beta^{-1}
    """
    val=C_minus_1_over_pVal*beta**(-1/2)\
        +C_minus_2_over_pVal*beta**(-1)
    return val

def leading_3_terms(beta):
    """

    :param beta:
    :return: C(-1/p)*beta^{-1/2}+ C(-2/p)* beta^{-1}+ [C(-3/p)+D(-(q+1)/p)]x^{-3/2}
    """
    val=C_minus_1_over_pVal*beta**(-1/2) \
        +C_minus_2_over_pVal*beta**(-1)\
        +(C_minus_3_over_pVal+D_minus_qPlus1_over_pVal)*beta**(-3/2)
    return val

def integrand(t,beta):
    return f(t)*np.exp(beta*h(t))

tIntStart=datetime.now()
results = []
scipyVals=[]
for beta in betaValsAll:
    result, error = quad(integrand, a, b, args=(beta,))
    results.append((beta, result, error))
    scipyVals.append(result)
tIntEnd=datetime.now()

print("integrate time: ",tIntEnd-tIntStart)


# # Display the results
# for beta, result, error in results:
#     print(f"Beta: {beta:.1f}, Integral: {result:.5f}, Error: {error:.5e}")

#plt 1 term
leading1TermVals=[leading_1_term(beta) for beta in betaScatterVals]

plt.figure()
plt.plot(betaValsAll,scipyVals,label="scipy",linestyle='-.',color="blue", linewidth=1)
plt.scatter(betaScatterVals,leading1TermVals,color="red",s=6,label="asymtotic, 1 term")
plt.xscale('log')
plt.yscale('log')
plt.legend(loc="best")
plt.xlabel("$\\beta$")
plt.ylabel("$J$")
plt.title("$J\sim C(-\\frac{1}{2})\\beta^{-\\frac{1}{2}}$")
plt.savefig("asymp1term.png")
plt.close()


#plt 2 terms
leading2TermsVals=[leading_2_terms(beta) for beta in betaScatterVals]
plt.figure()
plt.plot(betaValsAll,scipyVals,label="scipy",linestyle='-.',color="blue", linewidth=1)
plt.scatter(betaScatterVals,leading2TermsVals,color="red",s=6,label="asymtotic, 2 terms")

plt.xscale('log')
plt.yscale('log')
plt.legend(loc="best")
plt.xlabel("$\\beta$")
plt.ylabel("$J$")
plt.title("$J\sim C(-\\frac{1}{2})\\beta^{-\\frac{1}{2}}+C(-1)\\beta^{-1}$")
plt.savefig("asymp2terms.png")
plt.close()

#plt 3 terms
leading3TermsVals=[leading_3_terms(beta) for beta in betaScatterVals]
plt.figure()
plt.plot(betaValsAll,scipyVals,label="scipy",linestyle='-.',color="blue", linewidth=1)
plt.scatter(betaScatterVals,leading3TermsVals,color="red",s=6,label="asymtotic, 3 terms")

plt.xscale('log')
plt.yscale('log')
plt.legend(loc="best")
plt.xlabel("$\\beta$")
plt.ylabel("$J$")
plt.title("$J\sim C(-\\frac{1}{2})\\beta^{-\\frac{1}{2}}+C(-1)\\beta^{-1}+[C(-\\frac{3}{2})+D(-\\frac{3}{2})]\\beta^{-\\frac{3}{2}}$")
plt.savefig("asymp3terms.png")
plt.close()