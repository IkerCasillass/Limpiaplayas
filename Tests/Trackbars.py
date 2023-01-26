import cv2
import numpy

# Remember that functions are declared on top of the scripts on python!
def nothing(val): #Here should go logic for threshold or any filter
	pass

# Creating a window with black image
img = numpy.zeros((300, 512, 3), numpy.uint8)
cv2.namedWindow('image')

#cv2.createTrackbar('variable_name',mat, min_val, max_val, function_name)
# creating trackbars for red color change
cv2.createTrackbar('R', 'image', 0, 255, nothing)

# creating trackbars for Green color change
cv2.createTrackbar('G', 'image', 0, 255, nothing)

# creating trackbars for Blue color change
cv2.createTrackbar('B', 'image', 0, 255, nothing)

while(True):
	# show image
	cv2.imshow('image', img)

	# for button pressing and changing
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

	# get current positions of all Three trackbars
	r = cv2.getTrackbarPos('R', 'image')
	g = cv2.getTrackbarPos('G', 'image')
	b = cv2.getTrackbarPos('B', 'image')

	# display color mixture
	img[:] = [b, g, r]

# close the window
cv2.destroyAllWindows()
