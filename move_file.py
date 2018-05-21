import os

# pruned_files = os.listdir("data/training_images/")
# all_files = os.listdir("data/training_images_annotation/")
#
# missing_files = list(set(all_files) - set(pruned_files))
# for file in missing_files:
#     os.rename("data/training_images_annotation/"+file, "data/bad_images/"+file)



to_move_files = os.listdir("data/testing_images/")

for file in to_move_files:
    os.rename("data/training_images_annotation/"+file, "data/testing_images_annotation/"+file)