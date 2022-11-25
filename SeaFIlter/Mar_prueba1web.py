import cv2 as cv
import numpy as np
def kmeans(image):

    img = image.copy()
    pixel_values = img.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    stop_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    number_of_attempts = 10
    
    # Esta es la estrategia para inicializar los centroides. En este caso, optamos por inicializacin aleatoria.
    centroid_initialization_strategy = cv.KMEANS_RANDOM_CENTERS
    
    _, labels, centers = cv.kmeans(pixel_values,
                                    3, #num of clusters
                                    None,
                                    stop_criteria,
                                    number_of_attempts,
                                    centroid_initialization_strategy)
    
    # Aplicamos las etiquetas a los centroides para segmentar los pixeles en su grupo correspondiente.
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    
    # Debemos reestructurar el arreglo de datos segmentados con las dimensiones de la imagen original.
    segmented_image = segmented_data.reshape(img.shape)
    
    # Mostramos la imagen segmentada resultante.
    return segmented_image


vc = cv.VideoCapture(0)

lightBlue1 = np.array([88, 50, 20], np.uint8)
lightBlue2 = np.array([97, 255, 255], np.uint8)

Blue1 = np.array([97, 50, 20], np.uint8)
Blue2 = np.array([125, 255, 255], np.uint8)



while True:
    ret, frame = vc.read()
    if ret == True:
        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # Transformar BGR a HSV
        
        blueMask1 = cv.inRange(frameHSV, lightBlue1, lightBlue2)
        blueMask2 = cv.inRange(frameHSV, Blue1, Blue2)

        allBlues = cv.add(blueMask1, blueMask2)
        visualizeBlues = cv.bitwise_and(frame, frame, mask=allBlues)

        kernel = np.ones((5, 5), np.uint8)
        opening = cv.morphologyEx(visualizeBlues, cv.MORPH_OPEN, kernel, iterations=1)
        closing = cv.morphologyEx(visualizeBlues, cv.MORPH_CLOSE, kernel)
        
        #cv.imshow('frame', frame)
        #cv.imshow('Light Blue', blueMask1)
        #cv.imshow('Blue', blueMask2)
        #cv.imshow('All blues', allBlues)
        #cv.imshow('Visualize Blues', visualizeBlues)
        #cv.imshow("open", opening)
        #cv.imshow("closing", closing)
        #K = kmeans(visualizeBlues)
        #cv.imshow("kmeans", K)
        if cv.waitKey(50) == 27:
            break

vc.release()
cv.destroyAllWindows()