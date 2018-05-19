import cv2
import numpy as np
import os

def convert(dir, img_file):
    img = cv2.imread(os.path.join(dir, img_file))
    mask = np.zeros(img.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    rect = (1, 1, 665, 344)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    return img

for path, _ ,files in os.walk("data/ut-zap50k-images"):
    for file in files:
        img = convert(path, file)
        cv2.imwrite("data/alpha_image/" + path.replace("/","-") + "-" + file.replace(".jpg", ".png"), img)
