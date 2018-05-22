import cv2
import numpy as np
import os
import random
from random import randint
import multiprocessing

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

testing_images = os.listdir("../data/testing_images")
training_images = os.listdir("../data/training_images")
bad_images = os.listdir("../data/sample_bad_images")

texture_images = os.listdir("../data/texture")
texture_images.remove(".DS_Store")

image_size = 500
edge = 50
item_rotate_angle = 45
offset = 100

def process_image(file):
    file = file.replace(".jpg", ".png")
    if file == ".DS_Store" or file in testing_images or file in bad_images or file in training_images:
        return
    print(file)

    bg_img = None
    while bg_img is None:
        bg_img = cv2.imread("../data/texture/" + random.choice(texture_images))
        x, y = bg_img.shape[:2]
        if x - 2 * edge - image_size < 0 or y - 2 * edge - image_size < 0:
            bg_img = None

    x_begin = randint(edge, x - edge - image_size)
    y_begin = randint(edge, y - edge - image_size)

    crop_img = bg_img[x_begin: x_begin + image_size, y_begin:y_begin + image_size]
    rotation_matrix = cv2.getRotationMatrix2D((int(image_size / 2), int(image_size / 2)), randint(-15, 15), 1.2)
    crop_img = cv2.warpAffine(crop_img, rotation_matrix, (image_size, image_size))

    overlay_t_img = cv2.imread("../data/alpha_image/" + file, -1)

    H = np.float32([[1, 0, randint(-offset, offset)], [0, 1, randint(-offset, offset)]])
    overlay_t_img = cv2.warpAffine(overlay_t_img, H, (image_size, image_size))  # 需要图像、变换矩阵、变换后的大小

    rotation_matrix = cv2.getRotationMatrix2D((int(image_size / 2), int(image_size / 2)), randint(-item_rotate_angle, item_rotate_angle), 1)
    overlay_t_img = cv2.warpAffine(overlay_t_img, rotation_matrix, (image_size, image_size))
    b_channel, g_channel, r_channel, a_channel = cv2.split(overlay_t_img)
    cv2.imwrite("../data/training_images_annotation/" + file, a_channel / 255)

    result = transparentOverlay(crop_img, overlay_t_img)
    cv2.imwrite("../data/training_images/" + file, result)

files = os.listdir("../data/mask_image")
pool = multiprocessing.Pool()
result = pool.map(process_image, files)