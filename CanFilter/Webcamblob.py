# Standard imports
import cv2
import numpy as np
import math

def detectBlobs(image, hsv_min, hsv_max):

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds for binarizing image
    params.minThreshold = 0
    params.maxThreshold = 150

    # Change distance between blobs in pixels
    params.minDistBetweenBlobs = 20

    # Filter by Color. (0-255 in binary scale)
    params.filterByColor = True
    params.blobColor = 0

    # Filter by Area. (meassured in density pixels)
    params.filterByArea = True
    params.minArea = 1000
    params.maxArea = 10000

    # Filter by Circularity (values between 0 - 1)
    params.filterByCircularity = False
    params.minCircularity = 0
    params.maxCircularity = 1

    # Filter by Convexity (values from 0 to 1)
    params.filterByConvexity = False
    params.minConvexity = 0.87
    params.maxConvexity = 1
    
    # Filter by Inertia (values from 0 to 1 -> circle)
    params.filterByInertia = False
    params.minInertiaRatio = 0.1
    params.maxInertiaRatio = 0.5

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    #Definir Kernel para operaciones morfologicas (open - close)
    kernel = np.ones((5, 5), np.uint8)

    blurredframe = cv2.GaussianBlur(image, (5, 5), 0)
    hsv_img = cv2.cvtColor(blurredframe, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_img, hsv_min, hsv_max)
    mask = cv2.dilate(mask, None, iterations=1)
    mask = cv2.erode(mask, None, iterations=1)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.medianBlur(mask, 9) #Applying blur to minimize noise

    # Detect blobs.
    reversemask = 255 - mask

    keypoints = detector.detect(reversemask)
    
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(frame
                                        , keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Show keypoints
    number_of_blobs = len(keypoints)
    text = "Cans detected: " + str(len(keypoints))
    cv2.putText(im_with_keypoints, text, (20, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    
    cv2.imshow("Keypoints", im_with_keypoints)
    cv2.imshow('Inverted mask', reversemask)
    
    return keypoints

def getBlobPosition(frame, keypoint):
    rows = float(frame.shape[0])
    cols = float(frame.shape[1])
    center_x    = 0.5*cols
    center_y    = 0.5*rows
    # print(center_x)
    x = (keyPoint.pt[0] - center_x)/(center_x)
    y = (keyPoint.pt[1] - center_y)/(center_y)
    return(x,y)


#Color range for detection!!!!!
hsv_min = (0, 0, 0)
hsv_max = (180, 255, 30)

#Webcam video
vc = cv2.VideoCapture(0)

#Main loop
while True:
    ret, frame = vc.read()
    if ret == True:

        '''width = vc.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = vc.get(cv2.CAP_PROP_FRAME_HEIGHT )
        fps =  vc.get(cv2.CAP_PROP_FPS)'''
        #print(width, height)

        keypoints = detectBlobs(frame, hsv_min, hsv_max)

        for i, keyPoint in enumerate(keypoints):
                
                #--- Here you can implement some tracking algorithm to filter multiple detections
                #--- We are simply getting the first result
                x = keyPoint.pt[0]
                y = keyPoint.pt[1]
                s = keyPoint.size
                a = (math.pi*(s**2)) / 2
                
                print(f"kp {int(i)}:  s = {int(s)}  x = {int(x)}  y = {int(y)}  a = {int(a)}")


                #--- Find x and y position in camera adimensional frame
                x, y = getBlobPosition(frame, keyPoint)

        if cv2.waitKey(50) == 27:
            break

cv2.destroyAllWindows()

