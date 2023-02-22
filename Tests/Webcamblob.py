# Standard imports
import cv2
import numpy as np
 
# Read image
vc = cv2.VideoCapture(0)
# Set up the detector with default parameters.
#detector = cv2.SimpleBlobDetector.create()

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds for binarizing image
params.minThreshold = 0
params.maxThreshold = 150

# Change distance between blobs in pixels
params.minDistBetweenBlobs = 10

# Filter by Color. (0-255 in binary scale)
params.filterByColor = True
params.blobColor = 0

# Filter by Area. (meassured in density pixels)
params.filterByArea = True
params.minArea = 10
params.maxArea = 5000

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

#Color range for detection!!!!!
hsv_min = (0, 0, 0)
hsv_max = (180, 255, 30)
 
while True:
    ret, frame = vc.read()
    if ret == True:

        #Transform to HSV
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_img, hsv_min, hsv_max)
        mask = cv2.dilate(mask, None, iterations=1)
        mask = cv2.erode(mask, None, iterations=1)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
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


        if cv2.waitKey(50) == 27:
            break

cv2.destroyAllWindows()