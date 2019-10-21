import cvxpy as cvx
import numpy as np
import matplotlib.pyplot as plt

N = 50 # time steps
dt = 0.1
path = cvx.Variable((N, 4)) # x/y pos and vel
f = cvx.Variable(N-1) # force

# unpack variables
x = path[:,0]
y = path[:,1]
vx = path[:,2]
vy = path[:,3]

c = [] #constraints
c += [f >= 0] # only fire rocket downward
c += [x[0] == 0, vx[0] == 0, y[0] == 10, vy[0] == 0]

for t in range(N-1):
    c += [x[t + 1] ==  x[t] + vx[t]*dt ]
    c += [y[t + 1] ==  y[t] + vy[t]*dt ]
    c += [vx[t + 1] ==  vx[t]]
    c += [vy[t + 1] ==  vy[t] + (- 9.8 + f[t])*dt ]

c += [y[N-1] == 0] # landed
c += [vy[N-1] == 0] # gently vx[N-1] == 0


objective = cvx.Minimize(cvx.sum(f)) # minimize total fuel use

prob = cvx.Problem(objective, c)
prob.solve(verbose = True)
plt.plot(y.value, label="height")
plt.plot(f.value, label="force")
plt.legend()
plt.title("Height vs Time")
plt.show()

'''
1d lunear lander
2d lunar lander - don't do rotational version.

obstacle lunear lander.
flappy bird mixed integer programming
0/1 with recovery window.

partition into convex regions. The pipes make easy boxes though. And in fact the corners are easy also.
NICE




'''