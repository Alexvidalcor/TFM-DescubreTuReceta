import io

import os

import re

from google.protobuf.json_format import MessageToDict

from google.cloud import vision

from google.cloud.vision_v1 import types

from typing import List

from singleton import SingletonMeta

from ticket_recognition.remove_bg_and_super_resolution import delete_background, super_resolution

class Recognize_Tickets_Products(metaclass = SingletonMeta):
    
    def __init__(
        self,
        credentials_path: str,
        environment: str = "production"
    ) -> None:

        self.credentials_path = credentials_path
        self.image_path = ""
        self.super_resolution_model_path = ""
        self.def_product_list = []
        
        assert environment in ["local", "production"]
        self.environment = environment


    def run(self) -> List[str]:
        """Run method.

        Returns: 
            List[str]: list with the products as cleaned as possible.
        """

        if self.environment == "local":
            return self._local_run()
        
        return

    def _local_run(self) -> List[str]:
        """Run method in local environments.
        
        Returns: 
            List[str]: list with the products as cleaned as possible.
        """
        
        self.image_path = input("Introduce el enlace del ticket: ")

        if self.super_resolution_model_path != "":
            no_bg_path = delete_background(self.image_path)
            self.image_path = super_resolution(no_bg_path, self.super_resolution_model_path)

        else:
            checker = input("¿Deseas borrar el background de la imagen y aplicar super resolución?: si o no - ")
            while checker != "si" and checker != "no":
                checker = input("Valor no contemplado. Por favor, introduce si desea o no borrar el background y aplicar super resolución: si o no - ")

            if checker == "si":
                self.super_resolution_model_path = input("Introduce al ruta del modelo: ")
                no_bg_path = delete_background(self.image_path)
                self.image_path = super_resolution(no_bg_path, self.super_resolution_model_path)


        product_list = self.ticket_ocr_recognition()
        self.clean_recognized_products(product_list)
        # product_list = product_list + ticket_ocr_recognition(credentials, image_path)

        if checker == "si":
            os.remove(no_bg_path)
            os.remove(self.image_path)

        checker = input("Quieres subir otro ticket?: si o no - ")
        while checker != "si" and checker != "no":
            checker = input("Valor no contemplado. Por favor, introduce si desea o no cargar otro ticket: si o no - ")

        if checker == "si":
           self._local_run()




    def ticket_ocr_recognition(self):
        """Apply google api for the text ocr recognition to ticket.
        
        Returns: 
            List[str]: list with recognized products.
        """

        # Set the credentials to the google api
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path

        client = vision.ImageAnnotatorClient()

        if self.environment == "local":  # Get image in local environment
            with io.open(self.image_path, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
        else:                            # Get image in production environment
            image = types.Image()
            image.source.image_uri = self.image_path

        # Apply text recognition
        response = client.text_detection(image=image)

        # Get the dictionary with products and relative positions
        texts = MessageToDict(response._pb)

        # Get the products text and split in a list.
        text = texts["textAnnotations"]
        text = text[0]
        text = text["description"]
        text = text.upper()
        text = text.split("\n")

        return text

    def clean_recognized_products(
        self,
        products_list: List[str],
    ) -> List[str]:
        """Clean the recognized products
        
        Args:
            products_list: list with the recognized products.
        """

        # Go through a products_list to clean each product
        for i, item in enumerate(products_list):
            
            # Remove numbers
            new_item = re.sub("\d+", "", item)

            # Remove punctiation marks
            new_item = re.sub("[^\w\s]",'', new_item)

            # Split each item in a list of words
            new_item = new_item.split(" ")

            # Go through each item to remove unneccesary words
            for count, word in enumerate(new_item):
                if len(word) <= 2:
                    new_item.remove(word)
                    count -= 1
                    continue
            

            if new_item == []:  # Check if the resultant new item is empty
                continue
            else:               # Concatenate again all the words and add to def product list
                new_item = " ".join(new_item)
                self.def_product_list.append(new_item)



