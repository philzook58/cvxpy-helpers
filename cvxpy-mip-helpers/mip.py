import cvxpy as cvx
import numpy as np
import pypoman

def circle(N):
    """Builds N sided polygon MIP approximation of circle. returns x, y, constraints"""
    x = cvx.Variable()
    y = cvx.Variable()
    l = cvx.Variable(N) #interpolation variables
    segment = cvx.Variable(N,boolean=True) #segment indicator variables, relaxing the boolean constraint gives the convex hull of the polygon
    
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    xs = np.cos(angles) #we're using a VRep
    ys = np.sin(angles)

    constraints = []
    constraints += [x == l*xs, y == l*ys] # x and y are convex sum of the corner points
    constraints += [cvx.sum(l) == 1, l <= 1, 0 <= l] #interpolations variables. Between 0 and 1 and sum up to 1
    constraints += [cvx.sum(segment) == 1] # only one indicator variable can be nonzero

    constraints += [l[N-1] <= segment[N-1] + segment[0]] #special wrap around case
    for i in range(N-1):
        constraints += [l[i] <= segment[i] + segment[i+1]] # interpolation variables suppressed
    return x, y, constraints

# one encoding for a relu
# Another possible one is to use rays. lam(1,0) + (1-lam)(1,1) = (x,y)
# https://arxiv.org/pdf/1711.07356.pdf
def relu(x, M=100):
    y = cvx.Variable(x.shape)
    z = cvx.Variable(x.shape, boolean=True)
    notz = 1 - z
    constraints = []
    constraints += [y >= 0, y >= x]
    constraints += [x <= M * z,- M * notz <= x]
    constraints += [y <= M * z, y <= x + 2 * M * notz]
    return y, constraints

def curveMIP(pts):
    d = pts.shape[1]
    N = pts.shape[0]
    x = cvx.Variable(d)
    l = cvx.Variable(N) #interpolation variables
    segment = cvx.Variable(N-1,boolean=True)
    constraints = []
    constraints += [x == pts.T@l]
    constraints += [cvx.sum(l) == 1, l <= 1, 0 <= l] #interpolations variables. Between 0 and 1 and sum up to 1
    constraints += [cvx.sum(segment) == 1] # only one indicator variable can be nonzero

    constraints += [l[0] <= segment[0]] #special cases
    constraints += [l[N-1] <= segment[N-2]]
    for i in range(1,N-1):
        constraints += [l[i] <= segment[i] + segment[i+1]] # interpolation variables suppressed
    return x, segments, constraints


def functionMIP(f, xs):
    ''' samples f at xs (ordered array of positions) to build piecewise linear approximation. Returns a function that can be applied to cvx variables'''
    #fs = np.array([f(x) for pt in pts])
    fs = f(xs) #assume f is vectorized
    def g(x):
        fx, segs, constraints = curveMIP( np.stack(fs,pts).T)
        constraints += [x == fx[1]]
        return fx[0], constraints
    return g

def notMIP(z):
    return 1 - z

def tableMIP(table):
    """ given a table of booleans (a tabulation of a boolean function), outputs a function that uses the first element of the table as the output"""
    A, b = pypoman.duality.compute_polytope_halfspaces(np.array(table))
    A1 = A[:,1:]
    A2 = A[:,0]
    def g(a): # a? or a tuple of as?
        z = cvx.Variable(boolean = True) #vectorize?
        constraints = []
        constraints += [A1@a + A2*z <= b]
        return z, constraints
    return g 

def allBools(n):
    assert(n >= 0)
    if n == 0:
        return []
    elif n == 1:
        return [(0,),(1,)]
    else:
        rec = allBools(n-1)
        return [(0,) + bs  for bs in rec] + [ (1,) + bs  for bs in rec]  

def buildTable(f, arity=2):
    inputs = allBools(arity)
    table = [(f(*bs),) + bs  for bs in inputs]
    return table

def mipify(f, arity=2, allowExtra = False):
    table = buildTable(f,arity=arity)
    return tableMIP(table)
    '''
    def g(*args):
        assert(len(args) == arity)
        assert(args[0].shape == args[1].shape)
        z = cvx.Variable(args[0].shape, boolean=True)
    return g
    '''



andMIP = mipify(lambda a,b: a * b)
orMIP = mipify(lambda a,b: max(a, b))
xorMIP = mipify(lambda a, b: int(a == b))

print(buildTable(lambda a,b: a * b))
print(andMIP)
'''


make mip pendulum using circle. Turns pendulum into a sequence of inlcined planes. Possibly a bad approximation
The SHO oscillator sine apporixmation at the stable point is replaced with peicewise parabolas. you could do worse. Although.. piecewise parabolas in cartesian space?

rather than circle
arbitrary mipcurve
mipclosedcurve
mip surface - given triangualtion of surface, we can mip it
delauney - simple 2d plane areas
union - open union - reify the individal areas and then extrnal sum z == 1
listunion

functions ~ curves

def suppressedPair(N):
    l = cvx.variable(N)
    z = cvx.Variable(N, boolean=True)
    constraints = [0 <= l, l <= z]
    return l, z, constraints


# curve_mip is union of segments. Vrep of a segment is just 2 points.


def union_of_vrep(vreps):
    nshapes = len(vreps)
    c = []
    indicators = cvx.Variable(nshapes, boolean=True)
    c += [cvx.sum(indicators) == 1] # in exactly 1
    xs = []
    for i,vrep in enumerate(vreps):
        (verts, d) = vrep.shape 
        coordinates = cvx.Variables(verts)
        c += [coordinates >= 0, coordinates <= indicator[i]]
        xs.append(coordinates * vrep)
    x = cvx.Variable(d)
    c += [sum(xs) == x]
    return x, c


#what happened to reify?
# ctx is constraints built so far. We need to this to compute big M.
# and really it would be nice (vital?) to turn off boolean
def reify_halfplane(p, ctx): 
    pass

class PolyRel():
    # list of integers
    from : List[Int]
    to   : List[Int]
    vars : List[cvx.Variables] # maybe the from to lists should just be these.
    constraints = List[Cvx.Expr] ?

    def compose(self, ):
    def converse(self, ):
    def complement(self):
    def __rdiv__()
    def __rmul__(self,r):
        sefl.compose(r)
    def union(self,r):
    def intersect(self,r):
    def query_sub(self,r):
        return prob
    def 


'''