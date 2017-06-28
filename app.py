from flask import Flask, request, jsonify
from sqlalchemy import create_engine


db_conncect = create_engine('sqlite:///testdb.db')
app = Flask(__name__)


languages = [{'name': 'JS'}, {'name': 'Python'}, {'name': 'Ruby'}]


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It Works'})

@app.route('/lang', methods=['GET'])
def getLangs():
    return jsonify({'languages': languages})

@app.route('/lang', methods=['POST'])
def addOne():
    language = {'name': request.json['name']}
    languages.append(language)
    return jsonify({'languages': languages})

@app.route('/lang/<string:name>', methods=['GET'])
def getOne(name):
    langs =[language for language in languages if language['name'] == name]
    return jsonify({'language': langs[0]})


@app.route('/lang/<string:name>', methods=['PUT'])
def editOne(name):
    langs =[language for language in languages if language['name'] == name]
    langs[0]['name'] = request.json['name']
    return jsonify({'language': langs[0]})

if __name__ == '__main__':
    app.run(port='5002')
