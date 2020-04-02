import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def histogramme(i):
    hist, bins = np.histogram(i.flatten(), 256, [0, 256])
    return hist

def histogramme_old(i):
    image = np.array(i)
    hist = np.zeros(256, int)

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            hist[int(image[i, j])] = int(hist[int(image[i, j])] + 1)

    return hist


def transformationLinaire(image):
    imageRetour = np.zeros(image.shape)
    lut = np.zeros(256)

    for i in range(0, 256):
        lut[i] = 255 * ((i - image.min()) / (image.max() - image.min()))

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            imageRetour[i, j] = lut[image[i, j]]

    return imageRetour


def transformationLinaireAvecSaturation(image, sMax, sMin):
    imageRetour = np.zeros(image.shape)
    lut = np.zeros(256)

    for i in range(0, 256):
        lut[i] = (255 / (sMax - sMin)) * (i - sMin)
        if (lut[i] < 0):
            lut[i] = 0
        if (lut[i] > 255):
            lut[i] = 255

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            imageRetour[i, j] = lut[image[i, j]]

    return imageRetour

def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	return cv.LUT(image, table)


def egalisationHistogramme(image):
    imageRetour = cv.equalizeHist(image)

    return imageRetour