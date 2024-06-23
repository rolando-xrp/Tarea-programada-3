import os

configuracion = {
    'version': 1,
    'loggers': {
        'errores': {
            'level': 'ERROR',
            'handlers': ['handler_errores']
        },
    },
    'handlers': {
        'handler_errores' : {
            'class': "logging.FileHandler",
            'filename': "logs/errores.txt",
            'level': 'ERROR',
            'formatter' : 'formato_error'
        },

    },
    'formatters': {
        'formato_error': {
            'format' : "%(asctime)s - %(levelname)s - %(message)s - %(funcName)s -%(pathname)s - %(module)s - %(lineno)d - %(process)d - %(thread)d"
        },
    }
}


def crear_carpetas_log():
    ruta = "logs"
    if not os.path.exists(ruta):
        os.mkdir(ruta)