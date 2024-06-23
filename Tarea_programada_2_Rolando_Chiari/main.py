import threading
from Funciones import numero_imagenes,peticion_credenciales,peticion_imagenes,imagen,carpeta_imagenes,carpeta_cambio_imagenes,enviar_correo
import logging
import logging.config
import Bitacora.config

Bitacora.config.crear_carpetas_log()
logging.config.dictConfig(Bitacora.config.configuracion)

errores = logging.getLogger('errores')

print('----'*50)
print('''El siguiente programa se encarga de descargar de 1 a 10 imagenes de una URL
y le permitira realizarle 1,2,3,4 o ningun cambio a dichas imagenes.
los cambios que podra realizar son: Blanco y negro, Transponer, Difuminar y Rotar 90 grados en sentido horario.
      ''')
print('----'*50)

url_credenciales = 'https://python-course.lat/image-app/api-token-auth/'
url_fotos = 'https://python-course.lat/image-app/images/'
try:
    cantidad_imagenes = numero_imagenes(int(input('Digite el numero de imagenes que desea descargar: ')))
except Exception as e:
    print(f'El error es: {e}')
    errores.error(f'El error es: {e}')

token = peticion_credenciales(url_credenciales)
lista_urls = peticion_imagenes(cantidad_imagenes,token,url_fotos)
carpeta_con_imagenes = carpeta_imagenes()

lista_imagenes = []
for i in range(0,cantidad_imagenes):
    picture = threading.Thread(target=imagen, args=(lista_urls,i))
    lista_imagenes.append(picture)
for i in lista_imagenes:
    i.start()
print('----'*50)
print('A continuacion se le va a presentar una lista con los cambios que puede realizarle a las imagenes')
print('Blanco y negro, Transponer, Difuminar, Rotar 90 grados en sentido horario')
print('----'*50)
lista_seleccion = []
try:
    numero_cambios = int(input('Digite un numero de 1 al 4 dependiendo de la cantidad de cambios que desea realizar: '))
    if numero_cambios < 0 or numero_cambios > 4:
        print('Digite un numero entre 0 y 4')
except Exception as e:
    print(f'El error es {e}')

while numero_cambios > 0:
    try:
        seleccion_1 = input('Digite una de las opciones anteriormente mostradas: ')
        seleccion = seleccion_1.lower()
        if seleccion != 'blanco y negro' and seleccion != 'transponer' and seleccion != 'difuminar' and seleccion != 'rotar 90 grados en sentido horario':
            print('La opcion digitada no es valida')
        else:
            if seleccion not in lista_seleccion:
                lista_seleccion.append(seleccion)
            else:
                print(f'La opcion {seleccion} ya fue usada, por favor digite una opcion diferente')
    except Exception as e:
        print(f'El error es: {e}')
        errores.error(f'El error es: {e}')
    numero_cambios -= 1

carpeta_con_imagenes_con_cambios = carpeta_cambio_imagenes(lista_seleccion,cantidad_imagenes)

print('----'*50)
print('A continuacion, se van a enviar las imagenes por correo electronico')
try:
    correo_emisor = input('Digite el correo del cual se desea enviar las imagenes: ')
    correo_receptor = input('Digite el correo al cual desea enviar las imagenes: ')
    asunto = input('Digite el asunto del correo: ')
    mensaje_saludo = input('Digite el mensaje de saludo: ')
    password = input('Digite su contraseña para poder enviar el correo: ')
    info_cantidad_imagenes = f'se enviaron {cantidad_imagenes} imagenes y '
    info_cambios = 'Los cambios realizados a las imagenes son: '
    for i in lista_seleccion:
        info_cambios = info_cambios + i
    mensaje_a_enviar = mensaje_saludo + info_cantidad_imagenes + info_cambios
except Exception as e:
    print(f'El error es: {e}')

envio_correo = threading.Thread(target=enviar_correo, args=(correo_emisor,correo_receptor,asunto,cantidad_imagenes,mensaje_a_enviar,password))
envio_correo.start()





