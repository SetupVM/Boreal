import cv2
from PIL import Image
import numpy as np
import os
import math

ALLOWED_EXTENSIONS = {'JPG', 'JPEG', 'PNG', 'TIFF'}
STD_PPI = 150


def make_repeat_basic(img, final_w, final_h, inpixels=False, ppi=150):
    # Makes repeated basic version of image of final size width and height (in cm)
    if not inpixels:
        final_w, final_h = cm2pixels(final_w, ppi), cm2pixels(final_h, ppi)
    if img.shape[1] > final_w:
        img = img[:, :final_w]
    if img.shape[0] > final_h:
        img = img[:final_h, :]
    ratio_w, ratio_h = final_w / img.shape[1], final_h / img.shape[0]
    repeat_w, repeat_h = math.ceil(ratio_w), math.ceil(ratio_h)
    height, width = img.shape[:2]
    big_w, big_h = math.ceil(final_w / ratio_w * repeat_w), math.ceil(final_h / ratio_h * repeat_h)
    result_big = np.zeros((big_h, big_w, img.shape[2]), dtype=np.uint8)
    for i in range(repeat_h):
        for j in range(repeat_w):
            result_big[i*height:(i+1)*height, j*width:(j+1)*width] = img
    result = result_big[:final_h, :final_w]
    return result

def make_repeat_halfdrop(img, final_w, final_h, inpixels=False, ppi=150):
    # Makes repeated half-drop version of image of final size width and height (in cm)
    if not inpixels:
        final_w, final_h = cm2pixels(final_w, ppi), cm2pixels(final_h, ppi)
    if img.shape[1] > final_w:
        img = img[:, :final_w]
    if img.shape[0] > final_h:
        img = img[:final_h, :]
    ratio_w, ratio_h = final_w / img.shape[1], final_h / img.shape[0]
    repeat_w, repeat_h = math.ceil(ratio_w), math.ceil(ratio_h)
    height, width = img.shape[:2]
    big_w, big_h = math.ceil(final_w / ratio_w * repeat_w), math.ceil(final_h / ratio_h * repeat_h)
    result_big = np.zeros((big_h, big_w, img.shape[2]), dtype=np.uint8)

    for i in range(repeat_h):
        for j in range(repeat_w):
            if j % 2 == 0:
                result_big[i*height:(i+1)*height, j*width:(j+1)*width] = img
            else:
                #start gambiarra nivel hard
                if(height % 2 != 0): 
                    height1 = height + 1
                    result_big[i*height:int((i + 0.5)*height), j*width:(j+1)*width] = img[height1//2:, :]
                    result_big[int((i + 0.5)*height):(i+1)*height, j*width:(j+1)*width] = img[:height1//2, :]
                height1 = height + 1
                result_big[i*height:int((i + 0.5)*height), j*width:(j+1)*width] = img[height1//2:, :]
                result_big[int((i + 0.5)*height):(i+1)*height, j*width:(j+1)*width] = img[:height1//2, :]
                
    result = result_big[:final_h, :final_w]
    return result

def make_repeat_halfbrick(img, final_w, final_h, inpixels=False, ppi=150):
    # Makes repeated half-brick version of image of final size width and height (in cm)
    if not inpixels:
        final_w, final_h = cm2pixels(final_w, ppi), cm2pixels(final_h, ppi)
    if img.shape[1] > final_w:
        img = img[:, :final_w]
    if img.shape[0] > final_h:
        img = img[:final_h, :]
    ratio_w, ratio_h = final_w / img.shape[1], final_h / img.shape[0]
    repeat_w, repeat_h = math.ceil(ratio_w), math.ceil(ratio_h)
    height, width = img.shape[:2]
    big_w, big_h = math.ceil(final_w / ratio_w * repeat_w), math.ceil(final_h / ratio_h * repeat_h)
    result_big = np.zeros((big_h, big_w, img.shape[2]), dtype=np.uint8)
    for i in range(repeat_h):
        for j in range(repeat_w):
            if i % 2 == 0:
                result_big[i*height:(i+1)*height, j*width:(j+1)*width] = img
                
            elif width % 2 != 0:
                width1 = width + 1
                result_big[i*height:(i+1)*height, j*width:int((j + 0.5)*width)] = img[:, width1//2:]
                result_big[i*height:(i+1)*height, int((j + 0.5)*width):(j+1)*width] = img[:, :width1//2]
                
            else:    
                result_big[i*height:(i+1)*height, j*width:int((j + 0.5)*width)] = img[:, width//2:]
                result_big[i*height:(i+1)*height, int((j + 0.5)*width):(j+1)*width] = img[:, :width//2]
                
    result = result_big[:final_h, :final_w]
    return result

def make_repeat_center(img, final_w, final_h, inpixels=False, ppi=150):
    if not inpixels:
        final_w, final_h = cm2pixels(final_w, ppi), cm2pixels(final_h, ppi)
    if img.shape[1] > final_w:
        img = img[:, :final_w]
    if img.shape[0] > final_h:
        img = img[:final_h, :]
    height, width = img.shape[:2]
    result = np.ones((final_h, final_w, img.shape[2]), dtype=np.uint8) * 255
    base_w, base_h = (final_w - width) // 2, (final_h - height) // 2
    result[base_h:base_h+height, base_w:base_w+width] = img
    return result

def make_repeat_mirror(img, final_w, final_h, inpixels=False, ppi=150):
    # Makes repeated mirror version of image of final size width and height (in cm)
    if not inpixels:
        final_w, final_h = cm2pixels(final_w, ppi), cm2pixels(final_h, ppi)
    if img.shape[1] > final_w:
        img = img[:, :final_w]
    if img.shape[0] > final_h:
        img = img[:final_h, :]
    ratio_w, ratio_h = final_w / img.shape[1], final_h / img.shape[0]
    repeat_w, repeat_h = math.ceil(ratio_w), math.ceil(ratio_h)
    height, width = img.shape[:2]
    big_w, big_h = math.ceil(final_w / ratio_w * repeat_w), math.ceil(final_h / ratio_h * repeat_h)
    result_big = np.zeros((big_h, big_w, img.shape[2]), dtype=np.uint8)
    for i in range(repeat_h):
        for j in range(repeat_w):
            if i % 2 == 0:
                if j % 2 == 0:
                    result_big[i*height:(i+1)*height, j*width:(j+1)*width] = img
                else:
                    result_big[i*height:(i+1)*height, j*width:(j+1)*width] = np.flip(img, axis=1)
            else:
                if j % 2 == 0:
                    result_big[i*height:(i+1)*height, j*width:(j+1)*width] = np.flip(img, axis=0)
                else:
                    result_big[i*height:(i+1)*height, j*width:(j+1)*width] = np.flip(img, axis=(0,1))
    result = result_big[:final_h, :final_w]
    return result

REPEAT_LIST = {'basic': make_repeat_basic, 'halfdrop': make_repeat_halfdrop, 
                'halfbrick': make_repeat_halfbrick, 'center': make_repeat_center,
                'mirror': make_repeat_mirror}


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].upper() in ALLOWED_EXTENSIONS

def get_image_ppi(filename):
    img = Image.open(filename)
    return img.info['dpi'][0] if 'dpi' in img.info else 150

def read_image(img_name):
    img = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
    if len(img.shape) < 3:
        img = np.repeat(img[..., None], 3, axis=2)
    if img.shape[2] < 4:
        b, g, r = cv2.split(img)
        alpha = np.ones(b.shape, dtype=b.dtype) * 255
        img = cv2.merge((b, g, r, alpha))
    return img

def pixels2cm(pixels, ppi=STD_PPI):
    return 2.54*(pixels / ppi)

def cm2pixels(cm, ppi=STD_PPI):
    return int(cm / 2.54 * ppi)


def repeat_filename(filename, repeat_name):
    filename, ext = '.'.join(filename.split('.')[:-1]), filename.split('.')[-1]
    filename = f'{filename}_{repeat_name}.{ext}'
    return filename

def create_repeats(filename, folder):
    img = read_image(os.path.join(folder, filename))
    ppi = get_image_ppi(os.path.join(folder, filename))
    for repeat_name in REPEAT_LIST:
        curr = REPEAT_LIST[repeat_name](img, 140, 100, ppi=ppi)
        curr_filename = repeat_filename(filename, repeat_name)
        print(curr_filename)
        cv2.imwrite(os.path.join(folder, curr_filename), curr)


