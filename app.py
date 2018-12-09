#!/usr/bin/env python

""" Objetivo: Fazer um crawler que recupera dados do site ​www.vagalume.com​ em tempo de execução e
    servir os dados recuperados através de uma API Restful.
    Autor: Marcus Vinicius Laurindo da Silva
    Date de criação: 09/12/2018
    Disponível em: https://github.com/marvinsilva/webscraping-vagalume
    Python 3.7.1
"""

# Importar bibliotecas
import os               # Interfaces de sistema operacional diversas
import re               # Operações de expressão regular
import sys              # Parâmetros e funções específicos do sistema
import getopt           # Analisador para opções de linha de comando

from unicodedata import normalize   # Unicode Database. Retorna o formulário normal para o unistr da string Unicode
from crawler import WebScrap        # Importa a classe WebScrap do arquivo crawler.py para instanciar web scrap vagalume

__author__ = "[marvinsilva] Marcus Vinicius Laurindo da Silva"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Marcus Vinicius Laurindo da Silva"
__email__ = "vnc_vinicius92@hotmail.com"
__status__ = "Production"

# Instanciando a web scrap vagalume
vagalume = WebScrap()

# Variável com o nome e extensão deste arquivo
nome_arquivo = os.path.basename(__file__)

# Mensagem de erro contendo informações de utilização deste programa
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

def tratar_opcoes_comando():
    """ Analisa as opções de linha de comando e a lista de parâmetros.
        args é a lista de argumentos a ser analisada, sem a referência principal ao programa em execução.
	"""

    # Valores padrões para as veriáveis que serão utilizadas
    artista = str()
    musica = str()
    quant = 15
    todas = False

    try:
        # Define os argumentos e se estes recebem ou não funções opcionais (opts), curtas e longas
        # getopt.getopt(args, shortopts, longopts=[])
        opts, args = getopt.getopt(sys.argv[1:], "a:n:m:l:tvh",
                                   ["artista=", "numero=", "musica=", "todas", "version", "help"])
    except getopt.GetoptError as err:
        # Imprime informação de ajuda e sai:
        print(err)  # Imprime algo como: "option -x not recognized"
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-a", "--artista"):                      # Recebe em 'arg' o nome do artista
            artista = remover_acentos_char_especiais(arg)   # Trata o arg na função 'remover_acentos_char_especiais'
            if not vagalume.request(artista):               # Verifica se a URL do artista é valida no site do vagalume
                sys.exit()                                  # e caso não seja o programa termina

        elif opt in ("-n", "--numero") and artista:         # Se artista validado, recebe em 'arg'
            quant = int(arg)                                # o número de musicas top a listar
            # Caso esse número seja maior que 25, uma mensagem de erro é exibida e o programa termina
            if quant > 25:
                print("\nAtenção! O número máximo de músicas TOP é de 25")
                sys.exit()

        elif opt in ("-m", "--musica") and artista:         # Se artista validado, recebe em 'arg'
            musica = arg.upper()                            # a letra inicial da musica que deseja buscar

        elif opt in ("-t", "--todas") and artista:          # Se artista validado, recebe em 'arg' o parâmetro para
            todas = True                                    # listar todas as musicas disponíveis do artista

        elif opt in ("-h", "--help"):                       # Imprime a mensagem de ajuda sobre o programa é encerrado
            print(mensagem_ajuda)
            sys.exit()

        elif opt in ("-v", "--version"):                    # Imprime a versão e demais info sobre o programa
            print(f'Versão: {__version__}')
            print(f'Autor: {__author__}')
            print(f'E-mail: {__email__}')
            print(f'Licença: {__license__}')
            print(f'Status: {__status__}')
            sys.exit()

        # Caso o artista não tenha sido passado como argumento, uma
        # mensagem de erro é exibida e o programa é encerrado
        elif opt not in ("-a", "--artista") and opt not in ("-h", "--help"):
            print(f'\nErro: artista ou banda não reconhecido! {mensagem_ajuda}')
            sys.exit()
        # Caso seja passado um argumento não reconhecido
        else:
            assert False, "Opção não tratada"

    return artista, quant, musica, todas

def imprimir_resultado_converter_json(artista, quant, musica, todas):
    """ Função com o objetivo de analisar as opções selecionadas em linha de comando,
        percorrer a lista de músicas correspondente (top ou todas), imprimindo o resultado,
        e converter a lista em formato JSON
	"""
    # Executa a função 'search' na instancia 'vagalume' e recebe como
    # resultado as duas listas (top e todas) daquele artista
    top_musicas, alfabet_musicas = vagalume.search(artista)

    # Criação de listas vazias
    musica_por_letra = []
    formato_json = []

    if not musica and not todas:    # lista das top musicas do artista
        for seq, top in enumerate(top_musicas):
            if seq < quant:
                print(seq + 1, top)
                formato_json.append({seq + 1: top})
    else:
        if musica:  # lista de musicas de acordo com a primeira letra correspondente
            for mus in alfabet_musicas:
                if mus.startswith(musica):
                    musica_por_letra.append(mus)
                    print(mus)
                    formato_json.append({musica: mus})
        else:
            for mus in alfabet_musicas:   # lista todas as musicas do artista
                print(mus)
                formato_json.append({'musica': mus})

    print(f'\n{formato_json}')  # Imprime resultado da lista no formato JSON
    return formato_json

def main():
    """ Função principal deste software. Responsável por executar
        todas as outras funções
	"""
    # Recebe as variáveis tratadas a partir dos argumentos da linha de comando
    artista, quant, musica, todas = tratar_opcoes_comando()
    # Recebe a lista de musicas em formato JSON e imprime o resultado
    formato_json = imprimir_resultado_converter_json(artista, quant, musica, todas)

if __name__ == "__main__":
   # Chamada da função principal. Inicio do programa
   main()
