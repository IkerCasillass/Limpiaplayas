import cv2 as cv
import numpy as np

def detectDarkBlobs(img):
    
    params = cv.SimpleBlobDetector_Params()

    params.filterByArea = False
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    params.blobColor = 255
    detector = cv.SimpleBlobDetector_create(params)

    #Detect blobs in the image
    keypoints = detector.detect(img)
    print(len(keypoints))
    
    imgKeyPoints = cv.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    #Display found keypoints
    cv.imshow("Keypoints", imgKeyPoints)
    cv.waitKey(0)

    return 0

def video(frame):
            frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # Transformar BGR a HSV
            
            blackMask = cv.inRange(frameHSV, Black, Black1)

            on_trackbar(0) # Iniciar trackbar

            #B = cv.getTrackbarPos('Black', 'Frame')
            #maxBlackValue = B

            maxBlackValue = int(cv.getTrackbarPos('Black', 'Frame')) #Utilizar el valor decicido en la trackbar

            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            ret, blackDetection = cv.threshold(gray, maxBlackValue, 255, cv.THRESH_BINARY_INV) #Detectar valores menores a 20
            
            visualizeBlues = cv.bitwise_and(frame, frame, mask=blackMask)

            kernel = np.ones((3, 3), np.uint8)
            opening = cv.morphologyEx(blackDetection, cv.MORPH_OPEN, kernel, iterations=1)
            closing = cv.morphologyEx(visualizeBlues, cv.MORPH_CLOSE, kernel)

            contours, hierarchy = cv.findContours(blackDetection, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            #frame = cv.drawContours(frame, contours, -1,(0,200,0),3) #Agregando contornos del color negro al frame original

            #K = kmeans(opening)
            #cv.imshow("Kmeans", K)

            #cv.imshow('frame', frame)
            #cv.imshow("Negro", blackDetection)
            cv.imshow("open", opening)

            cv.imshow("Blobs", detectDarkBlobs(opening))

def on_trackbar(val):
    alpha = val / slider_Max
    beta = ( 1.0 - alpha )
    dst = cv.addWeighted(frame, alpha, frame, beta, 0.0)
    cv.imshow("Frame", dst)

#Creando Trackbar
slider_Max = 100
cv.namedWindow("Frame")
trackbar_name = 'Black'
cv.createTrackbar(trackbar_name, "Frame" , 0, slider_Max, on_trackbar)

vc = cv.VideoCapture(0)

Black = np.array([0, 0, 0], np.uint8)
Black1 = np.array([0, 0, 30], np.uint8)

img = cv.imread(r"C:\Users\ikerc\OneDrive\Escritorio\Vision_RT\Tests\latas.jpg", cv.IMREAD_GRAYSCALE) #leyendo imagen en grises


while True:
        ret, frame = vc.read()
        if ret == True:
            video(frame)

            if cv.waitKey(50) == 27:
                break

vc.release()
cv.destroyAllWindows()
