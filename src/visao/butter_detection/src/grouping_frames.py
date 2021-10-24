import os

##### Dataset Categories #####
# 70% train (0,7 * 605 = 424)
# 20% validation (0,2 * 605 = 121)
# 10% evaluation (0,1 * 605 = 60)
#####
    
os.chdir("../dataset/frames")
list_of_files = os.listdir(os.getcwd())

current_image = 0
for a_file in list_of_files:
    
    if current_image < 424:
        os.rename(a_file, "train_" + str(current_image) + ".jpg")

    elif current_image < 545:
        os.rename(a_file, "valid_" + str(current_image) + ".jpg")

    else:
        os.rename(a_file, "eval_" + str(current_image) + ".jpg")
    
    current_image += 1