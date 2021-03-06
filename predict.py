import argparse
import LoadBatches
import glob
import cv2
import numpy as np
import random
import VGGUnet
from keras import Model

parser = argparse.ArgumentParser()
parser.add_argument("--save_weights_path", type=str, default="weights/r")
parser.add_argument("--epoch_number", type=int, default=6)
parser.add_argument("--test_images", type=str, default="../result/to_test/")
parser.add_argument("--output_path", type=str, default="../result/5/")
parser.add_argument("--input_height", type=int, default=224)
parser.add_argument("--input_width", type=int, default=224)
parser.add_argument("--n_classes", type=int, default=2)
parser.add_argument("--model_name", type=str, default="vgg_segnet")

args = parser.parse_args()

n_classes = args.n_classes
model_name = args.model_name
images_path = args.test_images
input_width = args.input_width
input_height = args.input_height
epoch_number = args.epoch_number

# modelFns = { 'vgg_segnet': NNModels.VGGSegnet.VGGSegnet , 'vgg_unet': NNModels.VGGUnet.VGGUnet , 'vgg_unet2': NNModels.VGGUnet.VGGUnet2 , 'fcn8': NNModels.FCN8.FCN8 , 'fcn32': NNModels.FCN32.FCN32}
modelFN = VGGUnet.VGGUnet

m = modelFN(n_classes, input_height=input_height, input_width=input_width)
m.load_weights(args.save_weights_path + "." + str(epoch_number))
m.compile(loss='categorical_crossentropy',
          optimizer='adadelta',
          metrics=['accuracy'])

output_height = m.outputHeight
output_width = m.outputWidth

images = glob.glob(images_path + "*.jpg") + glob.glob(images_path + "*.png") + glob.glob(images_path + "*.jpeg")
images.sort()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(n_classes)]

for imgName in images:
    outName = imgName.replace(images_path, args.output_path)
    X = LoadBatches.getImageArr(imgName, args.input_width, args.input_height)
    pr = m.predict(np.array([X]))[0]

    model2 = Model(input=m.input, output=m.layers[-3].output)
    pr2 = model2.predict(np.array([X]))[0]

    print(pr, pr2)

    opr = pr
    pr = pr.reshape((output_height, output_width, n_classes)).argmax(axis=2)
    seg_img = np.zeros((output_height, output_width, 3))
    for c in range(n_classes):
        seg_img[:, :, 0] += ((pr[:, :] == c) * (colors[c][0])).astype('uint8')
        seg_img[:, :, 1] += ((pr[:, :] == c) * (colors[c][1])).astype('uint8')
        seg_img[:, :, 2] += ((pr[:, :] == c) * (colors[c][2])).astype('uint8')
    seg_img = cv2.resize(seg_img, (input_width, input_height))
    cv2.imwrite(outName, seg_img)

    original_img = cv2.imread(imgName)
    opr = opr.reshape((output_height, output_width, n_classes))
    original_img = cv2.resize(original_img, (opr.shape[0], opr.shape[1]),interpolation=cv2.INTER_CUBIC)
    b_channel, g_channel, r_channel = cv2.split(original_img)
    b_channel = b_channel.astype(np.float)
    g_channel = g_channel.astype(np.float)
    r_channel = r_channel.astype(np.float)
    alpha_channel = (opr[:,:,1] * 255).astype(np.float)
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    cv2.imwrite(outName.replace(".png","1.png").replace(".jpg",".png"), img_BGRA)
