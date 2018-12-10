#!/usr/bin/env python

"""	Objetivo: Fazer um crawler que recupera dados do site ​www.vagalume.com​ em tempo de execução e
    servir os dados recuperados em ENDPOINTS através de uma API Restful.
    Autor: Marcus Vinicius Laurindo da Silva
    Date de criação: 10/12/2018
    Disponível em: https://github.com/marvinsilva/webscraping-vagalume
    Python 3.7.1
"""

# Importando bibliotecas
import os       # Interfaces de sistema operacional diversas
import re       # Operações de expressão regular
import sys      # Parâmetros e funções específicos do sistema
from unicodedata import normalize       # Unicode Database. Retorna o formulário normal para o unistr da string Unicode
from crawler import WebScrap        # Importa a classe WebScrap do arquivo crawler.py para instanciar web scrap vagalume
from flask import Flask     # Flask é um microframework web escrito em Python e baseado na biblioteca WSGI Werkzeug e na biblioteca de Jinja2
from flask_restful import Resource, Api     # O Flask-RESTful é uma extensão do Flask que adiciona suporte para a construção rápida de APIs REST

# Informações sobre o software
__author__ = "[marvinsilva] Marcus Vinicius Laurindo da Silva"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Marcus Vinicius Laurindo da Silva"
__email__ = "vnc_vinicius92@hotmail.com"
__status__ = "Production"

# Criando uma instancia da classe flask
app = Flask(__name__)
# Criando uma API
api = Api(app)
# Instanciando a web scrap vagalume
vagalume = WebScrap()
# Variável com o nome e extensão deste arquivo
nome_arquivo = os.path.basename(__file__)

# Mensagem de ajuda contendo informações de utilização deste software
mensagem_ajuda = f"Endpoints:", \
                 "Outra mensagem"

# Mensagem contendo versão e demais informações sobre este software
mensagem_versao = f"Versao: {__version__}", f"Autor: {__author__}", \
                  f"E-mail: {__email__}", f"Licenca: {__license__}", \
                  f"Status: {__status__}"

def remover_acentos_char_especiais(txt):
    """ Converte caracteres com acento e remove caracteres especiais
	"""
    # A forma normal KD (NFKD) aplicará a decomposição de compatibilidade, ou seja,
    # substituirá todos os caracteres de compatibilidade por seus equivalentes
    rm_acentos = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    # Retorna a string obtida substituindo as ocorrências não sobrepostas mais à esquerda
    # do padrão na string pela replicação substituta.
    rm_char_especiais = re.sub('[^A-Za-z0-9 -]+', '', rm_acentos)
    
    # Ao retornar a variavel, substitui espaços ' ' por hífens '-' e converte a palavra
    # para letras minusculas
    return rm_char_especiais.replace(" ", "-").lower()

class TopMusic(Resource):
    """ Recurso para listar as top 15 musicas de um artista
	"""
    def get(self, artista):     # metodo GET para obter informações sobre o recurso (Resource)
        artista = remover_acentos_char_especiais(artista)       # Trata a requisição recebida na função 'remover_acentos_char_especiais'
        if not vagalume.request(artista, ''):                   # Verifica se a URL do artista é valida no site do vagalume
            sys.exit(2)                                         # e caso não seja uma mensagem de erro é exibida no console
        # Executa a função 'search' na instancia 'vagalume' e recebe como
        # resultado as duas listas (top e todas) daquele artista
        top_musicas, alfabet_musicas = vagalume.search(artista)

        lim_top_musicas = []
        # lista das top 15 musicas do artista
        [lim_top_musicas.append(top) for seq, top in enumerate(top_musicas) if seq < 15]
        
        return {'Top 15': lim_top_musicas}

class TopMusicQuant(Resource):
    """ Recurso para listar as top musicas de um artista na quantidade requisitada
	"""
    def get(self, artista, quant):     # metodo GET para obter informações sobre o recurso (Resource)
        artista = remover_acentos_char_especiais(artista)       # Trata a requisição recebida na função 'remover_acentos_char_especiais'
        if not vagalume.request(artista, ''):                   # Verifica se a URL do artista é valida no site do vagalume
            sys.exit(2)                                         # e caso não seja uma mensagem de erro é exibida no console

        if quant > 25:      # Valida top musicas limite 25
            return {'Erro': 'O numero maximo de musicas TOP e de 25'}

        # Executa a função 'search' na instancia 'vagalume' e recebe como
        # resultado as duas listas (top e todas) daquele artista
        top_musicas, alfabet_musicas = vagalume.search(artista)

        lim_top_musicas = []
        # lista das top musicas do artista
        [lim_top_musicas.append(top) for seq, top in enumerate(top_musicas) if seq < quant]
        
        return {f'Top {quant}': lim_top_musicas}

class AlfabetMusic(Resource):
    """ Recurso para listar todas as musicas de um artista
	"""
    def get(self, artista):     # metodo GET para obter informações sobre o recurso (Resource)
        artista = remover_acentos_char_especiais(artista)       # Trata a requisição recebida na função 'remover_acentos_char_especiais'
        if not vagalume.request(artista, ''):                   # Verifica se a URL do artista é valida no site do vagalume
            sys.exit(2)                                         # e caso não seja uma mensagem de erro é exibida no console
        
        # Executa a função 'search' na instancia 'vagalume' e recebe como
        # resultado as duas listas (top e todas) daquele artista
        top_musicas, alfabet_musicas = vagalume.search(artista)
        
        return {f'Todas as musicas de {artista}': alfabet_musicas}

class MusicaPorLetra(Resource):
    """ Recurso para listar as músicas de um artista baseado na primeira letra do título da música
	"""
    def get(self, artista, letra_inicial):     # metodo GET para obter informações sobre o recurso (Resource)
        artista = remover_acentos_char_especiais(artista)       # Trata a requisição recebida na função 'remover_acentos_char_especiais'
        if not vagalume.request(artista, ''):                   # Verifica se a URL do artista é valida no site do vagalume
            sys.exit(2)                                         # e caso não seja uma mensagem de erro é exibida no console

        # Executa a função 'search' na instancia 'vagalume' e recebe como
        # resultado as duas listas (top e todas) daquele artista
        top_musicas, alfabet_musicas = vagalume.search(artista)
        
        musica_por_letra = []
        # lista de musicas de acordo com a primeira letra correspondente
        [musica_por_letra.append(mus) for mus in alfabet_musicas if mus.startswith(letra_inicial.upper())]

        return {f'Musicas com a letra {letra_inicial}': musica_por_letra}

class LetraMusic(Resource):
    """ Recurso retorna a letra de uma música específica
	"""
    def get(self, artista,lyric):     # metodo GET para obter informações sobre o recurso (Resource)
        artista = remover_acentos_char_especiais(artista)       # Trata as requisições recebidas (artista e letra da musica)
        lyric = remover_acentos_char_especiais(lyric)           # na função 'remover_acentos_char_especiais'
        if not vagalume.request(artista, lyric):                # Verifica se a URL do artista e letra são validas no site do vagalume
            sys.exit(2)                                         # e caso não seja uma mensagem de erro é exibida no console
        
        # Executa a função 'letra' na instancia 'vagalume' e recebe como
        # resultado a letra da musica especificada daquele artista
        letra = vagalume.letra(artista, lyric)
        
        return {f'Letra da musica {lyric}': letra}

class Ajuda(Resource):
    """ Recurso exibe uma mensagem de ajuda sobre o programa
	"""
    def get(self):     # metodo GET para obter informações sobre o recurso (Resource)
        
        return {'Mensagem de ajuda: ': mensagem_ajuda}

class Versao(Resource):
    """ Recurso exibe a versao do software e demais informações
	"""
    def get(self):     # metodo GET para obter informações sobre o recurso (Resource)
        
        return {'Versao de Software: ': mensagem_versao}

if __name__ == "__main__":

    # Criando e adicionando os recursos e Endpoints a API
    # Comentarios exemplicados com o artista 'metallica'
    api.add_resource(AlfabetMusic, '/todas/<string:artista>')                            # http://127:0.0.1:5000/todas/metallica
    api.add_resource(TopMusic, '/top/<string:artista>')                                  # http://127:0.0.1:5000/top/metallica
    api.add_resource(TopMusicQuant, '/top/<string:artista>/<int:quant>')                 # http://127:0.0.1:5000/top/metallica/10
    api.add_resource(MusicaPorLetra, '/top/<string:artista>/<string:letra_inicial>')     # http://127:0.0.1:5000/top/metallica/a
    api.add_resource(LetraMusic, '/letra/<string:artista>/<string:lyric>')               # http://127:0.0.1:5000/letra/metallica/nothing-else-matters
    api.add_resource(Ajuda, '/help')                                                     # http://127:0.0.1:5000/help
    api.add_resource(Versao, '/version')                                                 # http://127:0.0.1:5000/version


    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    # app.run(host='127.0.0.1', port=port)
    # Para executar corretamente no Heroku, o host deve ser: '0.0.0.0' (https://vagalume-web-scrap.herokuapp.com/)
    app.run(host='0.0.0.0', port=port)
