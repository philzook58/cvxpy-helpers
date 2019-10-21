from sympy import *
import cvxpy as cvx
import matplotlib.pyplot as plt
import numpy as np
 
#build corresponding cvx variable for sympy variable
def cvxvar(expr, PSD=True):
    if expr.func == MatrixSymbol:
        i = int(expr.shape[0].evalf())
        j = int(expr.shape[1].evalf())
        return cvx.Variable((i,j), PSD=PSD)        
    elif expr.func == Symbol:
        return cvx.Variable()
 
def cvxify(expr, cvxdict): # replaces sympy variables with cvx variables
     return lambdify(tuple(cvxdict.keys()), expr)(*cvxdict.values()) 
 
 
xs = np.linspace(-1,1,100)
 
for N in range(3,6):
    #plot actual chebyshev
    chebcoeff = np.zeros(N)
    chebcoeff[-1] = 1
    plt.plot(xs, np.polynomial.chebyshev.chebval(xs, chebcoeff), color='r')
 
    cvxdict = {}
    # Going to need symbolic polynomials in x
    x = Symbol('x')
    xn = Matrix([x**n for n in range(N)]);
 
    def sospoly(varname):
        Q = MatrixSymbol(varname, N,N)
        p = (xn.T * Matrix(Q) * xn)[0]
        return p, Q
 
    t = Symbol('t')
    cvxdict[t] = cvxvar(t)
 
    #lagrange multiplier polynomial 1
    pl1, l1 = sospoly('l1')
    cvxdict[l1] = cvxvar(l1)
 
    #lagrange multiplier polynomial 2
    pl2, l2 = sospoly('l2')
    cvxdict[l2] = cvxvar(l2)
 
    #Equation SOS Polynomial 1
    peq1, eq1 = sospoly('eq1')
    cvxdict[eq1] = cvxvar(eq1)
 
    #Equation SOS Polynomial 2
    peq2, eq2 = sospoly('eq2')
    cvxdict[eq2] = cvxvar(eq2)
 
    a = MatrixSymbol("a", N,1)
    pa = Matrix(a).T*xn #sum([polcoeff[k] * x**k for k in range(n)]);
    pa = pa[0]
    cvxdict[a] = cvxvar(a, PSD=False)
 
 
    constraints = []
 
 
    # Rough Derivation for upper constraint
    # pol <= t
    # 0 <= t - pol + lam * (x+1)(x-1)  # relax constraint with lambda
    # eq1 = t - pol + lam
    # 0 = t - pol + lam - eq1
    z1 = t - pa + pl1 * (x+1)*(x-1) - peq1
    z1 = Poly(z1, x).all_coeffs()
    constraints += [cvxify(expr, cvxdict) == 0 for expr in z1]
 
    # Derivation for lower constraint
    # -t <= pol
    # 0 <= pol + t + lam * (x+1)(x-1) # relax constraint with lambda
    # eq2 = pol + t + lam     # eq2 is SOS
    # 0 = t - pol + lam - eq2     #Rearrange to equal zero.
    z2 = pa + t + pl2 * (x+1)*(x-1) - peq2
    z2 = Poly(z2, x).all_coeffs()
    constraints += [cvxify(expr, cvxdict) == 0 for expr in z2]
 
    constraints += [cvxdict[a][N-1,0] == 2**(N-2) ]
    obj = cvx.Minimize(cvxdict[t]) #minimize maximum absolute value
    prob = cvx.Problem(obj,constraints)
    prob.solve()
 
    print(cvxdict[a].value.flatten())
    plt.plot(xs, np.polynomial.polynomial.polyval(xs, cvxdict[a].value.flatten()), color='g')
 
 
plt.show()