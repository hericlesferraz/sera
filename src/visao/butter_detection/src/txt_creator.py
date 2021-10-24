import os

os.chdir("../dataset/frames")

list_of_files = os.listdir(os.getcwd())

with open("valid.txt", "w") as f:
    for item in list_of_files:

        if ("valid" in item) and (".jpg" in item):
            f.write("data/obj/" + item + "\n")


