import pandas as pd
import numpy as np
import re
import string
from typing import List
from googletrans import Translator


class Recommender:

    def __init__(self, df_receipes_path, df_ingredient_translation_path, products_recognized_list) -> None:
        self.df_receipes_path = df_receipes_path
        self.df_ingredient_translation_path = df_ingredient_translation_path
        self.products_recognized_list = products_recognized_list

    @property
    def df_receipes(self):
        df = pd.read_json(self.df_receipes_path)
        return df.dropna(subset=['ingredients'])

    @property
    def df_ingredients(self):
        return pd.read_csv(self.df_ingredient_translation_path, sep="|")

    @property
    def english_list(self):
        return self.df_ingredients["English"].tolist()

    @property
    def spanish_list(self):
        return self.df_ingredients["Spanish"].tolist()

    @property
    def translation_dict(self):
        return dict(zip(self.english_list, self.spanish_list))

    def run(self):
        """"""
        normalized_list = self.normalize_products()
        translated_list = self.translate_products(normalized_list)
        df_top_5 = self.get_top_5_receipes(translated_list)
        return self.translate_df(df_top_5)

    def normalize_products(self):
        """"""
        return_list = []
        for i, product in enumerate(self.products_recognized_list):
            # Casuistica de producto de una sola palabra que se encuentra exactamente igual en la lista
            if product in self.spanish_list:
                return_list.append(product)
                continue

            splitted_product = product.split(" ")

            # Casuistica producto con mas de una palabra
            if len(splitted_product) > 1:
                # Se comprueba que la primera palabra del producto exista en la lista de productos normalizados
                if splitted_product[0] in self.spanish_list:
                    return_list.append(splitted_product[0])
                # Se comprueba que si el producto igual pero escrito en otro orden y si es asi se sobreescribe
                for item in self.spanish_list:
                    counter = 0
                    splitted_item = item.split(" ")
                    for word in splitted_product:
                        if word in splitted_item:
                            counter += 1
                    if counter == len(splitted_product) and counter == len(splitted_item):
                        return_list.append(item)
                        break
                continue
        return return_list

    def translate_products(self, normalized_list):
        """"""
        return_list = []
        for key, value in self.translation_dict.items():
            for product in normalized_list:
                if product == value:
                    return_list.append(key)
        return return_list

    def match_ingredients(self, translated_list, ingredient_list):
        """"""
        if not isinstance(ingredient_list, List):
            return 0
        elif len(ingredient_list) == 0:
            return 0
        counter = 0
        for ingredient in ingredient_list:
            splitted_ingredient = ingredient.split(" ")
            for product in translated_list:
                if product in splitted_ingredient:
                    counter += 1
                    break
                else:
                    splitted_product = product.split(" ")
                    if len(splitted_product) > 1:
                        sub_counter = 0
                        for word in splitted_product:
                            if word in splitted_ingredient:
                                sub_counter += 1
                        if sub_counter == len(splitted_product):
                            counter+=1
                            break
                        else:
                            if splitted_product[0] in splitted_ingredient:
                                counter+=1
        return int(counter)

    def get_top_5_receipes(self, product_list):
        """"""
        df = self.df_receipes
        df["score"] = self.df_receipes["ingredients"].apply(lambda x: self.match_ingredients(product_list, x))
        df.sort_values(by=["score", "rating"], ascending=False, inplace=True)
        return df.iloc[0:5]

    def translate_cell(self, cell_value, translator):
        if isinstance(cell_value, List):
            aux_list = []
            for word in cell_value:
                translated_text = translator.translate(word, src='en', dest='es')
                aux_list.append(translated_text.text)
            return aux_list
        elif isinstance(cell_value, str):
            translated_text = translator.translate(cell_value, src='en', dest='es')
            return translated_text.text
        else:
            return cell_value

    def translate_df(self, df):
        translator = Translator()
        col_list = []
        for col in df.columns:
            translated_text = translator.translate(col, src='en', dest='es')
            col_list.append(translated_text.text)
        df.columns = col_list

        for col in df.columns:
            if df[col].dtype != "object":
                continue
            df[col] = df[col].apply(lambda x: self.translate_cell(x, translator))
        return df

lista = ['CARREFOUR MARKET', 'CONDE PENALVER  MADRID  ', 'CLUB', 'VIENES', 'CARREFOURESCLUBCARREFOUR', 'SUPERMERCADOS CHAMPION', 'CIF', 'TELEFONO TIENDA ', 'ATENCION CLIENTE  ', 'GALLETA CREMA', 'YOGUR LIQUIDO FRESA', 'CORAZON LECHUGA', 'ART TOTAL PAGAR', 'BASE', 'TIPO', 'VENTA', 'MASTERCARD', 'XXXXXXXXXXXX', 'IMPORTE', 'EUR', 'NRF', 'CUOTA', 'CONTACTLESS FIRMA NECESARIA', 'TODOS LOS IMPORTES SON EUR', 'CAMBIO RECIBIDO', 'DISPONE  DIAS PARA DEVOLUCIONES', 'DESCUBRE TODAS LAS VENTAJAS', 'LA TARJETA PASS', 'WWWPASSCARREFOURES', '  ', 'ATENDIO CLS', 'CARFOURUR EXPRESS', 'PLMANUEL ECERRRA  MADRID', 'TEL ATENCIÓN CLIENTE', ' PVP IVA INCLUIDO ', 'CHAMPU MENTHOL', 'PATATA PREFRITA', 'TOMATE BOLA', 'TIPO', 'ART TOTAL PAGAR', 'VENTA', 'DEBIT MASTERCARD', 'XXXXXXXXXXXX', '', 'IMPORTE EUR', '', 'BASE', 'CUOTA', 'CONTACTLESS FIRMA NECESARIA', 'TODOS LOS IMPORTES SON EUR']
lista = list(map(str.lower, lista))
clase = Recommender("recommender_system/full_format_recipes.json", "recommender_system\diccionario_ingredientes.csv", lista)

df = clase.run()

print(df.head(10))