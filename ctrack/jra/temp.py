import matplotlib.pyplot as plt

#f, aax = plt.subplots(2, sharex=True)
#aax[0].plot([1,2,3],[1,1,1])
#aax[1].plot([1,2,3],[2,2,2])
#
#aax[0].set_ylim([0,4])
#aax[1].set_ylim([0,3])
#
#plt.show()
#

fig = plt.figure()
ax1 =fig.add_axes([0.1, 0.1, 0.8, 0.3])
ax1.plot([1,2,3],[1,2,3])
ax1.set_ylim([0,4])

plt.draw()
plt.show()

