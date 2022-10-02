import matplotlib.pyplot as plt 

import tensorflow as tf

from keras import optimizers
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.vgg16 import VGG16
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from keras.models import Sequential, Model
from keras.preprocessing import image
from keras.utils import image_dataset_from_directory, load_img, img_to_array

from keras import layers

from PIL import Image

import numpy as np

# from ticket_recognition.remove_bg_and_super_resolution import delete_background

# from ticket_recognition.remove_bg_and_super_resolution

# from singleton import SingletonMeta

import os

class Recognize_Products_Images:
    
    def __init__(
        self,
        base_path: str,
        environment: str = "production",
    ) -> None:

        self.width_shape = 224
        self.height_shape = 224
        self.epochs = 10
        self.batch_size = 32 
        self.base_path = base_path
        self.def_product_list = []
        self.image_path = ""
        self.model_weights_path = "product_recognition/model_weights.h5"
        
        assert environment in ["local", "production"]
        self.environment = environment

    @property
    def class_names(self):
        return os.listdir(self.base_path)

    @property
    def num_classes(self):
        return len(self.class_names)


    def set_image_path(self, image_path: str) -> None:
        """Set the image path"""
        self.image_path = image_path

    def set_model_weights_path(self, model_weights_path: str) -> None:
        """"""
        self.model_weights_path = model_weights_path

    # Predict image label
    def run(self) -> str:
        """Run method.

        Returns: 
            str: list with the products as cleaned as possible.
        """

        if self.environment == "local":
            return self._local_run()

        product = self.predict_label()
        self.def_product_list.append(product)

        return self.def_product_list

    def _local_run(self) -> str:
        """Run method in local environments.
        
        Returns: 
            str: list with the products as cleaned as possible.
        """
        
        checker = input("Deseas entrenar el modelo?: si o no - ")
        while checker != "si" and checker != "no":
            checker = input("Valor no contemplado. Por favor, introduce si desea entrenar el modelo: si o no - ")

        if checker == "si":
            if os.path.exists(self.model_weights_path) == False:
                self.train_model()

            else:
                checker = input("Ya existe un modelo en la actualidad, sigue queriendo reentrenarlo?: si o no - ")
                while checker != "si" and checker != "no":
                    checker = input("Valor no contemplado. Por favor, introduce si desea reentrenar el modelo: si o no - ")

                if checker == "si":
                    self.train_model()

        # Predicción de imagenes
        print("[PREDICCIÓN DE IMÁGENES]:")
        self.image_path = input("Introduce el enlace de la imagen del producto: ")
        # no_bg_path = delete_background(self.image_path)
        product = self.predict_label()
        self.def_product_list.append(product)

        checker = input("Quieres subir otro producto?: si o no - ")
        while checker != "si" and checker != "no":
            checker = input("Valor no contemplado. Por favor, introduce si desea o no cargar otro producto: si o no - ")

        if checker == "si":
           self._local_run()

        return self.def_product_list

    # Training Model
    def train_model(self):
        """"""
        dataset = self.get_data_from_directory()
        model = self.set_up_training_model()

        X_train = np.concatenate([x for x, y in dataset], axis=0)
        y_train = np.concatenate([y for x, y in dataset], axis=0)

        lr_reduce = ReduceLROnPlateau(monitor='val_accuracy', factor=0.6, patience=8, verbose=1, mode='max', min_lr=5e-5)
        checkpoint = ModelCheckpoint('vgg16_finetune.h15', monitor= 'val_accuracy', mode= 'max', save_best_only = True, verbose= 1)

        model.fit(
            X_train,
            y_train,
            epochs=30,
            batch_size=15,
            validation_split=0.2,
            callbacks=[lr_reduce,checkpoint],
        )

        model.save_weights(self.model_weights_path)
    
    # Predict product label
    def predict_label(self):
        """Predict the label for a product image"""

        # Set model and load weights
        model = self.set_up_training_model()
        model.load_weights(self.model_weights_path)

        # Load and preprocess image
        img = load_img(self.image_path, target_size=(224, 224))
        img = img_to_array(img)
        img = np.reshape(img, (-1, 224, 224, 3))
        img = preprocess_input(img)

        # Get the label
        y_prob = model.predict(img)
        label = y_prob.argmax(axis=-1)
        lista = clase.class_names
        lista.sort()
        label_name = lista[label[0]]
        print(label_name)
        return label_name


    def get_data_from_directory(self) -> tf.data.Dataset:
        """Get data from a directory.
        
        Returns: 
            tf.data.Dataset: products dataset.
        """
        return image_dataset_from_directory(
            directory=self.base_path,
            labels="inferred",
            label_mode="categorical",
            class_names = self.class_names,
            image_size=(self.width_shape, self.height_shape),
            batch_size=self.batch_size,
        )
    
    def set_up_training_model(self):
        """"""

        baseModel = VGG16(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

        headModel = baseModel.output
        headModel = layers.Flatten(name="flatten")(headModel)
        headModel = layers.Dense(512, activation="relu")(headModel)
        headModel = layers.Dropout(0.5)(headModel)
        headModel = layers.Dense(256, activation='relu')(headModel)
        headModel = layers.Dense(self.num_classes, activation="softmax")(headModel)

        vgg_model = Model(inputs=baseModel.input, outputs=headModel)

        # for layer in baseModel.layers:
        #     layer.trainable = False
        for layer in vgg_model.layers[:15]:
            layer.trainable = False

        learning_rate= 0.00005

        vgg_model.compile(optimizers.Adam(lr=learning_rate), loss="categorical_crossentropy", metrics=["accuracy"])

        return vgg_model
       

###### Set vars ######
images_directory = "D:\\Desktop\myProjects\exampleImages"

clase = Recognize_Products_Images(images_directory, "local")

print(clase.def_product_list)


