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

def filtreMoyenneur3(image):
    return cv.blur(image, (3, 3))

def filtreMoyenneur5(image):
    return cv.blur(image, (5, 5))

def filtreMoyenneur7(image):
    return cv.blur(image, (7, 7))

def filtreGaussien3(image):
    return cv.GaussianBlur(image, (3, 3), 3)

def filtreGaussien5(image):
    return cv.GaussianBlur(image, (5, 5), 3)

def filtreGaussien7(image):
    return cv.GaussianBlur(image, (7, 7), 5)

def filtreMedian3(image):
    return cv.medianBlur(image, 3)

def filtreMedian5(image):
    return cv.medianBlur(image, 5)

def filtreMedian7(image):
    return cv.medianBlur(image, 7)

def robert(image):
    kernelx = np.array([[0, -1], [1, 0]])
    kernely = np.array([[-1, 0], [0, 1]])
    return cv.filter2D(image, -1, kernelx) + cv.filter2D(image, -1, kernely)

def prewitt(image):
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    img_prewittx = cv.filter2D(image, -1, kernelx)
    img_prewitty = cv.filter2D(image, -1, kernely)
    return img_prewittx + img_prewitty

def sobel(image):
    return cv.Sobel(image, cv.CV_8U, 1, 1, ksize=1)

def laplacien(image):
    return cv.Laplacian(image, cv.CV_8U, ksize = 3)

def canny(image, max, min):
    return cv.Canny(image, min, max)