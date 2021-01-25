import os

os.chdir("Dataset/dataset/validation/Dairy product")

for file in os.listdir(os.getcwd()):
    print(file)
    os.rename(file, "val_" + file)



