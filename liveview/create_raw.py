import cv2
import numpy as np
img = cv2.imread('flower.png')
def col2bayer(img):
    new = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if i%2 != j%2:
                new[i,j] = img[i,j,1]
            elif i%2:
                new[i,j] = img[i,j,0]
            else:
                new[i,j] = img[i,j,2]
    return new

out = cv2.VideoWriter('raw.avi', 0, 25, (img.shape[1], img.shape[0]), False)
for i in range(1, 1001):
    img2 = img.copy()
    cv2.putText(img2, '{}/{}'.format(i, 1000), (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, 8);
    out.write(col2bayer(img2))
    print(i)
    

