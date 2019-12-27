#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from pyfingerprint.pyfingerprint import PyFingerprint

import mysql.connector
from mysql.connector import Error



## Registro de nuevo dedo
##

## Intenta incializacion del sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('¡La contraseña del sensor de huellas dactilares es incorrecta!')

except Exception as e:
    print('¡La contraseña del sensor de huellas dactilares es incorrecta!')
    print('Exception message: ' + str(e))
    exit(1)

## Obteniendo informacion del sensor
print('Plantillas utilizadas actualmente: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tratando de enrolar el nuevo dedo
try:
    print('Esperando por dedo...')

    ## Esperando que el dedo sea leído
    while ( f.readImage() == False ):
        pass

    ## Convierte la imagen de lectura a caracteres y la almacena en charbuffer 1
    f.convertImage(0x01)

    ## Comprueba si el dedo ya está inscrito
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('La plantilla ya existe en la posición #' + str(positionNumber))
        exit(0)

    print('Quitar dedo...')
    time.sleep(2)

    print('Esperando por el mismo dedo otra vez...')

    ## Espera que se vuelva a leer el dedo.
    while ( f.readImage() == False ):
        pass

    ## Convierte la imagen de lectura a caracteres y la almacena en charbuffer 2
    f.convertImage(0x02)

    ## Compara los charbuffers
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Los dedos no coinciden')

    ## Crea una plantilla
    f.createTemplate()

    ## Guarda la plantilla en el nuevo número de posición
    positionNumber = f.storeTemplate()
    nombre = input ("Ingrese nombre t apellido: ")
    rut = input ("Ingrese RUT (Sin puntos ni guiones): ")
    
    ## Se crea puente de conexion MySQL
    try:
        connection = mysql.connector.connect(host='',
                                 database='',
                                 user='',
                                 password='')

        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO `usuarios`
                              (`nombre`, `posicion`, `rut`) VALUES (%s,%s,%s)"""
        insert_tuple = (nombre, positionNumber, rut)
        result  = cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()
        print ("Registro insertado con éxito en la tabla de usuarios")

    except mysql.connector.Error as error :
        connection.rollback() #deshacer si se produjo alguna excepción
        print("Error al insertar el registro en la tabla de usuarios {}".format(error))

    finally:
        #cierra la conexión de la base de datos.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("La conexión de MySQL está cerrada")



    print('Dedo inscrito con éxito!')
    print('Nueva posición de plantilla #' + str(positionNumber))

except Exception as e:
    print('¡Operación fallida!')
    print('Mensaje de Excepción: ' + str(e))
    exit(1)

