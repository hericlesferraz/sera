from os.path import expanduser, join
import os

home = expanduser("~")
image_folder = join(home, "darknet/build/darknet/x64/data/obj")
image_list = os.listdir(image_folder)
image_list_path = []

training_image_list = []
validation_image_list = []

for file in image_list:
    if '.jpg' in file:
        image_list_path.append(os.path.join("data/obj", file))

for image_file in image_list_path:
    if 'train' in image_file:
        training_image_list.append(image_file)
        continue

    if ('val' in image_file) and ('eval' not in image_file):
        validation_image_list.append(image_file)

print(len(validation_image_list))
print(validation_image_list)

###### Escrevendo o arquivo com as imagens de treino
with open("train.txt", "w") as file:
    for image in training_image_list:
        file.write(image + "\n")

###### Escrevendo o arquivo com as imagens de validação
with open("valid.txt", "w") as file:
    for image in validation_image_list:
        file.writelines(image + "\n")