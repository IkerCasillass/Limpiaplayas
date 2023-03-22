#!usr/bin/python

import cv2 as cv
import numpy as np

def draw_grid(img, grid_shape, color=(0, 255, 0), thickness=1):
    h, w, _ = img.shape
    rows, cols = grid_shape
    dy, dx = h / rows, w / cols

    # draw vertical lines
    for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
        x = int(round(x))
        cv.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    # draw horizontal lines
    for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
        y = int(round(y))
        cv.line(img, (0, y), (w, y), color=color, thickness=thickness)

    return img

def get_blob_centroid(img):
    # convert image to grayscale image
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # convert the grayscale image to binary image
    ret,thresh = cv.threshold(gray_image,60,250,cv.THRESH_BINARY_INV)
    
    # calculate moments of binary image
    M = cv.moments(thresh)
    #print(M)
    if M["m00"]!=0:
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # put text and highlight the center
        cv.circle(img, (cX, cY), 5, (255, 255, 255), -1)
        #cv.putText(img, "centroid", (cX - 25, cY - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        draw_target(img, cX, cY)
        
    # display the image
    cv.imshow("centroid", img)
    cv.imshow("thresh",thresh)

def draw_target(img, cX, cY):

    # Start coordinate (w/2, 0)
    h, w = img.shape[:2]
    start_point = (int(w/2), h)
    
    # End coordinate, blob
    end_point = (cX, cY)
    
    # Green color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 9 px
    thickness = 3
    
    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    image = cv.line(img, start_point, end_point, color, thickness)
    
    # Displaying the image 
    cv.imshow('frame', image) 

if __name__ == "__main__":
    vc = cv.VideoCapture(0)
    while(vc.isOpened()):
        ret, frame = vc.read()
        if ret == True:
            #frame = cv.resize(frame, (1280, 720))

            grid = draw_grid(frame,(3,8))
            #cv.imshow("coordinates",grid)

            get_blob_centroid(grid)

            if cv.waitKey(50) == 27:
                break
    vc.release()
    cv.destroyAllWindows()