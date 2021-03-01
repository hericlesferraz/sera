import os

os.chdir("Ensaio Fotográfico/todas")

for filename in os.listdir(os.getcwd()):
    print(filename)
    number = int(filename[:-4])
    new_number = 1000 + number
    new_filename = str(new_number) + ".jpg"
    os.rename(filename, new_filename)



