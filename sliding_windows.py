from helpers import pyramid, sliding_window, show_sliding, show_window, ar_resize, store_window
from detectors import preTrainedSSD, preTrainedRCNN, preTrainedYOLO, PascalVOCTest
import argparse
import time
import mxnet.image as mx
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-n", "--network", required=False, default="YOLO", help="Which network model will infer the image")
ap.add_argument("-v", "--visualize", required=False, default=False, help="Visualize the sliding window")
ap.add_argument("-s", "--store", required=False, default=False, help="Store metadata of each sliding window")
args = vars(ap.parse_args())

visualize = args["visualize"]
store = args["store"]
network = args["network"]

# load the image and define the window width, height and the pyramid scale
(winW, winH) = (512, 512)
scale = 1.5

startingCropHeight = 2200
influenceHeight = 2200
rawImage = mx.imread(args["image"])
rawImageDimensions = (rawImage.shape[1], rawImage.shape[0])

image = mx.fixed_crop(rawImage, 6000, startingCropHeight, 2000, influenceHeight)
#image = rawImage
rawImage = None

i = 0
level = 0
for resized in pyramid(image, scale):
	# loop over the sliding window for each layer of the pyramid
    for (x, y, window) in sliding_window(resized, stepSize=512, windowSize=(winW, winH)):

        i = i + 1

        if (visualize):
            show_sliding((x, y), resized, window, i)

        if (store):
            store_window((x, y), level, scale, (winW, winH), rawImageDimensions, startingCropHeight, i)

        if network == "RCNN":
            preTrainedRCNN(window)

        if network == "YOLO":
            preTrainedYOLO(window)

        if network == "SSD":
            #PascalVOCTest()

        exit()

    level = level + 1
	#print(i)
