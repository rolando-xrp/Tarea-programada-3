from PIL import Image,ImageFilter # type: ignore
import requests # type: ignore
import logging
import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



errores = logging.getLogger('errores')

def numero_imagenes(numero):
    '''
    Funcion que verifica que el numero de imagenes del usuario sea valido
    
    Args:
    numero: el numero que digita el usuario

    return:
    El numero que ingreso el usuario en caso de ser valido.
    '''
    if numero >= 1 and numero <= 10:
        return numero
    else:
        print (f'El numero digitado {numero}, no esta entre 1 y 10, porfavor seleccione un numero dentro de este rango')

def peticion_credenciales(url):
    '''
    Funcion que genera el token necesario para pedir las imagenes.

    Args:
    La url a la cual se le va a realizar la peticion.

    return:
    El token necesario para la descarga de las imagenes.
    '''
    try:
        datos = {
            'user': 'user',
            'password': 'python22024!',
    }
        response = requests.post(url, json=datos)
        token = response.json()
        return token
    except Exception as e:
        errores.error(f'El error es: {e}')


def peticion_imagenes(numero_imagenes,token,url_imagenes):
    '''
    Funcion que se encarga de pedir los https a un url

    Args:
    numero_imagenes: La cantidad de imagenes que el usuario desea descargar.
    Token: El token necesario para realizar el pedido
    url_imagenes: la url a la cual se le va a hacer la peticion

    return:
    Devuelve una lista con los https a los cuales se les va a pedir las imagenes.
    '''
    try:
        datos = {
            "cantidad": numero_imagenes # Número entero
        }
        encabezados = {
            'Content-type': 'application/json; charset=UTF-8',
            'Authorization' : f'Bearer {token}',
}
        response = requests.post(url_imagenes, json = datos, headers = encabezados)
        data = response.json()
        return data
    
    except Exception as e:
        errores.error(f'El error es: {e}')

def imagen(lista_url,indice):
    '''
    Funcion que se encarga de pedir la imagen a la direccion https.

    Args:
    Lista_url: Lista que posee los https a los cuales se les va a pedir la imagen
    indice: indice para navegar la lista de https.

    return:
    La imagen requerida.
    '''
    response_imagen = requests.get(lista_url[indice])
    with open(f"imagenes/imagen_{indice+1}.jpg", 'wb') as imagen:
        imagen.write(response_imagen.content)


def carpeta_imagenes():
    '''
    Funcion encargada de crear la carpeta donde se van a guardar las imagenes
    
    '''
    if os.path.exists('imagenes'):
        shutil.rmtree('imagenes')
    os.mkdir('imagenes')

def carpeta_cambio_imagenes(lista_seleccion,num_imagenes):
    '''
    Funcion que crea y llena la carpeta de las imagenes con o sin cambios.

    Args:
    lista_seleccion: Lista que contiene los cambios que el usuario desea agregar
    num_imagenes: El numero de imagenes que el usuario desea descargar.
    '''
    if os.path.exists('imagenes_con_cambios'):
        shutil.rmtree('imagenes_con_cambios')
    os.mkdir('imagenes_con_cambios')

    for i in range(1,num_imagenes+1):
        imagen = Image.open(f'imagenes/imagen_{i}.jpg')
        imagen.save(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')

    for i in lista_seleccion:
        if i == 'blanco y negro':
            for i in range(1,num_imagenes+1):
                imagen = Image.open(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')
                imagen_gris = imagen.convert('L')
                imagen_gris.save(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')
        
        elif i == 'transponer':
            for i in range(1,num_imagenes+1):
                imagen = Image.open(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')
                imagen_volteada = imagen.transpose(Image.FLIP_LEFT_RIGHT)
                imagen_volteada.save(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')

        elif i == 'difuminar':
            for i in range(1,num_imagenes+1):
                imagen = Image.open(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')
                imagen_desenfocada = imagen.filter(ImageFilter.GaussianBlur(5))
                imagen_desenfocada.save(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')

        elif i == 'rotar imagen':
            for i in range(1,num_imagenes+1):
                imagen = Image.open(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')
                imagen_rotada = imagen.rotate(90)
                imagen_rotada.save(f'imagenes_con_cambios/imagen_cambios_{i}.jpg')

def enviar_correo(correo_emisor,correo_receptor,asunto,numero_imagenes,mensaje_saludo,password):
    '''
    Funcion que se encarga de enviar el correo electronico

    Args:
    correo_emisor: correo que envia el mensaje.
    correoreceptor: correo que recibe el mensaje.
    asunto: Asunto del correo.
    numero_imagenes: La cantidad de imagenes que se va a enviar.
    mensaje_saludo: El mensaje de saludo.
    password: la contraña del usuario, necesaria para enviar el correo.
    '''
    mensaje = MIMEMultipart()
    mensaje['From'] = correo_emisor
    mensaje['To'] = correo_receptor
    mensaje['Subject'] = asunto

    cuerpo = mensaje_saludo
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    for i in range(1,numero_imagenes+1):
        with open(f'imagenes_con_cambios/imagen_cambios_{i}.jpg', mode="rb") as imagen:
            parte_imagen = MIMEBase('image', 'jpg')
            parte_imagen.set_payload(imagen.read())
        encoders.encode_base64(parte_imagen)
        mensaje.attach(parte_imagen)

    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()

    servidor.login(
        user = correo_emisor, 
        password = password)

    servidor.sendmail(
        correo_emisor, 
        correo_receptor, mensaje.as_string())

    servidor.quit()










