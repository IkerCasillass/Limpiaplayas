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

def nothing(val):
    pass

def video_analisis(frame):
    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # Transformar BGR a HSV
        
    blackMask = cv.inRange(frameHSV, Black, Black1)

    nothing(0) # Iniciar trackbar

    #B = cv.getTrackbarPos('Black', 'Frame')
    #maxBlackValue = B

    maxBlackValue = int(cv.getTrackbarPos('Black', 'frame')) #Utilizar el valor decicido en la trackbar

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, blackDetection = cv.threshold(gray, maxBlackValue, 255, cv.THRESH_BINARY_INV) #Detectar valores menores a 20
    #print(maxBlackValue)
    visualizeBlues = cv.bitwise_and(frame, frame, mask=blackMask)

    kernel = np.ones((10, 10), np.uint8)
    opening = cv.morphologyEx(blackDetection, cv.MORPH_OPEN, kernel, iterations=1)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

    contours, hierarchy = cv.findContours(blackDetection, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    frame = cv.drawContours(frame, contours, -1,(0,200,0),3) #Agregando contornos del color negro al frame original    

    #K = kmeans(opening)
    #cv.imshow("Kmeans", K)
    
    cv.imshow('frame', frame)
    cv.imshow("Negro", blackDetection)
    #cv.imshow("open", closing)

#MAIN
#vc = cv.VideoCapture(0)
vc = cv.imread("./lata_playa.jpg")
resized = cv.resize(vc,(720,500))
blur = cv.GaussianBlur(resized,(7,7),cv.BORDER_DEFAULT)
Black = np.array([0, 0, 0], np.uint8)
Black1 = np.array([0, 0, 30], np.uint8)

#Creando Trackbar
slider_Max = 125
cv.namedWindow("frame")
trackbar_name = 'Black'
cv.createTrackbar(trackbar_name, "frame" , 0, slider_Max, nothing)


'''while True:
    ret, frame = vc.read()
    if ret == True:
        video_analisis(frame)
        #get_blob_centroid(frame)

        if cv.waitKey(50) == 27:
            break

vc.release()'''
while True:
    video_analisis(blur)
    #get_blob_centroid(blur)
    if cv.waitKey(50) == 27:
        break
cv.destroyAllWindows()