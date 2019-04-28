import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
e=0.0001
matrix_u = []
matrix_u.append(1)
matrix_u.append(0.05)
tx=[]
ty=[]
def fun(x):
    return np.exp(40*x)+2/3*x-5/3
x = np.linspace(0,0.05,100)
y = fun(x)
plt.plot(x,y) # pyplot.plot()
plt.plot(x,0*x,"r")
k=0

while matrix_u[k]-matrix_u[k+1]>e:
    t0 = matrix_u[k+1]
    tmx = t0
    tmy = 1
    while tmy>0:
        tmy = (40*np.exp(40*t0)+2/3)*(tmx-t0)+fun(t0)
        tx.append(tmx)
        ty.append(tmy)
        tmx -= 0.00001
    print(tmy)
    matrix_u.append(tmx)

    plt.plot(tx,ty)
    k = k+1
print(matrix_u[k+1])
plt.show();
