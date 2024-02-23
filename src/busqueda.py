import mysql.connector
from config import DATABASE

def buscar_coincidencias(columna, valor):
    conexion = mysql.connector.connect(**DATABASE)
    cursor = conexion.cursor()

    consulta = f"SELECT * FROM datospersonalesdb WHERE {columna} LIKE %s"
    cursor.execute(consulta, (f"%{valor}%",))

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    resultados_filtrados = [r for r in resultados if valor.lower() in str(r).lower()]

    return resultados_filtrados