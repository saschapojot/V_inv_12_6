from sympy import *


#This script computes the derivatives of V using sympy


a1,b1,a2,b2,r=symbols("a1,b1,a2,b2,r",cls=Symbol,positive=True)

y0,z0,y1,L=symbols("y0,z0,y1,L",cls=Symbol,positive=True)

V1=a1*r**(-12)-b1*r**(-6)

V2=a2*r**(-12)-b2*r**(-6)

frc16=Rational(1,6)

r1=(2*a1/b1)**frc16
r2=(2*a2/b2)**frc16

###V1
# V1Val=V1.subs([(r,r1)])
#
# drV1=diff(V1,(r,4))
#
# drV1Val=drV1.subs([(r,r1)])
#
# pprint(drV1Val.simplify())

### V2
# V2Val=V2.subs([(r,r2)])
# drV2=diff(V2,(r,4))
# drV2Val=drV2.subs([(r,r2)])
# pprint(drV2Val.simplify())


## V=U1+U2+U3+U4

U1=a1*y0**(-12)-b1*y0**(-6)

U2=a2*z0**(-12)-b2*z0**(-6)

U3=a1*y1**(-12)-b1*y1**(-6)

U4=a2*(-y0-z0-y1+L)**(-12)-b2*(-y0-z0-y1+L)**(-6)


x1=z0
x2=y1

dU1=diff(U1,x1,x2)

dU2=diff(U2,x1,x2)

dU3=diff(U3,x1,x2)

dU4=diff(U4,x1,x2)

dU=dU1+dU2+dU3+dU4

dUVal=dU.subs([(y0,r1),(z0,r2),(y1,r1),(L,2*(r1+r2))])
# pprint(dUVal.simplify())


# dxU1=diff(U1,(x,n))
#
#
# dxU2=diff(U2,(x,n))
#
#
# dxU3=diff(U3,(x,n))
#
# dxU4=diff(U4,(x,n))
#
# dxV=dxU1+dxU2+dxU3+dxU4
#
# dxVVal=dxV.subs([(y0,r1),(z0,r2),(y1,r1),(L,2*(r1+r2))])
#
# pprint(dxVVal)


# dxU2Val=dxU2.subs([(z0,r2)])
#
# dxU4Val=dxU4.subs([(y0,r1),(z0,r2),(y1,r1),(L,2*(r1+r2))])
# pprint(dxU4Val)

# t1,t2=symbols("t1,t2",cls=Symbol,positive=True)

t1=9*2**(Rational(2,3))*b1**(Rational(7,3))*a1**(-Rational(4,3))
t2=9*2**(Rational(2,3))*b2**(Rational(7,3))*a2**(-Rational(4,3))

HV=Matrix([
    [t2,-t2,-t2,-t2],
    [-t2,t1+t2,t2,t2],
    [-t2,t2,2*t2,t2],
    [-t2,t2,t2,t1+t2]
])

pprint(t1**2*t2**2)