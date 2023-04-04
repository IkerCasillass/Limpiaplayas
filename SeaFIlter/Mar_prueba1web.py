import cv2
import numpy as np

def detectSea(img, shape):
    h = shape[0]
    w = shape[1]
    blueHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerBlue = np.array([88, 50, 20], np.uint8) #lower blue mask
    upperBlue = np.array([125, 255, 255], np.uint8) #upper blue mask

    kernel = np.ones((11, 11), np.uint8)
    blueMask = cv2.inRange(blueHSV,lowerBlue,upperBlue)
    opening = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel, iterations=3)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    sea =  cv2.bitwise_and(img, img, mask=closing)

    grayimg = cv2.cvtColor(sea, cv2.COLOR_BGR2GRAY)
        # Detecting contours in image. 
    contours, _= cv2.findContours(grayimg, cv2.RETR_TREE, 
                                cv2.CHAIN_APPROX_SIMPLE) 
    

    font = cv2.FONT_HERSHEY_COMPLEX
    
    #For storing y coordinates of sea
    ycoordinates = []
    # Going through every contours found in the image. 
    for cnt in contours : 

        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 

        # draws boundary of contours. 
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 5) 

        # Used to flatted the array containing 
        # the co-ordinates of the vertices. 
        n = approx.ravel() 
        i = 0


        for j in n : 
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1] 
                ycoordinates.append(y)

                # String containing the co-ordinates. 
                string = str(x) + " " + str(y) 

                if(i == 0): 
                    # text on topmost co-ordinate. 
                    cv2.putText(img, "Arrow tip", (x, y), 
                                    font, 0.5, (255, 0, 0)) 

                else: 
                    # text on remaining co-ordinates. 
                    cv2.putText(img, string, (x, y), 
                            font, 0.5, (0, 255, 0)) 
            i = i + 1

    return max(ycoordinates), sea

def main():
    vc = cv2.VideoCapture(0)
    h = 480
    w = 640

    while True:
        ret, frame = vc.read()
        if ret == True:
            lower_bound, sea = detectSea(frame, (h,w))
            cv2.imshow("Sea", sea)
            print(lower_bound)
            if cv2.waitKey(50) == 27:
                break

    vc.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()