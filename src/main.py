from flask import Flask, request, jsonify
from flask_cors import CORS
from busqueda import buscar_coincidencias

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")

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

if __name__ == '__main__':
    app.run(debug=True)
