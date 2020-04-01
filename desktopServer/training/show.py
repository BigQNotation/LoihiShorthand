import numpy as np
from matplotlib import pyplot as plt
images = np.load('./imageTrain.npy')
plt.imshow(images[2], cmap='gray')
plt.show()
