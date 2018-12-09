from flask import Flask
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

class Student(Resource):
    def get(self, name):
        return {'student': name}

api.add_resource(Student, '/student/<string:name>')     # http://127:0.0.1:5000/student/Marcus

# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))
# Tem que ser 0.0.0.0 para rodar no Heroku
#app.run(host='127.0.0.1', port=port)
app.run(host='0.0.0.0', port=5000)
