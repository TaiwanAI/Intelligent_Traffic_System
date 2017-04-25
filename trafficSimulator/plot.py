# import numpy as np
# import matplotlib.pyplot as plt
# import time
# y = [10, 9, 13, 12, 15, 18, 11, 5, 6, 7]
# x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# plt.plot(x,y)
# plt.show()
# y = [10, 9, 13, 12, 15, 18, 11, 5, 6, 100]

# time.sleep(1)
# plt.plot(x,y)
# plt.show()

import matplotlib.pyplot as plt
import numpy as np
import time
y_total = [4.0,11.3,33.0,29.1,22.7,41.8,42.7,28.2,20.0,30.0,42.7,38.2,25.5,36.4,33.6,20.0,23.6,38.2,38.2,41.8,42.7,47.3,41.8,51.8,52.7,55.5,52.7,53.6,48.2,50.9,50.9,51.8,50.0,40.0,37.3,37.3,24.5,34.5,51.8,50.9]

x = np.arange(20)
y = y_total[:20]

print(x);
# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.step(x, y, 'r-') # Returns a tuple of line objects, thus the comma
# line2, = ax.step(x, z	)
axes = plt.gca()
axes.set_ylim([1,80])

for i in range(20):

	line1.set_ydata(y)
	
	# y = np.append(y[1:], np.random.normal(loc = 8, scale = 2, size=1)[0])
	y = np.append(y[1:], y_total[20+i])

	print(y.shape)
	fig.canvas.draw()
	time.sleep(0.7)
