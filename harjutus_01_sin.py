from cmath import cos, pi
from math import sin

import matplotlib.pyplot as plt
from numpy import arange

t = list(arange(0, float(4*pi), float(pi/10)))
y = list(map(lambda x: sin(x), t))
z = list(map(lambda x: cos(x), t))

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(t, y, c='b', marker="s", label='japan')
ax1.plot(t, z, c='r', marker="1", label='usa')


plt.show()
