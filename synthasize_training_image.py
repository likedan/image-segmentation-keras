import cv2
import numpy as np
import os
import random
from random import randint

def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src

testing_images = os.listdir("data/testing_images")
texture_images = os.listdir("data/texture")
texture_images.remove(".DS_Store")

image_size = 500
edge = 50

for file in os.listdir("data/mask_image"):
    file = file.replace(".jpg", ".png")
    if file == ".DS_Store" or file in testing_images :
        continue
    print(file)

    bg_img = None
    while bg_img is None:
        bg_img = cv2.imread("data/texture/" + random.choice(texture_images))
        x, y = bg_img.shape[:2]
        if x - 2 * edge - image_size < 0 or y - 2 * edge - image_size < 0:
            bg_img = None
    overlay_t_img = cv2.imread("data/alpha_image/" + file, -1)

    x_begin = randint(edge, x - edge - image_size)
    y_begin = randint(edge, y - edge - image_size)

    crop_img = bg_img[x_begin: x_begin + 500, y_begin:y_begin + 500]

    result = transparentOverlay(crop_img, overlay_t_img)
    cv2.imwrite("data/training_images/" + file, result)

    b_channel, g_channel, r_channel, a_channel = cv2.split(overlay_t_img)
    a_channel = a_channel / 255

    annotation = np.array([a_channel,a_channel,a_channel]).transpose()
    cv2.imwrite("data/training_images_annotation/" + file, annotation)
