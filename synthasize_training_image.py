import cv2
import numpy as np
import os
import random


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

texture_images = os.listdir("data/texture")

for file in os.listdir("data/mask_image"):
    if file == ".DS_Store":
        continue
    file = file.replace(".jpg", ".png")
    bg_img = cv2.imread("data/texture/" + random.choice(texture_images))
    overlay_t_img = cv2.imread("data/alpha_image/" + file, -1)
    x, y = overlay_t_img.shape[:2]
    x_begin = int((x - 500) / 2)
    y_begin = int((y - 500) / 2)

    crop_img = bg_img[x_begin: x_begin + 500, y_begin:y_begin + 500]

    result = transparentOverlay(crop_img, overlay_t_img)
    cv2.imwrite("data/training_images/" + file, result)