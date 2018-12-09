from bs4 import BeautifulSoup                   # lib para análise e extração de dados da pagina HTML
from urllib.request import Request, urlopen     # lib para requisição HTTP da pagina
from urllib.error import URLError, HTTPError    # lib para tratamento de erros de requição

class WebScrap:
    """ Classe com objetivo de encapsular o crawler da URL valagume.com.br
    """

    def request(self, artista):
        """ Valida a requisição do artista ou banda na URL valagume.com.br
            de modo a verificar se o link realmente é valido
        """
        url = f'https://www.vagalume.com.br/{artista}/'     # link de busca do artista ou banda
        req = Request(url)      # executa a requisição para o site

        try:
            # Abre a URL que pode ser tanto uma String quanto um objeto Request
            # Ref.: # https://docs.python.org/3/library/urllib.error.html
            response = urlopen(req)
        except HTTPError as e:
            # Apesar de ser uma exceção (uma subclasse de URLError),
            # um HTTPError também pode funcionar como um valor de retorno semelhante a um arquivo não excepcional
            print('Código do erro: ', e.code)
            print(f'Não foi possível atender à solicitação para URL {url}')
            print(f'Favor verificar se o nome do artista ou banda está correto: {artista}')
            return False
        except URLError as e:
            # É uma subclasse do OSError
            print('Não conseguimos chegar a um servidor.')
            print('Motivo: ', e.reason)
            return False
        else:   # Caso a URL seja valida
            print("Solicitação requerida com sucesso!")
            print(f'Buscando por: {artista} ...')
            return True

    def search(self, artista):
        """ Executa o web scrap no site do vagalume retornando duas listas:
            lista das musicas TOP e lista de todas as musicas do artista
            correspondente passado como argumento na função
        """

        url = f'https://www.vagalume.com.br/{artista}/'     # link de busca do artista ou banda
        print(f'URL: {url}')
        documento_html = urlopen(url).read()    # recebe documento HTML
        # Criando uma instância da classe BeautifulSoup para analisar o documento_html
        soup = BeautifulSoup(documento_html, "html.parser")

        # Criando duas listas vazias
        top_musicas = []
        alfabet_musicas = []

        # Para cada titulo de musica no centexto das musicas top
        # do artista, acrescenta o item na lista de musicas top
        for top in soup.find(id="topMusicList").find_all("a", class_="nameMusic"):
            top_musicas.append(top.get_text())

        # Para cada titulo de musica no centexto de todas as músicas
        # do artista, acrescenta o item na lista de todas musicas
        for top in soup.find(id="alfabetMusicList").find_all("a", class_="nameMusic"):
            alfabet_musicas.append(top.get_text())

        return top_musicas, alfabet_musicas
