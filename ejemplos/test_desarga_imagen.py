#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tempfile
from pyfingerprint.pyfingerprint import PyFingerprint


# Lee la imagen y la descarga

# Intenta inicializar el sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if (f.verifyPassword() == False):
        raise ValueError(
            '¡La contraseña del sensor de huellas dactilares es incorrecta!')

except Exception as e:
    print('¡No se pudo inicializar el sensor de huellas digitales!')
    print('Exception message: ' + str(e))
    exit(1)

# Obtiene información del sensor
print('Plantillas utilizadas actualmente: ' +
      str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

# Intenta leer la imagen y la descrga
try:
    print('Esperando dedo en el sensor...')

    # Espera que se lea ese dedo
    while (f.readImage() == False):
        pass

    # f.convertImage(0x01)

    # ## Searchs template
    # result = f.searchTemplate()

    # positionNumber = result[0]

    # str(positionNumber))

    print('Descargando imagen (tomará un tiempo) ...')

    imageDestination = tempfile.gettempdir() + '/fingerprint.bmp'
    f.downloadImage(imageDestination)

    print('The image was saved to "' + imageDestination + '".')

except Exception as e:
    print('¡Operación fallida!')
    print('Mensaje de Excepción: ' + str(e))
    exit(1)
