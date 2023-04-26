# !usr/bin/python

import cv2 as cv
import numpy as np
import math as m

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

def get_blob_centroid(img, shape):

    h = shape[0]
    w = shape[1]
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
        draw_target(img, (h,w), (cX, cY))
        
    # display the image
    #cv.imshow("centroid", img)
    cv.imshow("thresh",thresh)

def get_blobs(img, shape):
    h = shape[0]
    w = shape[1]

    # convert the image to grayscale
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray_image,(11,11),cv.BORDER_DEFAULT)

    # convert the grayscale image to binary image
    ret,thresh = cv.threshold(blur,60,250,cv.THRESH_BINARY_INV)
    
    # find contours in the binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    D = []
    if contours != []:
        for c in contours:
            # calculate moments for each contour
            M = cv.moments(c)
            if M["m00"]!=0:
                # calculate x,y coordinate of center
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX = 0
                cY = 0
            cv.circle(img, (cX, cY), 5, (255, 255, 255), -1)
            #cv.putText(img, "centroid", (cX - 25, cY - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            dist = m.sqrt( (cX - int(w/2))**2 + (cY - h)**2 )
            D.append(dist)
            if dist <= min(D):
                #minimal x and y
                fX = cX
                fY = cY
        draw_target(img,(h,w),(fX,fY))

    # display the image
    #cv.imshow("Image", img)
    cv.imshow("thresh", thresh)

    
def draw_target(img, shape, point):

    if point[0] == 0 or point[1] == 0:
        return
    # Start coordinate at the bottom of the image (w/2, 0)
    h = shape[0]
    w = shape[1]
    start_point = (int(w/2), h)
    
    # End coordinate, blob
    end_point = (point[0], point[1])
    
    # Green color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 9 px
    thickness = 3
    
    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    image = cv.line(img, start_point, end_point, color, thickness)
    
    # Displaying the image 
    cv.imshow('frame', image) 
    get_angle(image,(h,w),point)

def get_angle(img, shape, point):

    h = shape[0]
    w = shape[1]

    topPoint = (int(w/2),0)
    bottomPoint = (int(w/2), h)

    image = cv.line(img, bottomPoint, topPoint, (0,0,255), 2)

    X = point[0] - int(w/2)
    Y = point[1] - 0
    angle = m.atan2(Y,X) * (180.0 / m.pi)
    msg = 'Angle: ' + str(round(angle,2))
    cv.putText(image, msg, (100, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    cv.imshow('frame', image)

#def pickedCan(img, )

def detectSea(img, shape):
    h = shape[0]
    w = shape[1]
    blueHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lowerBlue = np.array([88, 50, 20], np.uint8) #lower blue mask
    upperBlue = np.array([125, 255, 255], np.uint8) #upper blue mask

    kernel = np.ones((11, 11), np.uint8)
    blueMask = cv.inRange(blueHSV,lowerBlue,upperBlue)
    opening = cv.morphologyEx(blueMask, cv.MORPH_OPEN, kernel, iterations=3)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

    sea =  cv.bitwise_and(img, img, mask=closing)

    cv.imshow("sea", sea)


    
def main():
    vc = cv.VideoCapture(0)

    #get img size to adjust these parameters
    #print( vc.shape )
    h = 480
    w = 640
    while(vc.isOpened()):
        ret, frame = vc.read()
        if ret == True:
            #frame = cv.resize(frame, (1280, 720))

            #grid = draw_grid(frame,(3,8))
            #cv.imshow("coordinates",grid)

            #get_blob_centroid(frame,(h,w))
            get_blobs(frame,(h,w))
            detectSea(frame, (h,w))
            if cv.waitKey(50) == 27:
                break
    vc.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()