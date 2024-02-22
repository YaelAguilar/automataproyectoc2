import mysql.connector
from config import DATABASE

def buscar_coincidencias(columna, valor):
    conexion = mysql.connector.connect(**DATABASE)
    cursor = conexion.cursor()

    consulta = f"SELECT * FROM datospersonalesdb WHERE {columna} LIKE '%{valor}%'"
    cursor.execute(consulta)

    resultados = cursor.fetchall()

    if resultados:
        print("Coincidencias encontradas:")
        for resultado in resultados:
            print(resultado)
    else:
        print("No se encontraron coincidencias.")

    cursor.close()
    conexion.close()

columna = input("Ingrese el nombre de la columna (Clave_cliente, Nombre_Contacto, Correo, Teléfono_Contacto): ")
valor = input("Ingrese el valor a buscar: ")

buscar_coincidencias(columna, valor)
