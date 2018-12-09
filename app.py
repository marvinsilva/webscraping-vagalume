import os
import re
import getopt
import sys
from crawler import WebScrap
from unicodedata import normalize

vagalume = WebScrap()

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
                    \n-h   :   imprime a mensagem de ajuda deste programa\
                    \nNota :   \
                    \n- O numero maximo de musicas TOP e de 25 musicas\
                    \n- O nome do artista ou banda nao e opcional"

def remover_acentos_char_especiais(txt):
    rm_acentos = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    rm_char_especiais = re.sub('[^A-Za-z0-9 ]+', '', rm_acentos)
    return rm_char_especiais.replace(" ", "-").lower()

def tratar_opcoes_comando():
    artista = str()
    musica = str()
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

        if opt in ("-a", "--artista"):
            artista = remover_acentos_char_especiais(arg)
            if not vagalume.request(artista):
                sys.exit()

        elif opt in ("-n", "--numero") and artista:
            quant = int(arg)
            if quant > 25:
                print("\nAtenção! O número máximo de músicas TOP é de 25")
                sys.exit()

        elif opt in ("-m", "--musica") and artista:
            musica = arg.upper()

        elif opt in ("-t", "--todas") and artista:
            todas = True

        elif opt in ("-h", "--help"):
            print(mensagem_ajuda)
            sys.exit()

        elif opt not in ("-a", "--artista") and opt not in ("-h", "--help"):
            print(f'\nErro: artista ou banda não reconhecido! {mensagem_ajuda}')
            sys.exit()

        else:
            assert False, "Opção não tratada"

    return artista, quant, musica, todas

def imprimir_resultado_converter_json(artista, quant, musica, todas):

    top_musicas, alfabet_musicas = vagalume.search(artista, quant, musica, todas)
    musica_por_letra = []
    formato_json = []

    if not musica and not todas:    # lista das top musicas do artista
        for seq, top in enumerate(top_musicas):
            if seq < quant:
                print(seq + 1, top)
                formato_json.append({seq + 1: top})
    else:
        if musica:  # lista musicas de acordo com a primeira letra correspondente
            for mus in alfabet_musicas:
                if mus.startswith(musica):
                    musica_por_letra.append(mus)
                    print(mus)
                    formato_json.append({musica: mus})
        else:
            for mus in alfabet_musicas:   # lista todas as musicas do artista
                print(mus)
                formato_json.append({'musica': mus})

    print(f'\n{formato_json}')
    return formato_json

def main():
    artista, quant, musica, todas = tratar_opcoes_comando()
    formato_json = imprimir_resultado_converter_json(artista, quant, musica, todas)

if __name__ == "__main__":
    main()
