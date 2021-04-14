import numpy as np
import cv2 as cv

def edit_hsv(img, dh=-5, ds=20, dv=0):
    def add(x, dx):
        return np.clip(x+dx, 0, 255)
    imghsv = cv.cvtColor(img, cv.COLOR_BGR2HSV).astype("float32")
    (h, s, v) = cv.split(imghsv)
    h = add(h, dh)
    s = add(s, ds)
    v = add(v, dv)
    imghsv = cv.merge([h,s,v])
    return cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)

def edit_rgb(img, dr=(240, 255), dg=(255, 210), db=(140, 255)):
    def scale(arr, old, new):
        table = np.array([min(max(float(i)*new/old, 0), 255)
            for i in range(256)]).astype("uint8")
        return cv.LUT(arr, table)
    b, g, r = cv.split(img)
    b = scale(b, db[0], db[1])
    g = scale(g, dg[0], dg[1])
    r = scale(r, dr[0], dr[1])
    return cv.merge([b, g, r])


def edit_brightness(img, alpha=1.3, beta=0):
    result = img.copy()
    cv.convertScaleAbs(img, result, alpha, beta)
    return adjust_gamma(result)

def adjust_gamma(image, gamma=1.8):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
 
    # apply gamma correction using the lookup table
    return cv.LUT(image, table)

def white_balance(img):
    result = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv.cvtColor(result, cv.COLOR_LAB2BGR)
    return result

def fix_cols(img):
    return edit_brightness(edit_hsv(edit_rgb(img, db=(110, 255), dr=(230, 255))))

def debayer_ximea(img):
    return fix_cols(cv.cvtColor(img, cv.COLOR_BayerRG2BGR))



    
