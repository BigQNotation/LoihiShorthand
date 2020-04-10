import numpy as np
from matplotlib import pyplot as plt
import sys

#images = np.load('./imageTrain.npy')
images = np.load('./imageInfer.npy')
plt.imshow(images[int(sys.argv[1])], cmap='gray')
plt.show()
