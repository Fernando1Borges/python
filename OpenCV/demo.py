# Siraj Raval Youtube live demo
# I'll be using OpenCV + Python to detect strawberries in an image. This will take about 45 minutes and it'll be less than 100 lines of code.

#How to do Object Detection with OpenCV [LIVE]
#TFLearn
#OpenCV


import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
from __futuer__ import division

green = (0, 255, 0)

def show(image):

    #figure size in inches
    plt.figure(figsize = (10,10))
    plt.imshow(image, interpolation = 'nearest') #helps show our image

def overlay_mask(mask, image):
    #applying mask to process
    #make the mask rgb
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
    #were converting the mask to rgb
    return img

def find_biggest_contour(image):
    #copy image
    image = image.copy()

    #we want ta list of the contours
    contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # we wwant the chain from gratest to least, in an array
    # lets isolate to get largest contour
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = (contour_sizes, key=lambda x: x[0])[1]

    #return the biggest contour
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [biggest_contour], -1, 255, -1)

    return biggest_contour, mask

def circle_contour(image, contour):
    #we define shape of contour
    #get bounding ellipse
    image_with_ellipse = image.copy()
    ellipse = cv2.fitEllipse(contour)
    #add it
    cv2.ellipse(image_with_ellipse, ellipse, green, 2, cv2.CV_AA)
    return image_with_ellipse



def find_strawberry(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #channels are reversed, rgb is red green blue, bgr is blue green red
    #difference is how the colors are stored, the ordering.
    #order of colors in memory
    #its about bytes and memory and ordreing
    #conver tto correct color scheme is step one

    max_dimension = max(image.shape)
    #shape is the window size, we need it to be the right size

    max_dimension = max(image.shape)
    scale = 700/max_dimension
    image = cv2.resize(image, None, fx=scale, fy=scale)

    #step 3 - clean our image we want clean smooth color for easier identification
    #takes color scheme accross gaussian curve to smomoth it
    image_blur = cv2.GaussianBlur(image, (7, 7), 0)
    #convert image to hsv format
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
    #now we'll filter by the color
    #hsv seperates luma image intensity from chroma the brightness intensity
    # we want to focus on color


    # step 4 - define our filters
    #filter by the color
    # use numpy array to define colors
    min_red = np.array([0,100, 80])
    max_red = np.array([10, 256, 256])

    #mask is like we focus on one color and blur everything else out
    mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)

    #filter by brightness
    min_red2 = np.array([190, 100, 80])
    max_red2 = np.array([180, 256, 256])

    mask2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)

    #ake these two masks and ...
    mask = mask1 + mask2

    #step 5 - segmentation
    #seperate strawberries from everything else

    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #circle strawberry with an ellipse of size 15 by 15
    # make it fit around strawberry
    mask_closed = cv2.morphologyEX(mask, cv2.MORPH_CLOSE, kernal)
    mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernal)
    #first perform a closing operation
    #process of ... useful for closing small holes in ... another safetycheck
    #to make sure its a red layer
    #erosion - dilation
    # dilation - erotion
    #useful for removing noise

    # step 6 - find the biggest strawberry
    # we only want to circle the biggest one if we have more than one
    big_strawberry_contour, mask_strawberries = find_biggest_contour(mask_clean)

    #step 7 - overlay the masks that we created on the image
    overlay = ovarlay_mask(mask_clean, image)

    #step 8 - circle the biggest strawberry
    circled = circle_contour(overlay, big_strawberry_contour)

    show(circled)

    #step 9 (last step) conver back to original color scheme
    bgr = cv2.cvtColor(circled, cv2.COLOR_RGB2BGR)

    return bgr


#read the image in 3 lines

image = cv2.imread('yo.jpg')
result = find_strawberry(image)
#write thenew image
cv2.imwrite('yo2.jpg',result)
