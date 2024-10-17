from flask import Flask, jsonify, make_response
import json

app = Flask(__name__)

# Função para carregar dados do arquivo JSON
def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

# Rota GET para retornar os eventos
@app.route('/eventos', methods=['GET'])
def get_items():
    data = load_data()
    response = make_response(jsonify(data))
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)
