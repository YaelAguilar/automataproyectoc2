from flask import Flask, render_template, request
from busqueda import buscar_coincidencias

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    columna = request.form['columna']
    valor = request.form['valor']

    resultados = buscar_coincidencias(columna, valor)

    return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
