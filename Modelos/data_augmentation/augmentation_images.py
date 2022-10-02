# Cargar Librerias

import matplotlib.pyplot as plt 
from keras.utils import img_to_array

from keras.preprocessing.image import ImageDataGenerator
from keras.applications.imagenet_utils import preprocess_input

from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout, BatchNormalization, Input

import os


#Leer imagen a partir de una url
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import UnidentifiedImageError

import requests
from io import BytesIO

import shutil

images_directory = "D:\\Desktop\myProjects\images_scrapping_17-08-22"
# images_directory = "D:\\Desktop\myProjects\exampleImages"

class_list = os.listdir(images_directory)
path_list = [os.path.join(images_directory,  x) for x in class_list]
path_dict = dict(zip(class_list, path_list))

num_classes = len(class_list)
width_shape = 448
height_shape = 448
epochs = 20
batch_size = 32

# Augmentation

train_datagen = ImageDataGenerator(rotation_range=40,
width_shift_range=0.2,
height_shift_range=0.2,
zoom_range=0.3,
horizontal_flip=False,
fill_mode='nearest',
brightness_range=[0.4,1.5]
    # preprocessing_function=preprocess_input
)


# Creación de modelo 
nb_train_samples = 9544
model = Sequential()

inputShape = (height_shape, width_shape, 3)
model.add(Conv2D(32,(3,3), input_shape=inputShape))
model.add(Conv2D(32,(3,3)))
model.add(MaxPool2D())
          
model.add(Conv2D(64,(3,3)))
model.add(Conv2D(64,(3,3)))
model.add(Conv2D(64,(3,3)))
model.add(MaxPool2D())

model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(num_classes,activation='softmax', name='output'))

model.summary()

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])


for image_class, path in path_dict.items():
    # Get images path
    images_list = os.listdir(path)
    print(images_list)
    # Remove possible new empty folders
    if images_list == []:
        os.rmdir(path)
        continue

    images_path_list = [os.path.join(path,  x) for x in images_list]
    images_path_dict = dict(zip(images_list, images_path_list))

    # Create sub directory as a sub class
    new_path = os.path.join(path, image_class)
    os.mkdir(new_path)


    # Move images into sub class
    for image, sub_image_path in images_path_dict.items():
        # Delete folders and no png files
        aux_image = image.split(".")
        if len(aux_image) == 1:
            os.rmdir(sub_image_path)
            continue
        if aux_image[-1] != "png":
            os.remove(sub_image_path)
            continue
        try:
            Image.open(sub_image_path)
        except:
            os.remove(sub_image_path)
            continue
        # Get new image path
        new_image_path = os.path.join(new_path, image)
        # Move image
        os.replace(sub_image_path, new_image_path)

    # Remove possible new empty folders
    images_list = os.listdir(new_path)
    if images_list == []:
        os.rmdir(new_path)
        os.rmdir(path)
        continue

    # Get images from directory and feed image array information
    train_generator = train_datagen.flow_from_directory(  
            path,
            target_size=(width_shape, height_shape),
            batch_size=batch_size,
            save_to_dir=new_path,
            keep_aspect_ratio=True,
            class_mode='categorical')

    # Train model
    model.fit(  
        train_generator,
        epochs=epochs,
        batch_size=batch_size)
    
    # Move tickets back to origin directory
    min_level_images_list = os.listdir(new_path)
    min_level_path_list = [os.path.join(new_path,  x) for x in min_level_images_list]
    def_images_path_list = [os.path.join(path,  x) for x in min_level_images_list]
    def_path_dict = dict(zip(min_level_path_list, def_images_path_list))

    for path, def_path in def_path_dict.items():
        os.replace(path, def_path)
    
    # Remove temporal sub class
    os.rmdir(new_path)




