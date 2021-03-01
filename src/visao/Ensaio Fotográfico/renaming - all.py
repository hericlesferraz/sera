import os

os.chdir("Ensaio Fotográfico/manteiga2")
cont = 177

for file in os.listdir(os.getcwd()):
    print(file)
    os.rename(file, str(cont) + ".jpg")
    cont += 1



