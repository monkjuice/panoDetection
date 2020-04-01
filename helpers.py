from mxnet.image import imresize
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
from model.Window import Window

def calculate_bbox(position, level, scale, windowSize, startingCropHeight):

	sequence = scale ** level
	position = (position[0], position[1] + (startingCropHeight/sequence))

	(x, y) = (position[0] * sequence, position[1] * sequence)
	(x1, y1) = (position[0] * sequence + (windowSize[0] * sequence), position[1] * sequence + (windowSize[1] * sequence))

	return ((x, y), (x1, y), (x1, y1), (x, y1))

def calculate_spherical_coordinates(bbox, rawImageDimensions):

	x = (bbox[1][0] - bbox[0][0]) / 2 + (bbox[0][0])
	y = (bbox[2][1] -  bbox[1][1]) / 2 + (bbox[0][1])

	center = (x, y)

	ath = (x / rawImageDimensions[0] - 0.5) * 360
	atv = (y / rawImageDimensions[1] - 0.5) * 180

	return (atv, ath, center)

def store_window(position, level, scale, windowSize, rawImageDimensions, startingCropHeight, i):

	bbox = calculate_bbox(position, level, scale, windowSize, startingCropHeight)

	(atv, ath, center) = calculate_spherical_coordinates(bbox, rawImageDimensions)

	window = Window(atv, ath, center, i, bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1])
	window.store()


# resize keeping aspect ratio
def ar_resize(image, scale):
	width = int(image.shape[1] / scale)
	ratio = width / float(image.shape[1])
	height = (int(image.shape[0] * ratio))

	image = imresize(image, w=width, h=height)

	return image

def pyramid(image, scale=1.5, minSize=(600, 600)):
	# yield the original image
	yield image

	# keep looping over the pyramid
	while True:
		# compute the new dimensions of the image and resize it
		image = ar_resize(image, scale)

		# if the resized image does not meet the supplied minimum
		# size, then stop constructing the pyramid
		if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
			break

		# yield the next image in the pyramid
		yield image


def sliding_window(image, stepSize, windowSize):
	# slide a window across the image
	for y in range(0, image.shape[0], stepSize):
		for x in range(0, image.shape[1], stepSize):

			(winWidth, winHeight) = (windowSize[0], windowSize[1])
			(imgWidth, imgHeight) = (image.shape[1], image.shape[0])

			crop = np.index_exp[y:y + winHeight, x:x + winWidth]

			x_out_of_bounds = imgWidth < x + winWidth
			y_out_of_bounds = imgHeight < y + winHeight

			if not x_out_of_bounds and not y_out_of_bounds:
				window =  (x, y, image[crop])

			else:
				(alternativeX, alternativeY) = (x, y)
				if x_out_of_bounds:
					alternativeX = imgWidth - winWidth
				if y_out_of_bounds:
					alternativeY = imgHeight - winHeight
				crop = np.index_exp[alternativeY : imgHeight, alternativeX : imgWidth]
				window = (alternativeX, alternativeY, image[crop])

			yield window


fig, ax = plt.subplots(1)

def show_sliding(position, image, window, i):
	if i == 1:
		ax.imshow(image.asnumpy())

	rect = patches.Rectangle(position,window.shape[0] ,window.shape[1] ,linewidth=1,edgecolor='w',facecolor='none')
	ax.add_patch(rect)
	#ax.axis('off')
	#plt.show(block=False)
	plt.pause(0.000000000002)
	#plt.close()


def show_window(pos, window):
	plt.imshow(window.asnumpy())
	#plt.axis('off')
	plt.show(block=False)
	plt.pause(0.0002)
	plt.close()
