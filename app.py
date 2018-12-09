import getopt
import sys
import re
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from unicodedata import normalize

nome_arquivo = os.path.basename(__file__)

mensagem_ajuda = f"\nuso: python {nome_arquivo} -a \"nome do artista ou banda\" [opcoes] ... \
                    \n[-a --artista | -n --numero | -m --musica | -l --letra " \
                    f"| -t --todas | -v --versao | -h --help]\
                    \nopcoes e argumentos:\
                    \n-a   :   nome do artista ou banda para pesquisa\
                    \n-n   :   numero especifico de musicas do TOP de um artista\
                    \n-m   :   musicas de um artista baseado na primeira letra do titulo\
                    \n-l   :   musica especifica para pesquisa da respectiva letra\
                    \n-t   :   todas as musicas do artista\
                    \n-v   :   imprime a versao do software\
                    \n-h   :   imprime a mensagem de ajuda deste programa\n"

def remover_acentos_char_especiais(txt):
    rm_acentos = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    rm_char_especiais = re.sub('[^A-Za-z0-9 ]+', '', rm_acentos)
    return rm_char_especiais.replace(" ", "-").lower()

def request(artista):
    url = f'https://www.vagalume.com.br/{artista}/'
    req = Request(url)
    try:
        response = urlopen(req)
    except HTTPError as e:
        print('Código do erro: ', e.code)
        print(f'Não foi possível atender à solicitação para URL {url}')
        print(f'Favor verificar se o nome do artista ou banda está correto: {artista}')
        return False
    except URLError as e:
        print('Não conseguimos chegar a um servidor.')
        print('Motivo: ', e.reason)
        return False
    else:
        print("Solicitação requerida com sucesso!")
        print(f'Buscando por: {artista} ...')
        return True

def main():
    artista = ''
    musica = ''
    quant = 15
    todas = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:n:m:l:tvh",
                                   ["artista=", "numero=", "musica=", "todas", "help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for opt, arg in opts:

        if opt not in ("-a", "--artista") and opt not in ("-h", "--help"):
            print(f'\nErro: artista ou banda não reconhecido!')
            sys.exit()

        elif opt in ("-a", "--artista"):
            artista = remover_acentos_char_especiais(arg)
            if not request(artista):
                sys.exit()

        elif opt in ("-n", "--numero"):
            quant = int(arg)

        elif opt in ("-m", "--musica"):
            musica = arg.upper()

        elif opt in ("-t", "--todas"):
            todas = True

        elif opt in ("-h", "--help"):
            print(mensagem_ajuda)
            sys.exit()

    url = f'https://www.vagalume.com.br/{artista}/'
    print(url)
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    top_musicas = []
    alfabet_musicas = []

    for top in soup.find(id="topMusicList").find_all("a", class_="nameMusic"):
        top_musicas.append(top.get_text())

    for top in soup.find(id="alfabetMusicList").find_all("a", class_="nameMusic"):
        alfabet_musicas.append(top.get_text())

    print(f'top: {top_musicas}')
    print(f'alfabetic {alfabet_musicas}')


if __name__ == "__main__":
    main()
