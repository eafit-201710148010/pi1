from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

tipo_medicion = {'sensor': 'DS18B20', 'variable': 'numerico', 'unidades': 'centigrados fahrenheit' }

mediciones = [
    {'fecha': '2019-08-24 09:24:00', **tipo_medicion, 'valor': 70},
    {'fecha': '2019-08-24 12:30:00', **tipo_medicion, 'valor': 95},
    {'fecha': '2019-08-24 16:00:00', **tipo_medicion, 'valor': 81},
    {'fecha': '2019-08-24 18:43:00', **tipo_medicion, 'valor': 66},
    {'fecha': '2019-08-24 21:15:00', **tipo_medicion, 'valor': 52},
]

#get tipo medicion
@app.route('/')
def get():
    return jsonify(tipo_medicion)

@app.route('/mediciones', methods=['GET'])
def getAll():
    return jsonify(mediciones)

@app.route('/mediciones/mayores/<int:porcentaje>',methods=['GET'])
def getMayores(porcentaje):
    mayores = len(mediciones) * porcentaje/100
    lista = []
    resultado = []
    for medicion in mediciones:
        lista.append(medicion['valor'])  
    lista.sort()
    lista.reverse()
    for n in range(mayores):
        for medicion in mediciones:
            aux = 0
            if(medicion['valor']==lista[n]):
                resultado.append(medicion)
                mediciones.remove(aux)
                break
            aux = aux + 1
    return jsonify(resultado)       
        

@app.route('/mediciones', methods=['POST'])
def postOne():
    body = request.json
    now = datetime.now()
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**body, **tipo_medicion})
    return jsonify(mediciones)

@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putOne(fecha):
    body = request.json
    x = False
    for medicion in mediciones:
        if (fecha in medicion['fecha']):
            x = True
            medicion['valor'] = body['valor']
    return 'Modificado' if x else 'No Encontrado'
    

app.run(port=5000,debug=True)





