from __future__ import print_function
import sys

import cv2 as cv
import numpy as np


def print_help():
    print('''
    This program demonstrated the use of the discrete Fourier transform (DFT).
    The dft of an image is taken and it's power spectrum is displayed.
    Usage:
    discrete_fourier_transform.py [image_name -- default lena.jpg]''')


def main(image):

    print_help()

    I = image

    if I is None:
        print('Error opening image')
        return -1

    rows, cols = I.shape
    m = cv.getOptimalDFTSize(rows) # On optimise la taille (multiple de 2, 3 ou 5)
    n = cv.getOptimalDFTSize(cols) # On optimise la taille (multiple de 2, 3 ou 5)

    # On étend les frontière de l'image avec les nouvelles tailles. Les pixels ajoutés sont initialisés à 0
    padded = cv.copyMakeBorder(I, 0, m - rows, 0, n - cols, cv.BORDER_CONSTANT, value=[0, 0, 0])

    # Le résultat d'une transformée de Fourier est complexe. Cela implique que pour chaque valeur d'image, le résultat
    # est de deux valeurs d'image (une par composant). De plus, la plage des domaines de fréquence est beaucoup plus
    # grande que son homologue spatiale. Par conséquent, nous les stockons généralement au moins dans un format flottant.
    # Par conséquent, nous convertirons notre image d'entrée en ce type et la développerons avec un autre canal pour contenir les valeurs complexes:
    planes = [np.float32(padded), np.zeros(padded.shape, np.float32)]
    # On Ajoute au plan étendu avec des zéros
    complexI = cv.merge(planes)

    # de cette façon, le résultat peut tenir dans la matrice source
    cv.dft(complexI, complexI)
    ## [dft]
    # compute the magnitude and switch to logarithmic scale
    # = > log(1 + sqrt(Re(DFT(I)) ^ 2 + Im(DFT(I)) ^ 2))
    ## [magnitude]
    cv.split(complexI, planes)                   # planes[0] = Re(DFT(I), planes[1] = Im(DFT(I))

    cv.magnitude(planes[0], planes[1], planes[0])# planes[0] = magnitude
    magI = planes[0]

    # Il s'avère que la plage dynamique des coefficients de Fourier est trop grande pour être affichée à l'écran. Nous
    # avons des valeurs changeantes petites et élevées que nous ne pouvons pas observer comme ça. Par conséquent, les
    # valeurs élevées se transformeront toutes en points blancs, tandis que les petites seront noires. Pour utiliser
    # les valeurs d'échelle de gris à pour la visualisation, nous pouvons transformer notre échelle linéaire en une échelle logarithmique:
    matOfOnes = np.ones(magI.shape, dtype=magI.dtype)
    cv.add(matOfOnes, magI, magI) #  On passe à l'échelle logarithmique
    cv.log(magI, magI)

    # Rappelez-vous qu'à la première étape, nous avons agrandi l'image? Eh bien, il est temps de jeter les valeurs
    # nouvellement introduites. À des fins de visualisation, nous pouvons également réorganiser les quadrants du
    # résultat, de sorte que l'origine (zéro, zéro) corresponde au centre de l'image.
    magI_rows, magI_cols = magI.shape
    # recadrer le spectre, s'il a un nombre impair de lignes ou de colonnes
    magI = magI[0:(magI_rows & -2), 0:(magI_cols & -2)]
    cx = int(magI_rows/2)
    cy = int(magI_cols/2)

    q0 = magI[0:cx, 0:cy]         # Top-Left - Create a ROI per quadrant
    q1 = magI[cx:cx+cx, 0:cy]     # Top-Right
    q2 = magI[0:cx, cy:cy+cy]     # Bottom-Left
    q3 = magI[cx:cx+cx, cy:cy+cy] # Bottom-Right

    tmp = np.copy(q0)               # swap quadrants (Top-Left with Bottom-Right)
    magI[0:cx, 0:cy] = q3
    magI[cx:cx + cx, cy:cy + cy] = tmp

    tmp = np.copy(q1)               # swap quadrant (Top-Right with Bottom-Left)
    magI[cx:cx + cx, 0:cy] = q2
    magI[0:cx, cy:cy + cy] = tmp

    cv.normalize(magI, magI, 0, 1, cv.NORM_MINMAX) # Transformez la matrice avec des valeurs flottantes en a


    return magI

def filtre_passe_bas(image, filtre):
    o_rows, o_cols = image.shape
    m = cv.getOptimalDFTSize(o_rows)
    n = cv.getOptimalDFTSize(o_cols)
    new_image = cv.copyMakeBorder(image, 0, m - o_rows, 0, n - o_cols, cv.BORDER_CONSTANT, value=[0, 0, 0])

    dft = cv.dft(np.float32(new_image), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = new_image.shape
    crow, ccol = rows / 2, cols / 2

    # create a mask first, center square is 1, remaining all zeros
    mask = np.zeros((rows, cols, 2), np.uint8)
    crow_n = crow * filtre / 100
    ccol_n = ccol * filtre / 100
    mask[int(crow - crow_n):int(crow + crow_n), int(ccol - ccol_n):int(ccol + ccol_n)] = 1

    # apply mask and inverse DFT
    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv.idft(f_ishift)
    img_back = cv.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    return img_back[:o_rows, :o_cols]

def filtre_passe_haut(image, filtre):
    o_rows, o_cols = image.shape
    m = cv.getOptimalDFTSize(o_rows)
    n = cv.getOptimalDFTSize(o_cols)
    new_image = cv.copyMakeBorder(image, 0, m - o_rows, 0, n - o_cols, cv.BORDER_CONSTANT, value=[0, 0, 0])

    dft = cv.dft(np.float32(new_image), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = new_image.shape
    crow, ccol = rows / 2, cols / 2

    # create a mask first, center square is 1, remaining all zeros
    mask = np.ones((rows, cols, 2), np.uint8)
    crow_n = crow * filtre / 100
    ccol_n = ccol * filtre / 100
    mask[int(crow - crow_n):int(crow + crow_n), int(ccol - ccol_n):int(ccol + ccol_n)] = 0

    # apply mask and inverse DFT
    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv.idft(f_ishift)
    img_back = cv.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    return img_back[:o_rows, :o_cols]