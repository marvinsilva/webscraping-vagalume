from flask import Flask
from flask_restful import Resource, Api
from crawler import WebScrap

app = Flask(__name__)
api = Api(app)
vagalume = WebScrap()

class Student(Resource):
    def get(self, name):
        top_musicas, alfabet_musicas = vagalume.search(name)
        print(top_musicas, alfabet_musicas)
        return {'student': top_musicas}

api.add_resource(Student, '/top/<string:name>')     # http://127:0.0.1:5000/student/Marcus

app.run(port=5000)
