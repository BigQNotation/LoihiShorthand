import numpy as np
from matplotlib import pyplot as plt
images = np.load('./imageTrain.npy')
plt.imshow(images[1], cmap='gray')
plt.show()
