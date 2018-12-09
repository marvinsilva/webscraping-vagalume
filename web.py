from flask import Flask
from flask_restful import Resource, Api
from crawler import WebScrap
from unicodedata import normalize
import re
import os
app = Flask(__name__)
api = Api(app)
vagalume = WebScrap()

def remover_acentos_char_especiais(txt):
    """ Converte caracteres com acento e remove caracteres especiais
	"""
    # A forma normal KD (NFKD) aplicará a decomposição de compatibilidade, ou seja,
    # substituirá todos os caracteres de compatibilidade por seus equivalentes
    rm_acentos = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    # Retorna a string obtida substituindo as ocorrências não sobrepostas mais à esquerda
    # do padrão na string pela replicação substituta.
    rm_char_especiais = re.sub('[^A-Za-z0-9 ]+', '', rm_acentos)
    # Ao retornar a variavel, substitui espaços ' ' por hífens '-' e converte a palavra
    # para letras minusculas
    return rm_char_especiais.replace(" ", "-").lower()

class TopMusic(Resource):
    def get(self, artista):
        artista = remover_acentos_char_especiais(artista)
        print(artista)
        top_musicas, alfabet_musicas = vagalume.search(artista)
        lim_top_musicas = []
        for seq, top in enumerate(top_musicas):
            if seq < 15:
                lim_top_musicas.append(top)
        return {'Top 15': lim_top_musicas}

class AlfabetMusic(Resource):
    def get(self, artista):
        artista = remover_acentos_char_especiais(artista)
        top_musicas, alfabet_musicas = vagalume.search(artista)
        return {f'Todas as músicas de {artista}': alfabet_musicas}

class TopMusicQuant(Resource):
    def get(self, artista, quant):
        artista = remover_acentos_char_especiais(artista)
        if quant > 25:
            return {'Error': 'O número máximo de músicas TOP é de 25'}
        top_musicas, alfabet_musicas = vagalume.search(artista)
        lim_top_musicas = []
        for seq, top in enumerate(top_musicas):
            if seq < quant:
                lim_top_musicas.append(top)
        return {f'Top {quant}': lim_top_musicas}

class MusicaPorLetra(Resource):
    def get(self, artista, letra_inicial):
        artista = remover_acentos_char_especiais(artista)
        top_musicas, alfabet_musicas = vagalume.search(artista)
        musica_por_letra = []
        for mus in alfabet_musicas:
            if mus.startswith(letra_inicial.upper()):
                musica_por_letra.append(mus)

        return {f'Músicas com a letra {letra_inicial}': musica_por_letra}

api.add_resource(AlfabetMusic, '/alfabet/<string:artista>') # http://127:0.0.1:5000/top/metallica
api.add_resource(TopMusic, '/top/<string:artista>') # http://127:0.0.1:5000/top/metallica
api.add_resource(TopMusicQuant, '/top/<string:artista>/<int:quant>') # http://127:0.0.1:5000/top/metallica/10
api.add_resource(MusicaPorLetra, '/top/<string:artista>/<string:letra_inicial>') # http://127:0.0.1:5000/top/metallica


#app.run(host='127.0.0.1', port=5000)
# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', 5000))
# Tem que ser 0.0.0.0 para rodar no Heroku
#app.run(host='127.0.0.1', port=port)
app.run(host='0.0.0.0', port=port)
