import os
import cv2
# pruned_files = os.listdir("../data/training_images/")
# all_files = os.listdir("../data/training_images_annotation/")
#
# missing_files = list(set(all_files) - set(pruned_files))
# for file in missing_files:
#     os.rename("../data/training_images_annotation/"+file, "../data/bad_images/"+file)



to_move_files = os.listdir("../data/testing_images_annotation/")

for file in to_move_files:
    os.rename("../data/training_images/"+file, "../data/testing_images/"+file)

# to_remove_files = os.listdir("../data/bad_images/")
# for file in to_remove_files:
#     if os.path.exists("../data/alpha_image/"+file.replace(".png",".jpg")):
#         os.remove("../data/alpha_image/"+file.replace(".png",".jpg"))

#
# img = cv2.imread("../data/training_images_annotation/00a00cbc8bab03a9d90eaca812b410cd879a3834.png")
# img *=255
# cv2.imshow("img", img)
# cv2.waitKey(0)