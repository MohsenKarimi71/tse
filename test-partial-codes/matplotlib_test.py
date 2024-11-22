import matplotlib.pyplot as plt
import numpy as numpy

fig, axs = plt.subplots(2, 3)
axs[1,1].plot([1, 2, 3, 4, 5, 6, 7], [2, 8, 9, 6, 11, 25, 3])
axs[0,2].plot([1, 2, 3, 4, 5, 6, 7], [5, 1, 4, 8, 11, 7, 8])


# a figure with one Axes on the left, and two on the right:
fig2, axs2 = plt.subplot_mosaic([['1', '2', '2'],
                               ['1', '3', '4'],
                               ['5', '5', '5'],
                               ['6', '7', '7']])
axs2['2'].plot([1, 2, 3, 4, 5, 6, 7], [2, 8, 9, 6, 11, 25, 3])
axs2['3'].plot([1, 2, 3, 4, 5, 6, 7], [5, 1, 4, 8, 11, 7, 8])
axs2['4'].plot([1, 2, 3, 4, 5, 6, 7], [2, 8, 9, 6, 11, 25, 3])
axs2['6'].plot([1, 2, 3, 4, 5, 6, 7], [5, 1, 4, 8, 11, 7, 8])

plt.show()