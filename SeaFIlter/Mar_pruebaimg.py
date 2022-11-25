import cv2 as cv
import numpy as np

src = r"C:\Users\ikerc\OneDrive\Escritorio\Vision_RT\FiltroMar\Prueba_playa.jpg" #Raw string con ruta de la imagen
img = cv.imread(src, 1) #Leer imagen

HSVimg = cv.cvtColor(img, cv.COLOR_BGR2HSV) #BGR a HSV

lightBlue1 = np.array([88, 50, 20], np.uint8) #Límite inferior de azul bajo
lightBlue2 = np.array([97, 255, 255], np.uint8) #Límite superior de azul bajo

Blue1 = np.array([97, 50, 20], np.uint8) #Límite inferior de azul
Blue2 = np.array([125, 255, 255], np.uint8) #Límite superior de azul


blueMask1 = cv.inRange(HSVimg, lightBlue1, lightBlue2) #Filtrar azul bajo
blueMask2 = cv.inRange(HSVimg, Blue1, Blue2) #Filtrar azul fuerte

allBlues = cv.add(blueMask1, blueMask2) #Filtrar todo el azul
visualizeBlues = cv.bitwise_and(img, img, mask=allBlues) #Visualizar todo el azul


kernel = np.ones((6, 6), np.uint8)
opening = cv.morphologyEx(blueMask2, cv.MORPH_OPEN, kernel, iterations=1)
closing = cv.morphologyEx(blueMask2, cv.MORPH_CLOSE, kernel)



while True:

    cv.imshow('IMAGEN', img) #Imagen original
    cv.imshow('Mar', blueMask2) #Mar filtrado
    cv.imshow("Opening", opening)
    cv.imshow("Closing", closing)
    #cv.imshow('ALLBLUES', visualizeBlues) #Visualizando azules

    if cv.waitKey(50) == 27:
        break


cv.destroyAllWindows()
