from flask import make_response


# Permite el flujo de datos constante entre las imágenes tomadas por la webcam desde el backend hacia su procesado en backend. Hace posible la imagen previa.
'''
Devuelve respuesta de imagen
'''
def send_file_data(data, mimetype='image/jpeg', filename='output.jpg'):
    response = make_response(data)
    response.headers.set('Content-Type', mimetype)
    response.headers.set('Content-Disposition', 'attachment', filename=filename)

    return response

