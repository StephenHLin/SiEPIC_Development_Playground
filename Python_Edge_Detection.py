# -*- coding: utf-8 -*-
'''
Canny Edge Detection
Source:opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
Otsu Thresholding
Source:docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#opening
Source:docs.opencv.org/3.3.0/d7/d4d/tutorial_py_thresholding.html
Moore Neighbour TRACING
Source: www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
Ramer–Douglas–Peucker algorithm
Source: en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm

Author: Stephen
'''

import cv2 #Image Reader Library
import numpy as np
import Tkinter,tkFileDialog
from matplotlib import pyplot as plt

DEBUG=False
#User Input GUI
# root = Tkinter.Tk()
# root.withdraw()
# filedialog_path = tkFileDialog.askopenfilename()
# img = cv2.imread(filedialog_path,0)

#Without User Input
#filepath = '/home/a2/Documents/UBC/Lithography/Progress Folder/0308_2018/Data/Device0/'
#filename = 'Device0'

filepath = '/home/a2/Documents/UBC/Lithography/Progress Folder/0308_2018/Example/'
filename = 'HIJ'

#filepath = '/home/a2/Documents/UBC/Lithography/'
#filename = 'image_001'

imgname = filename+'.jpg'
savename = filename+'_poly'

#filepath = '/home/a2/Desktop/SiEPIC-Litho/'
#imgname = 'testimg.png'
img = cv2.imread(filepath+imgname,0)
#img = cv2.resize(img, (1280, 720))

if DEBUG:
    edges = cv2.Canny(img,100,200)

    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()

    # global thresholding
    ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    # Otsu's thresholding
    ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # plot all the images and their histograms
    images = [img, 0, th1,
              img, 0, th2,
              blur, 0, th3]
    titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
              'Original Noisy Image','Histogram',"Otsu's Thresholding",
              'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
    for i in xrange(3):
        plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
        plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
        plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
        plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
    plt.show()

else:
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #closing to remove small artifacts on the side
    kernel = np.ones((5,5),np.uint8)
    th3 = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)
    th3 = cv2.bitwise_not(th3)
    #Find Edges
    edges = cv2.Canny(th3,100,200)

    # plt.subplot(131),plt.imshow(img,cmap = 'gray')
    # plt.title('Original SEM'), plt.xticks([]), plt.yticks([])
    # plt.subplot(132),plt.imshow(th3,cmap = 'gray')
    # plt.title('Gaussian Filtered Otsu Threshold'), plt.xticks([]), plt.yticks([])
    # plt.subplot(133),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Detection'), plt.xticks([]), plt.yticks([])
    # plt.show()

#contourimage, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contourimage, contours, hierarchy = cv2.findContours(th3,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]

#filters the contours to only pick the contours at the surface of the device
#filteredcontours = [contours[i] for i in range(len(contours)) if hierarchy[0][i][3] >= 2] #the 2 here is hieracy order, hope all devices are the same.
filteredcontours = [contours[i] for i in range(len(contours)) if hierarchy[i][2] <0]
#REF: https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy

img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
cv2.drawContours(img, filteredcontours, -1, (0, 255, 0), thickness=10, lineType=8)
cv2.imshow("Contour Plot", img)
cv2.waitKey()

'''
#DEBUG BOX
for component in zip(contours, hierarchy):
    currentContour = component[0]
    currentHierarchy = component[1]
    x,y,w,h = cv2.boundingRect(currentContour)
    if currentHierarchy[2] < 0:
        # these are the innermost child components
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
    elif currentHierarchy[3] < 0:
        # these are the outermost parent components
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

#Draw the contour based on the detected edges map
#for h,cnt in enumerate(contours):
    #contimg = cv2.drawContours(edges,[cnt],0,255,10)
polys = [cv2.approxPolyDP(filteredcontours[i],0.5,True) for i in range(len(filteredcontours))]

'''
#Contour to Polygon
polys = []
for cont in filteredcontours:
    polys.append(cv2.approxPolyDP(cont, 0.5, True)) #0.5 is how much distance is allowed from normal shape,
    ##True means the polygon is closed
    #Single line because polys points to the memory location but writing a variable and then having
    #polys point to it results in pointing at the variable location; which in turn is re-written ever loop
    #print approx_curve

cv2.drawContours(img, filteredcontours, -1, (255, 255, 0), thickness=1, lineType=8)
cv2.imshow("Contour Plot", img)
cv2.waitKey()
'''
print(len(polys))

#Organize coordinates from opencv's messy format
x=[]
y=[]
for j in range(len(polys)):
    for i in range(len(polys[j])):
        #newpolys.append(items)
        x.append(polys[j][i][0][0])#Xcoord
        y.append(-polys[j][i][0][1])#Ycoord
    exportcoord = np.array(zip(x,y),dtype=[('x',float),('y',float)]) #create an np with both coords`
    plt.plot(exportcoord['x'],exportcoord['y'])
    plt.show()
    np.savetxt(filepath+savename+str(j)+'.polytxt', exportcoord, delimiter=',') #saves the np array.
    x = [] #Clear the array after
    y = []
