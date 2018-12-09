from flask import Flask
from flask_restful import Resource, Api
from crawler import WebScrap
from unicodedata import normalize
import re

app = Flask(__name__)
api = Api(app)
vagalume = WebScrap()

class TopMusic(Resource):
    def get(self, artista):
        artista = remover_acentos_char_especiais(artista)
        print(artista)
        top_musicas, alfabet_musicas = vagalume.search(artista)
        lim_top_musicas = []
        for seq, top in enumerate(top_musicas):
            if seq < 15:
                lim_top_musicas.append(top)
        return {'Top 15': 'Teste'}


api.add_resource(TopMusic, '/top/<string:artista>') # http://127:0.0.1:5000/top/metallica


app.run(port=5000)
