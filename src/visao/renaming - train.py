import os

os.chdir("Dataset/dataset/training/Dairy product")

for file in os.listdir(os.getcwd()):
    print(file)
    os.rename(file, "train_" + file)



