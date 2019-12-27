#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyfingerprint.pyfingerprint import PyFingerprint
import mysql.connector
from mysql.connector import Error

# Borra las huellas del sensor

# Trata de inicializar el huellero
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('¡La contraseña del sensor de huellas dactilares es incorrecta!')

except Exception as e:
    print('¡No se pudo inicializar el sensor de huellas digitales!')
    print('Mensaje de excepción: ' + str(e))
    exit(1)
# Obtiene informacion del sensor
print('Plantillas utilizadas actualmente: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

# Trata de borrar la plantilla de la huella
posicion = ""

mySQLConnection = mysql.connector.connect(host='',
                                     database='',
                                     user='',
                                     password='')

try:
    rut = input ("Ingrese RUT (Sin puntos ni guiones): ")

    cursor = mySQLConnection.cursor(prepared=True)
    sql_select_query = """select * from usuarios where rut = %s and activo = 1"""
    cursor.execute(sql_select_query, (rut, ))
    record = cursor.fetchall()
    
    for row in record:
        print("ID = ", row[0], )
        print("NOMBRE = ", row[1].decode())
        print("POSICION = ", row[2], )
        print("RUT = ", row[3].decode(), )
        print("ACTIVO = ", row[4], "\n")
        posicion = row[2]
        
        cursor = mySQLConnection.cursor(prepared=True)
        sql_update_query = """update usuarios set activo = %s where posicion = %s and activo = %s"""
        input = (0, posicion,1)
        cursor.execute(sql_update_query, input)
        mySQLConnection.commit()
        print("Registro actualizado con éxito")


except mysql.connector.Error as error:
    print("Error al obtener el registro de la base de datos: {}".format(error))
    print('Operacion Fallida!')
    print('Exception message: ' + str(e))
    exit(1)
finally:
    # cerrar la conexión de la base de datos.
    if (mySQLConnection.is_connected()):
        cursor.close()
        mySQLConnection.close()
        print("La conexión está cerrada")

        print("POS", posicion)

    posicion = int(posicion)

    if ( f.deleteTemplate(posicion) == True ):
         print('Plantilla elmiminada')

