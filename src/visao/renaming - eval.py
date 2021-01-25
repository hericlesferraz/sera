import os

os.chdir("Dataset/dataset/evaluation/Dairy product")

for file in os.listdir(os.getcwd()):
    print(file)
    os.rename(file, "eval_" + file)



