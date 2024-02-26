from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from config import DATABASE
import re

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")

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

def guardar_usuario(username, password):
    conexion = mysql.connector.connect(**DATABASE)
    cursor = conexion.cursor()

    consulta_verificacion = "SELECT * FROM user WHERE username = %s"
    cursor.execute(consulta_verificacion, (username,))
    existe_usuario = cursor.fetchone()

    if existe_usuario:
        cursor.close()
        conexion.close()
        return False

    consulta_insercion = "INSERT INTO user (username, password) VALUES (%s, %s)"
    datos_usuario = (username, password)

    try:
        cursor.execute(consulta_insercion, datos_usuario)
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar usuario: {str(e)}")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()

def validar_contrasena(password):
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$')
    return bool(password_regex.match(password))

@app.route('/buscar', methods=['POST'])
def buscar():
    try:
        data = request.get_json()
        columna = data['columna']
        valor = data['valor']

        resultados = buscar_coincidencias(columna, valor)

        return jsonify({'resultados': resultados})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        conexion = mysql.connector.connect(**DATABASE)
        cursor = conexion.cursor()

        consulta = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(consulta, (username, password))

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario:
            return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'})
        else:
            return jsonify({'success': False, 'error': 'Verifica tus datos ingresados'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not validar_contrasena(password):
            return jsonify({'error': 'Las condiciones de contraseña no se cumplen.'}), 400

        if not guardar_usuario(username, password):
            return jsonify({'error': 'El usuario ya existe.'}), 400

        return jsonify({'message': 'Usuario registrado exitosamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
