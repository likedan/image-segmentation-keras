import cv2
import numpy as np
import os

def convert(img_file):
    origin_img = cv2.imread(os.path.join("data/test_images", img_file))

    x, y = origin_img.shape[:2]
    edge = 100
    img = np.zeros((edge * 2 + x, edge * 2 + y, 3), np.uint8)
    img += 255
    img[edge : edge + x, edge: edge + y] = origin_img
    mask = np.zeros(img.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    rect = (1, 1, 665, 344)
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    b_channel, g_channel, r_channel = cv2.split(img)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255

    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    img_BGRA = img_BGRA * mask2[:, :, np.newaxis]
    return img, img_BGRA

for file in os.listdir("data/test_images"):
    if file == ".DS_Store":
        continue
    mask_img, alpha_image = convert(file)
    cv2.imwrite("data/mask_image/" + file, mask_img)
    cv2.imwrite("data/alpha_image/" + file.replace(".jpg", ".png"), alpha_image)
