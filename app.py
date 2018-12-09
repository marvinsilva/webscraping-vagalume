import getopt
import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

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

        if opt in ("-a", "--artista"):
            print(f' artista {arg}')
            artista = arg

        elif opt in ("-n", "--numero"):
            quant = int(arg)

        elif opt in ("-m", "--musica"):
            musica = arg.upper()

        elif opt in ("-t", "--todas"):
            todas = True

        elif opt in ("-h", "--help"):
            print("Help")
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
