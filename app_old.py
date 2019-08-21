from flask import Flask, jsonify, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hithere')
def hi_there():
    return 'I hit /hithere'

@app.route('/return_json')
def my_json():
    age = 10*2.4
    resp = {'name':'Douglas',
            'age': age,
            'phones':[
                {'phone_name':'mobile',
                 'number':'0838705704'},
                {'phone_name':'mobile',
                 'number':'1231231'}
            ]}
    return jsonify(resp)

@app.route('/add_num', methods=["POST"])
def add_nums():
    data = request.get_json()
    my_sum = data['x'] + data['y']
    return jsonify({'sum':my_sum})

if __name__ == '__main__':
    app.run()
