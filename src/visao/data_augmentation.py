import cv2
import os

# Fazendo uma lista com o caminho relativo de todos os arquivos que passarão por Data Augmentation
lista_eval = os.listdir('Dataset/dataset/evaluation/Dairy product')
for count in range(len(lista_eval)):
    lista_eval[count] = os.path.join('Dataset/dataset/evaluation/Dairy product', lista_eval[count])

print(lista_eval)
print()

lista_train = os.listdir('Dataset/dataset/training/Dairy product')
for count in range(len(lista_train)):
    lista_train[count] = os.path.join('Dataset/dataset/training/Dairy product', lista_train[count])

print(lista_train)
print()

lista_val = os.listdir('Dataset/dataset/validation/Dairy product')
for count in range(len(lista_val)):
    lista_val[count] = os.path.join('Dataset/dataset/validation/Dairy product', lista_val[count])

print(lista_val)
print()

lista_all_files = lista_eval + lista_train + lista_val
print(lista_all_files)
print()

# Espelhando todos as imagens horizontalmente
for image in lista_all_files:
    image_numpy = cv2.imread(image)
    image_numpy_flipped = cv2.flip(image_numpy, 1)

    new_image_filepath = image[:-4] + "_flipped" + ".jpg"
    print(new_image_filepath)
    cv2.imwrite(new_image_filepath, image_numpy_flipped)
