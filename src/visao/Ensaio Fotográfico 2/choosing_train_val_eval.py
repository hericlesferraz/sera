from random import shuffle
import os

os.chdir("manteiga")
lista_imagens = (os.listdir(os.getcwd()))

lista_imagens_randomizada = lista_imagens.copy()
shuffle(lista_imagens_randomizada)

print(lista_imagens_randomizada)

# Imagens de treino
lista_train = lista_imagens_randomizada[:338]
print(len(lista_train))

# Imagens de validação
lista_val = lista_imagens_randomizada[338:392]
print(len(lista_val))

# Imagens de evaluation
lista_eval = lista_imagens_randomizada[392:]
print(len(lista_eval))

# Renomeando as imagens
for filename in lista_imagens:
    print(filename)

    if filename in lista_train:
        os.rename(filename, "train_" + filename)

    elif filename in lista_val:
        os.rename(filename, "val_" + filename)

    elif filename in lista_eval:
        os.rename(filename, "eval_" + filename)
   