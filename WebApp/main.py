
# Importación de librerías principales
from flask import Flask, render_template, request, redirect, url_for, session
request
from flask_mobility import Mobility

import cv2
import datetime
import os, sys
import numpy as np
import pandas as pd

# Importación de módulos
from src.camera_support import *

# Comprobaciones iniciales
try:
    os.mkdir("src/images")
except OSError as error:
    pass

# Variables iniciales
width = 320
height = 240
mode = "TICKET"
mainCamera = "environment"

# Aplicación web
app = Flask(__name__)
Mobility(app)

# Product Recognition Instance
from product_recognition.product_recognition import Recognize_Products_Images


# Ticket Recognition Instance
from ticket_recognition.ticket_recognition import Recognize_Tickets_Products

# Recommender Instance
from recommender_system.recommender_system import Recommender


# Endpoint principal
@app.route('/')
def homepage():
    return render_template("index.html", width=width, height=height, mode=mode, mainCamera=mainCamera)

# Endpoint que sube imagenes procesadas constantemente a la web
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        fs = request.files.get('snap')
        if fs:

            # Cargamos la imagen
            original = cv2.imdecode(np.frombuffer(fs.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            
            # Convertimos a escala de grises
            gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            
            # Aplicar suavizado Gaussiano
            gauss = cv2.GaussianBlur(gris, (5,5), 0)
                        
            # Detectamos los bordes con Canny
            canny = cv2.Canny(gauss, 50, 150)
                  
            # Buscamos los contornos
            (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            cv2.drawContours(original,contornos,-1,(0,0,255), 2)
            cv2.waitKey(0)

            ret, buf = cv2.imencode('.jpg', original)
            return send_file_data(buf.tobytes())
        else:
            return "No detectada ninguna foto"

    return

# Endpoint que procesa la imagen tomada por el usuario
'''
Devuelve dataframe en caso de procesar un ticket
Devuelve producto identificado en caso de procesar un producto
'''
@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        fs = request.files.get('snap')
        try:
            if fs and mode=="TICKET":
                print("Procesado ticket")
                fs.save('image.jpg')
                tr = Recognize_Tickets_Products(credentials_path="tomato/tomato_sauce.json")
                tr.set_image_path('image.jpg')

                global lista_recetas_rec
                lista_recetas_rec = tr.run()
                lista_recetas_rec = [element for element in lista_recetas_rec if element not in ["kg", "precio", "unidad", "kg kg", "descripción"]]

                rc = Recommender("recommender_system/full_format_recipes.json", "recommender_system/cleaned_recipes.csv" ,"recommender_system/diccionario_ingredientes.csv", lista_recetas_rec)

                global df
                df = rc.run()
                
                return "Procesado Ticket!"

            elif fs and mode=="PRODUCTO":
                print("Procesado producto")
                fs.save('image.jpg')
                pr = Recognize_Products_Images("")
                print(pr)

                global lista_prod_rec
                lista_prod_rec = pr.run()

                return "Procesado Producto! (TESTEO)"

            else:
                return "No detectada ninguna foto"
        except:
            return "Error :("
    
    return

# Endpoint que selecciona el modo de procesado: producto o ticket
'''
Establece la variable de modo en función de la elección de usuario recogida
'''
@app.route('/selection', methods=['POST'])
def selection():
        global mode
        mode = request.form['mode']
        return render_template("index.html", width=width, height=height, mode=mode, mainCamera=mainCamera)


# Endpoint que permite cambiar entre cámara trasera o delantera, SÓLO si la aplicación web se ejecuta en un dispositivo móvil.
'''
Devuelve el parámetro necesario para realizar el cambio de cámara activa en Javascript.
'''
@app.route('/selectionCam/<mainCamera>',methods=['GET', 'POST'])
def selectionCam(mainCamera):

        if mainCamera =="environment":
            mainCamera = "user"
        else:
            mainCamera = "environment"
            
        return render_template("index.html", width=width, height=height, mode=mode, mainCamera=mainCamera)


# Endpoint que renderiza la página de resultados en función de procesados anteriores.
@app.route('/results', methods=['GET', 'POST'])
def results():

    recipe_chosen = 0

    return render_template("result.html",       
        df_web=[df.iloc[[recipe_chosen]].to_html(classes='data')],
            titles_web = df.columns.values,
        mode=mode, 
        lista_prod_detected=lista_recetas_rec)

#Endpoint que permite seleccionar una receta concreta del top recetas.
@app.route('/selectrecipe', methods=['GET', 'POST'])
def selectionrecipe():

    recipe_chosen = request.args.get("recipe_chosen",default = 0, type = int)

    return render_template("result.html",       
        df_web=[df.iloc[[recipe_chosen]].to_html(classes='data')],
            titles_web = df.columns.values,
        mode=mode, 
        lista_prod_detected=lista_recetas_rec)



if __name__ == "__main__":
    app.run(debug = False, host = "0.0.0.0", port = 4000)