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

def watershed(image):

    img = image.copy()
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    ret, thresh = cv.threshold(blur,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
 
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)
    sure_bg = cv.morphologyEx(opening,cv.MORPH_CLOSE,kernel, iterations = 2)
    # sure background area
    # sure_bg = cv.dilate(opening,kernel,iterations=2)
    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,3)
    ret, sure_fg = cv.threshold(dist_transform,0.1*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg,sure_fg)


    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    # img[markers == 1] = [0,255,0]

    # cv.imshow("Watershed", img)

    markers = cv.watershed(image,markers)

    image[markers == -1] = [255,0,0]

    return image

def contour(image):

    img = image.copy()
    img = cv.resize(img,(256,256))

    gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    _,thresh = cv.threshold(gray, np.mean(gray), 255, cv.THRESH_BINARY_INV)
    edges = cv.dilate(cv.Canny(thresh,0,255),None)

    cnt = sorted(cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[-2], key=cv.contourArea)[-1]
    mask = np.zeros((256,256), np.uint8)
    masked = cv.drawContours(mask, [cnt],-1, 255, -1)

    dst = cv.bitwise_and(img, img, mask=mask)
    segmented = cv.cvtColor(dst, cv.COLOR_BGR2RGB)

    return segmented


if __name__ == "__main__":
    vc = cv.VideoCapture(0)
    while(vc.isOpened()):
        ret, frame = vc.read()
        if ret == True:
            frame = cv.resize(frame, (1280, 720))

            K = kmeans(frame)
            cv.imshow('Kmeans', K)

            W = watershed(frame)
            #cv.imshow("Watershed", W)

            C = contour(frame)
            #cv.imshow("Contours", C)

            if cv.waitKey(50) == 27:
                break
    vc.release()
    cv.destroyAllWindows()
