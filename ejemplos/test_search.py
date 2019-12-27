#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import mysql.connector
from mysql.connector import Error

# Busqueda de un dedo

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
print('Plantillas utilizadas actualmente:' +
      str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

# Intenta buscar el dedo y calcular el hash
try:
    print('Esperando el dedo ...')

    # Espera que se lea ese dedo
    while (f.readImage() == False):
        pass

    # Convierte la imagen leída en caracteres y la almacena en charbuffer 1
    f.convertImage(0x01)

    # Busqueda de la plantilla
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if (positionNumber == -1):
        print('¡No se encontraron coincidencias!')
        exit(0)
    else:
        print('Plantilla encontrada en la posición #' + str(positionNumber))
        print('El puntaje de precisión es: ' + str(accuracyScore))

        try:
            mySQLConnection = mysql.connector.connect(host='',
                                                      database='',
                                                      user='',
                                                      password='')
            cursor = mySQLConnection.cursor(prepared=True)
            sql_select_query = """select * from usuarios where posicion = %s and activo = 1"""
            cursor.execute(sql_select_query, (positionNumber, ))
            record = cursor.fetchall()
            for row in record:
                print("ID = ", row[0], )
                print("NOMBRE = ", row[1].decode())
                print("POSICION = ", row[2], )
                print("RUT = ", row[3].decode(), )
                print("ACTIVO = ", row[4], "\n")
        except mysql.connector.Error as error:
            print("Error al obtener el registro de la base de datos: {}".format(error))
        finally:
            # cerrar la conexión de la base de datos.
            if (mySQLConnection.is_connected()):
                cursor.close()
                mySQLConnection.close()
                print("La conexión está cerrada")

    # Carga la plantilla encontrada en charbuffer 1
    f.loadTemplate(positionNumber, 0x01)

    # Descarga las características de la plantilla cargada en charbuffer 1
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    # Características de hash de plantilla
    print('SHA-2 hash de plantilla: ' +
          hashlib.sha256(characterics).hexdigest())

except Exception as e:
    print('Operación fallida!')
    print('Mensaje de Excepción: ' + str(e))
    exit(1)
