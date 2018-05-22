import os
from shutil import copyfile


# pruned_files = os.listdir("../data/testing_images/")
# all_files = os.listdir("../data/training_images/")
#
# missing_files = list(set(all_files) - set(pruned_files))
# for file in missing_files:
#     file = file.replace(".jpg", ".png")
#     os.rename("../data/alpha_image/"+file, "../data/sample_bad_images/"+file)

#
# to_move_files = os.listdir("../data/bad_images/")
#
# for file in to_move_files:
#     copyfile("../data/alpha_image/"+file, "../data/sample_bad_images/"+file)

# to_remove_files = os.listdir("../data/bad_images/")
# for file in to_remove_files:
#     if os.path.exists("../data/alpha_image/"+file.replace(".png",".jpg")):
#         os.remove("../data/alpha_image/"+file.replace(".png",".jpg"))

#
# img = cv2.imread("../data/training_images_annotation/00a00cbc8bab03a9d90eaca812b410cd879a3834.png")
# img *=255
# cv2.imshow("img", img)
# cv2.waitKey(0)

pruned_files = os.listdir("../data/testing_images/")
all_files = os.listdir("../data/training_images/")
print(len(list(set(all_files).union(set(pruned_files)))))
print(len(all_files) + len(pruned_files))
