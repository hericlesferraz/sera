import os

os.chdir("manteiga")
cont = 1000

for file in os.listdir(os.getcwd()):
    print(file)
    os.rename(file, str(cont) + ".jpg")
    cont += 1



