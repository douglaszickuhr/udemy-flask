from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://mongo:27017",
                     username='root',
                     password='example')
db = client.myNewDB
user_num = db["user_num"]

user_num.insert_one({
    'num_of_users': 0
})

class Visit(Resource):
    def get(self):
        prev_num = user_num.find({})[0]['num_of_users']
        return jsonify({'users':prev_num})

    def post(self):
        prev_num = user_num.find({})[0]['num_of_users']
        new_num = prev_num + 1
        user_num.update({},{'$set':{'num_of_users':new_num}})
        return jsonify({'users':new_num})


def check_posted_data(data, function_name):
    if function_name == 'divide':
        if int(data['y']) == 0:
            return 302, 'Division by 0'
        else:
            return [200]

    if 'x' not in data or 'y' not in data:
        return 301, 'Missing number'
    else:
        return [200]



class Add(Resource):
    def post(self):
        # Get posted data
        data = request.get_json()

        # Pre-check the status
        status = check_posted_data(data, 'add')

        # Validate response
        if status[0] != 200:
            ret_json = {
                'message': status[1],
                'status': status[0]
            }
            return jsonify(ret_json)

        # Extract from list
        x = int(data['x'])
        y = int(data['y'])

        # Calculate
        ret = x + y

        # Build response
        ret_json = {
            'message': ret,
            'status': 200
        }

        return jsonify(ret_json)

class Subtract(Resource):
    def post(self):
        # Get posted data
        data = request.get_json()

        # Pre-check the status
        status = check_posted_data(data, 'subtract')

        # Validate response
        if status[0] != 200:
            ret_json = {
                'message': status[1],
                'status': status[0]
            }
            return jsonify(ret_json)

        # Extract from list
        x = int(data['x'])
        y = int(data['y'])

        # Calculate
        ret = x - y

        # Build response
        ret_json = {
            'message': ret,
            'status': 200
        }

        return jsonify(ret_json)


class Multiply(Resource):
    def post(self):
        # Get posted data
        data = request.get_json()

        # Pre-check the status
        status = check_posted_data(data, 'multiply')

        # Validate response
        if status[0] != 200:
            ret_json = {
                'message': status[1],
                'status': status[0]
            }
            return jsonify(ret_json)

        # Extract from list
        x = int(data['x'])
        y = int(data['y'])

        # Calculate
        ret = x * y

        # Build response
        ret_json = {
            'message': ret,
            'status': 200
        }

        return jsonify(ret_json)

class Divide(Resource):
    def post(self):
        # Get posted data
        data = request.get_json()

        # Pre-check the status
        status = check_posted_data(data, 'divide')

        # Validate response
        if status[0] != 200:
            ret_json = {
                'message': status[1],
                'status': status[0]
            }
            return jsonify(ret_json)

        # Extract from list
        x = int(data['x'])
        y = int(data['y'])

        # Calculate
        ret = x / y

        # Build response
        ret_json = {
            'message': ret,
            'status': 200
        }

        return jsonify(ret_json)

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/visit")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
