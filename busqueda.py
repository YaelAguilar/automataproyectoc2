import mysql.connector
from config import DATABASE

def buscar_coincidencias(columna, valor):
    conexion = mysql.connector.connect(**DATABASE)
    cursor = conexion.cursor()

    consulta = f"SELECT * FROM datospersonalesdb WHERE {columna} LIKE '%{valor}%'"
    cursor.execute(consulta)

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados
