from helpers import pyramid, sliding_window, show_sliding, show_window, ar_resize, store_window
from detectors import preTrainedSSD, preTrainedRCNN, preTrainedYOLO, PascalVOCTest
import argparse
import time
import mxnet.image as mx
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-n", "--network", required=False, default="none", help="Which network model will infer the image")
ap.add_argument("-v", "--visualize", required=False, default=False, help="Visualize the sliding window")
ap.add_argument("-s", "--store", required=False, default=False, help="Store metadata of each sliding window")
args = vars(ap.parse_args())


visualize = args["visualize"]
store = args["store"]
network = args["network"]

# load the image and define the window width, height and the pyramid scale
(winW, winH) = (512, 512)
scale = 1.5

startingCropHeight = 1300
influenceHeight = 2200
rawImage = mx.imread(args["image"])
rawImageDimensions = (rawImage.shape[1], rawImage.shape[0])

image = mx.fixed_crop(rawImage, 0, startingCropHeight, 11264, influenceHeight)
#image = rawImage
rawImage = None

i = 0

for (x, y, window) in sliding_window(image, stepSize=512, windowSize=(winW, winH)):

    i = i + 1

    if (visualize):
        show_sliding((x, y), image, window, i)
        time.sleep(1)

    if (store):
        store_window((x, y), scale, (winW, winH), rawImageDimensions, startingCropHeight, i)

    if network == "RCNN":
        preTrainedRCNN(window)

    if network == "YOLO":
        preTrainedYOLO(window)

    if network == "SSD":
        PascalVOCTest()
    # exit()
