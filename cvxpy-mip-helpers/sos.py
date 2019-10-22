import cvxpy as cvx
from sympy import *
import random
'''
The idea is to use raw cvxpy and sympy as much as possible for maximum flexibility.

Construct a sum of sqaures polynomial using sospoly. This returns a variable dictionary mapping sympy variables to cvxpy variables.
You are free to the do polynomial operations (differentiation, integration, algerba) in pure sympy
When you want to express an equality constraint, use poly_eq(), which takes the vardict and returns a list of cvxpy constraints.
Once the problem is solved, use poly_value to get back the solution polynomials.

That some polynomial is sum of squares can be expressed as the equality with a fresh polynomial that is explicility sum of sqaures.

With the approach, we get the full unbridled power of sympy (including grobner bases!)

I prefer manually controlling the vardict to having it auto controlled by a class, just as a I prefer manually controlling my constraint sets
Classes suck.
'''


def cvxify(expr, cvxdict): # replaces sympy variables with cvx variables in sympy expr
     return lambdify(tuple(cvxdict.keys()), expr)(*cvxdict.values()) 

def sospoly(terms, name=None):
    ''' returns sum of squares polynomial using terms, and vardict mapping to cvxpy variables '''
    if name == None:
        name = str(random.getrandbits(32))
    N = len(terms)
    xn = Matrix(terms)
    Q = MatrixSymbol(name, N,N)
    p = (xn.T * Matrix(Q) * xn)[0]
    Qcvx = cvx.Variable((N,N), PSD=True)
    vardict = {Q : Qcvx} 
    return p, vardict

def polyvar(terms,name=None):
    ''' builds sumpy expression and vardict for an unknown linear combination of the terms '''
    if name == None:
        name = str(random.getrandbits(32))
    N = len(terms)
    xn = Matrix(terms)
    Q = MatrixSymbol(name, N, 1)
    p = (xn.T * Matrix(Q))[0]
    print(p)
    Qcvx = cvx.Variable((N,1))
    vardict = {Q : Qcvx} 
    return p, vardict

def poly_eq(p1, p2 , vardict):
    ''' returns a list of cvxpy constraints '''
    dp = p1 - p2
    polyvars = list(dp.free_symbols - set(vardict.keys()))
    return [ cvxify(expr, vardict) == 0 for expr in poly(dp, gens = polyvars).coeffs()]

def vardict_value(vardict):
    ''' evaluate numerical values of vardict '''
    return {k : v.value for (k, v) in vardict.items()}

def poly_value(p1, vardict):
    ''' evaluate polynomial expressions with vardict'''
    return cvxify(p1, vardict_value(vardict))

if __name__ == "__main__":
    x = symbols('x')
    terms = [1, x, x**2]
    #p, cdict = polyvar(terms)
    p, cdict = sospoly(terms)
    c = poly_eq(p, (1 + x)**2 , cdict)
    print(c)
    prob = cvx.Problem(cvx.Minimize(1), c)
    prob.solve()

    print(factor(poly_value(p, cdict)))

    # global poly minimization
    vdict = {}
    t, d = polyvar([1], name='t')
    vdict.update(d)

    p, d = sospoly([1,x,x**2], name='p')
    vdict.update(d)
    constraints = poly_eq(7 + x**2 - t, p, vdict)
    obj = cvx.Maximize( cvxify(t,vdict) )
    prob = cvx.Problem(obj, constraints)
    prob.solve()
    print(poly_value(t,vdict))


'''
p, d = sospoly([1,x,x**2,x**3])
cvxdict += d

p, d = sospoly(  [ x ** i * y ** j for i in range(3) for j in range(3)]  )
cvxdict += d
'''



'''

def sospoly(terms, varname=None):
        N = len(terms)
        xn = Matrix(terms)
        Q = MatrixSymbol(varname, N,N)
        p = (xn.T * Matrix(Q) * xn)[0]
        Qcvx = cvx.Variable((N,N), PSD=True)
        vardict = {Q : Qcvx} 
        return SOSExpr(p, vardict)

# Sympy + cvxpy = SOS

class SOS():
    def __init__(self,  ):
        cvx.

    def __eq__(self, rhs):
    def constraints(self):

def sospoly( deglist ):

def sospoly(deglist):
    product([deg for (_,deg) in   ])
    for (var, deg)
    xn = Matrix([x**n for n in range(N)]);
    Q = MatrixSymbol(varname, N,N)
    p = (xn.T * Matrix(Q) * xn)[0]
    return p, Q

def sospoly(terms)

def cvxify(expr, cvxdict): # replaces sympy variables with cvx variables
     return lambdify(tuple(cvxdict.keys()), expr)(*cvxdict.values()) 
class SOSPoly():
    def __init__(self,terms):
        #N = product([deg for (_,deg) in deglist])
        #xn = Matrix([x**n for n in range(N)]);
        N = len(terms)
        xn = Matrix(terms)
        Q = MatrixSymbol(varname, N,N)
        self.p = (xn.T * Matrix(Q) * xn)[0]
        self.vardict = 
    def __rmul__(self, rhs):
        self.p * rhs
    def __add__(self,)




def liftconstpoly(p):
    return SOSExpr(p, {})

class SOSExpr():
    def __init__(self, expr=0, vardict = {}):
        self.vardict = vardict
        self.sympy_expr = expr
    def __rmul__()

    def value():

    def cvxify(self): # replaces sympy variables with cvx variables
        return lambdify(tuple(self.vardict.keys()), expr)(*(self.vardict.values())) 
    

# maybe only off equality.
# SOS is by setting equzl to unknown SOS poly.




class SOSConstraint():
    def __init__(self, lhs, op, rhs):
        if op = "GTE":
            vs = getvars(lhs,rhs)
            sospoly()

    def to_cvx(self):
        z1 = Poly(z1, x).all_coeffs()
        constraints += [cvxify(expr, cvxdict) == 0 for expr in z1]

'''
