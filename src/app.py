from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from bcrypt import hashpw, gensalt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://mongo:27017",
                     username='root',
                     password='example')

db = client.sentences_database
users = db["users"]

"""
Resources           Route       Method      Param               Response
Register User       /register   POST        Username/Pwd        200 - OK

Store Sentence      /store      POST        User/Pwd/sentence   200 - OK
                                                                301 - Out of Tokens
                                                                302 - Invalid Password

Retrieve Sentence   /get        GET         User/Pwd            200 - OK
                                                                301 - Out of Tokens
                                                                302 - Invalid Password
"""

def hash_pwd(pwd):
    return hashpw(pwd.encode('utf8'),gensalt())

def validate_user(user,pwd):
    hashed_pwd = users.find({'username':user})[0]['password']

    if hashed_pwd == hashpw(pwd.encode('utf8'), hashed_pwd):
        return True
    else:
        return False

def user_tokens(user):
    return users.find({'username':user})[0]['tokens']

class Register(Resource):
    def post(self):
        data = request.get_json()

        username = data['username']
        password = hash_pwd(data['password'])

        users.insert_one({'username':username,
                          'password':password,
                          'sentences':"",
                          'tokens':5})
        ret_json = {
            'message': 'User Created',
            'status': 200
        }
        return jsonify(ret_json)

class Store(Resource):
    def post(self):
        data = request.get_json()

        username = data['username']
        password = data['password']
        sentence = data['sentence']

        if not validate_user(username, password):
            return jsonify({'message':'Invalid User',
                            'status':301})

        operation_cost = 1
        tokens = user_tokens(username)

        if tokens < operation_cost:
            return jsonify({'message':'Insuficient tokens',
                            'status':302})

        users.update({'username':username},
                     {'$set':{
                        'sentences':sentence,
                        'tokens':tokens-1
                     }}
        )

        return jsonify({'message':'Sentence Stored',
                        'status' : 200})

class Token(Resource):
    def get(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not validate_user(username, password):
            return jsonify({'message':'Invalid User',
                            'status':301})

        tokens = user_tokens(username)

        return jsonify({'message':str(tokens),
                        'status':200})

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        new_tokens = int(data['tokens'])

        if not validate_user(username, password):
            return jsonify({'message':'Invalid User',
                            'status':301})

        tokens = user_tokens(username)

        users.update({'username':username},
                     {'$set':{
                        'tokens':tokens+new_tokens
                     }}
        )

        return jsonify({'message':str(tokens+new_tokens),
                        'status':200})

class Sentence(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not validate_user(username, password):
            return jsonify({'message':'Invalid User',
                            'status':301})

        sentence = users.find({'username':username})[0]['sentences']

        return jsonify({'message':sentence,
                       'status':200})



api.add_resource(Register,'/register')
api.add_resource(Store,'/store')
api.add_resource(Token,'/token')
api.add_resource(Sentence,'/sentence')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
