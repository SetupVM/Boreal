import cv2
from PIL import Image
import numpy as np
import os
import math

ALLOWED_EXTENSIONS = {'JPG', 'JPEG', 'PNG', 'TIFF'}
STD_PPI = 150


def pixels2cm(pixels, ppi=STD_PPI):
    return 2.54*(pixels / ppi)

def cm2pixels(cm, ppi=STD_PPI):
    return int(cm / 2.54 * ppi)

def get_image_ppi(filename):
    img = Image.open(filename)
    return img.info['dpi'][0] if 'dpi' in img.info else 150


def make_repeat_halfdrop(img, final_w, final_h, inpixels=False, ppi=150):
    # Makes repeated half-drop version of image of final size width and height (in cm)
    if not inpixels:
        final_w, final_h = cm2pixels(final_w, ppi), cm2pixels(final_h, ppi)
        print("final_w:",final_w,"final_w:",final_h)
        print("imgShape[1]:",img.shape[1],"imgShape[0]:",img.shape[0])
    if img.shape[1] > final_w:
        img = img[:, :final_w]
    if img.shape[0] > final_h:
        img = img[:final_h, :]
    ratio_w, ratio_h = final_w / img.shape[1], final_h / img.shape[0]
    print("ratio_w:",ratio_w,"ratio_h:",ratio_h)
    repeat_w, repeat_h = math.ceil(ratio_w), math.ceil(ratio_h)
    print("repeat_w:",repeat_w,"repeat_w:",repeat_h)
    height, width = img.shape[:2]
    print("height:",height,"width:",width)
    big_w, big_h = math.ceil(final_w / ratio_w * repeat_w), math.ceil(final_h / ratio_h * repeat_h)
    print("big_w:",big_w,"big_h:",big_h)
    result_big = np.zeros((big_h, big_w, img.shape[2]), dtype=np.uint8)
    print(result_big)
    for i in range(repeat_h):
        for j in range(repeat_w):
            if j % 2 == 0:
                result_big[i*height:(i+1)*height, j*width:(j+1)*width] = img
                print("to no par man")
                print(img.shape)
            else:
                print("To no impar 1")
                #start gambiarra nivel hard
                if(height % 2 != 0): 
                    height1 = height + 1
                    result_big[i*height:int((i + 0.5)*height), j*width:(j+1)*width] = img[height1//2:, :]
                    result_big[int((i + 0.5)*height):(i+1)*height, j*width:(j+1)*width] = img[:height1//2, :]
                    print(img.shape)
                print("To impar 2")    
                result_big[i*height:int((i + 0.5)*height), j*width:(j+1)*width] = img[height1//2:, :]
                result_big[int((i + 0.5)*height):(i+1)*height, j*width:(j+1)*width] = img[:height1//2, :]
                print(img.shape)
    result = result_big[:final_h, :final_w]
    return result

img = cv2.imread('/home/victormoraes/Documentos/rapport/app/static/images/signal-2021-04-06-153239_002.jpeg')
pic = make_repeat_halfdrop(img,140,100)
cv2.imwrite('teste1.jpg',pic)