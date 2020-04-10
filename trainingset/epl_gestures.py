from sklearn import datasets
import numpy as np
from nxsdk_modules.epl.src.multi_pattern_learning.epl_multi_pattern_learning import EPLMultiPatternLearning
from nxsdk_modules.epl.src.multi_pattern_learning.epl_parameters import ParamemtersForEPL

def getLabelAndImageData(labelFile, imageFile):
    try:
        labelData = np.load(labelFile)
        imageData = np.load(imageFile)
    except IOError:
        print("Cannot Open Label Files or Image Files")
        raise
    return labelData, imageData

# display the images of the patterns (digits) to be learned
def plot_images(digits, data, title):
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8, 8),
                        subplot_kw={'xticks': [], 'yticks': []})
    for i, ax in enumerate(axs.flat):
        img = data[i]
        img = np.reshape(img, (8,8))
        ax.imshow(img, interpolation=None, cmap='viridis')
        ax.set_title(str(digits[i]))
    plt.tight_layout()
    fig.suptitle(title, fontsize=16)
    plt.show()

#define utility functions
#create the training dataset by choosing the appropriate images of the digts to be learned
def get_training_data(digits, fourX=True, idx=0):
    train_data = []
    for digit in digits:
        training_image = image_dict[digit][idx]
        # print(training_image)
        training_image = np.ndarray.astype(training_image, int)
        if fourX: training_image = (training_image//4)*4
        training_image = np.ndarray.flatten(training_image).tolist()
        # print(training_image)
        train_data.append(training_image)
    return train_data


trainLabelsFile="../2GesturesSet/labelTrain.npy"             
trainImagesFile="../2GesturesSet/imageTrain.npy"
inferLabelsFile="../2GesturesSet/labelInfer.npy"
inferImagesFile="../2GesturesSet/imageInfer.npy"
trainLabelData,trainImageData = getLabelAndImageData(trainLabelsFile, trainImagesFile)
inferLabelData,inferImageData = getLabelAndImageData(inferLabelsFile, inferImagesFile)


# load the digits dataset which consists of 8X8 images of digits
#digits = datasets.load_digits()
#images = digits.images
#targets = digits.target

# create a map of {digt->list of images of the digits}
image_dict = {n : [] for n in range(10)}
for t, img in zip(targets, images):
    image_dict[t].append(img)

numPatterns = 6
#randomly choose 6 digits
digits = [0, 2, 4, 5, 7, 9]

# generate the training data
train_data = get_training_data(digits=digits)

# visulize the training data    
#plot_images(digits, train_data, title="Digits to Learn")

# define the parameters
eplParams = ParamemtersForEPL()
eplParams.numPatterns = numPatterns
# Image size is 8X8 and we are using only 1MC per column
eplParams.numColumns = 64 
eplParams.numMCsPerColumn = 1
# Use 5 GCs per column per pattern
eplParams.numGCsPerPatternPerColumn = 5
eplParams.connProbMCToGC = 0.2
eplParams.numDelaysMCToGC = 2
eplParams.useRandomSeed = True
eplParams.randomGenSeed = 100
eplParams.numGammaCyclesTrain = 45
# create the network

epl = EPLMultiPatternLearning(eplParams=eplParams)

# generate 5 noisy test samples for each pattern
numTestSamples = 5
occlusionPercent = 0.2 # randomly perturb only 20% of the image pixels
test_data = epl.generateTestingData(trainingData=train_data,
                                occlusionPercent=occlusionPercent,
                                numTestSamples=numTestSamples)

#visualize the test data by displaying the 3rd test sample for each pattern
test_data_subset = []
sampleIdx=3
for patternIdx in range(numPatterns):
    idx = patternIdx * numTestSamples + sampleIdx
    test_data_subset.append(test_data[idx])

#plot the 3rd test sample for each pattern
#plot_images(digits, test_data_subset, title="Noisy samples of the learned digits")

epl.fit(trainingSet=train_data, testingSet=test_data)

epl.predict()

epl.evaluate(similarityThreshold=0.85)

epl.showRasterPlot(patternIdx=0, sampleIdx=3)

#Change the number of dendrites between MC->GC connections
eplParams.numDelaysMCToGC = 3 # was 2 before

#create a new network and redo the above process
epl = EPLMultiPatternLearning(eplParams=eplParams)

# This dumps a lot of output
epl.fit(trainingSet=train_data, testingSet=test_data)
epl.predict()

# Accuracy improves to 97% instead of 83% from before
epl.evaluate(similarityThreshold=0.85)
