
## Web Scraping Vagalume
---
O projeto tem como principal objetivo executar web scraping no site vagalume.com.br recuperando os dados em tempo de execução e atender a requisição para as seguintes funcionalidades:

1. Retornar as 15 primeiras músicas do TOP de um artista;
2. Retornar um número específico de músicas do TOP de um artista (sendo no máximo 25);
3. Retornar as músicas de um artista baseado na primeira letra do título da música;
4. Retornar todas as músicas do artista;
5. Retornar a letra de uma música específica. 

Para atender os objetivos do projeto, foram desenvolvidos três programas com modo de execução e diferentes tarefas.

### crawler.py: 
Responsável por realizar a extração dos dados no site vagalume.com.br

### app.py:
Utiliza o analizador de argumentos de linha de comando para selecionar as requisições, executar o programa crawler e exibir o resultado para o usuário

### web.py: 
Utiliza a API Restful com diferentes Endpoints para receber e tratar diferentes requisições, executar o programa crawler e disponibilizar o resultado nos mesmo Endpoints

*API: API é um conjunto de rotinas e padrões de programação para acesso a um aplicativo de software ou plataforma baseado na Web. A sigla API refere-se ao termo em inglês "Application Programming Interface" que significa em tradução para o português "Interface de Programação de Aplicativos".*

*REST: A Representational State Transfer (REST), em português Transferência de Estado Representacional, é um estilo de arquitetura que define um conjunto de restrições e propriedades baseados em HTTP. Web Services que obedecem ao estilo arquitetural REST, ou web services RESTful, fornecem interoperabilidade entre sistemas de computadores na Internet.*

*Web Scraping: técnica de extração de dados utilizada para coletar dados de sites.*

---
Segue modo de operação dos softwares desenvolvidos neste projeto:

### app.py
uso: python app.py -a "nome do artista ou banda" [opcoes] ... 
[-a --artista | -n --numero | -m --musica | -l --letra | -t --todas | -v --versao | -h --help]

1. Retornar as 15 primeiras músicas do TOP de um artista
```python
python app.py -a "metallica"
python app.py --artista "metallica"
```
2. Retornar um número específico de músicas do TOP de um artista (sendo no máximo 25)
```python
python app.py -a "metallica" -n 10
python app.py --artista "metallica" --numero 10
```
3. Retornar as músicas de um artista baseado na primeira letra do título da música
```python
python app.py -a "metallica" -m a
python app.py --artista "metallica" --musica a
```
4. Retornar todas as músicas do artista
```python
python app.py -a "metallica" -t
python app.py --artista "metallica" --todas
```
5. Retornar a letra de uma música específica 
```python
python app.py -a "metallica" -l "nothing else matters"
python app.py --artista "metallica" --letra"nothing else matters"
```
6. Retornar a versão e demais informações sobre o software
```python
python app.py -v
python app.py --version
```
7. Retornar as informções de ajuda sobre o software
```python
python app.py -h
python app.py --help
```
---
### web.py
Os Endpoints desta solução estão disponibilizados em um servidor público e podem ser acessados e testados em: 
```
https://vagalume-web-scrap.herokuapp.com/
```

1. Retornar as 15 primeiras músicas do TOP de um artista<br>
Recebe uma requisição em um endpoint com o nome do artista e lista as 15 primeiras músicas do TOP do artista<br>
__/top/[artista]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/top/metallica
```
![alt text](https://github.com/marvinsilva/webscraping-vagalume/blob/master/images/top.PNG "top")

2. Retornar um número específico de músicas do TOP de um artista (sendo no máximo 25)<br>
No mesmo endpoint do item anterior, recebe uma indicação de quantas músicas do TOP do artista serão listadas<br>
__/top/[artista]/[numeroDeMusicasTop]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/top/metallica/10
```
![alt text](https://github.com/marvinsilva/webscraping-vagalume/blob/master/images/top_dez.PNG "top dez")

3. Retornar as músicas de um artista baseado na primeira letra do título da música<br>
Recebe uma requisição em um endpoint com o nome do artista e a primeira letra do título e lista as músicas que começam com a letra<br> 
__/top/[artista]/[primeiraLetraDoTituloDaMusica]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/top/metallica/a
```
![alt text](https://github.com/marvinsilva/webscraping-vagalume/blob/master/images/top_a.PNG "top a")

4. Retornar todas as músicas do artista<br>
Recebe uma requisição em um endpoint com o nome do artista e lista todas as músicas daquele artista<br>
__/todas/[artista]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/todas/metallica
```
![alt text](https://github.com/marvinsilva/webscraping-vagalume/blob/master/images/todas.PNG "todas")

5. Retornar a letra de uma música específica<br>
Recebe uma requisição em um endpoint com o nome do artista e o título da música e exibi a letra da música<br>
__/letra/[artista]/[tituloDaMusica]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/letra/metallica/nothing-else-matters
```
![alt text](https://github.com/marvinsilva/webscraping-vagalume/blob/master/images/letra.PNG "letra")

6. Retornar a versão e demais informações sobre o software<br>
__/version__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/version
```
![alt text](https://github.com/marvinsilva/webscraping-vagalume/blob/master/images/version.PNG "version")

7. Retornar as informções de ajuda sobre o software<br>
__/help__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/help
```
![alt text](https://github.com/marvinsilva/webscraping-vagalume/blob/master/images/help.PNG "help")

Exemplos dos memos Endpoints aplicados em servidor local [host:port] = 127:0.0.1:5000:
```
http://127:0.0.1:5000/top/metallica
http://127:0.0.1:5000/top/metallica/10
http://127:0.0.1:5000/top/metallica/a
http://127:0.0.1:5000/todas/metallica
http://127:0.0.1:5000/letra/metallica/nothing-else-matters
http://127:0.0.1:5000/version
http://127:0.0.1:5000/help
```
