import numpy as np
from matplotlib import pyplot as plt
images = np.load('./imageTrain.npy')
plt.imshow(images[10], cmap='gray')
plt.show()
