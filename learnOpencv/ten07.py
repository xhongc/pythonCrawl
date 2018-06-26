import numpy as np
import matplotlib.pyplot as plt

ax = plt.subplot(111)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))

x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(x), np.sin(x)

plt.plot(x, C, color='red', linewidth=2.5, linestyle='-', label=r'$cos(t)$')
plt.plot(x, S, color='blue', linewidth=2.5, linestyle='-', label=r'$sin(t)$')

plt.xlim(x.min() * 1.1, x.max() * 1.1)
plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi],
           [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

plt.ylim(C.min() * 1.1, C.max() * 1.1)
plt.yticks([-1, 0, +1],
           [r'$-1$', r'$0$', r'$+1$'])
plt.show()