## webscraping-vagalume

O projeto web-scraping-vagalume tem como principal objetivo executar um web scraping* no site vagalume.com.br recuperando os dados em tempo de execução
e atender a requisição para as seguintes funcionalidades:

1. Retornar as 15 primeiras músicas do TOP de um artista;
2. Retornar um número específico de músicas do TOP de um artista (sendo no máximo 25);
3. Retornar as músicas de um artista baseado na primeira letra do título da música;
4. Retornar todas as músicas do artista;
5. Retornar a letra de uma música específica. 

*Web Scraping é uma técnica de extração de dados utilizada para coletar dados de sites.*

Para atender os objetivos do projeto, foram desenvolvidos três programas com modo de execução e diferentes tarefas.

### crawler.py: 
Responsável por realizar a extração dos dados no site vagalume.com.br

### app.py:
Utiliza o analizador de argumentos de linha de comando para selecionar as requisições, executar o programa crawler e exibir o resultado para o usuário

### web.py: 
Utiliza a API Restful* com diferentes Endpoints para receber e tratar diferentes requisições, executar o programa crawler e disponibilizar o resultado nos mesmo Endpoints

*API Restful:*

---
A seguir, será descrito o modo de execuçaõ dos softwares 'app.py' e 'web.py':

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
Os Endpoints desta solução estão disponibilizados em um servidor público e podem ser acessados e testados em: https://vagalume-web-scrap.herokuapp.com/<br>

1. Retornar as 15 primeiras músicas do TOP de um artista<br>
Receber uma requisição em um endpoint com o nome do artista e listar as 15 primeiras músicas do TOP do artista<br>
__/top/[artista]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/top/metallica
```
2. Retornar um número específico de músicas do TOP de um artista (sendo no máximo 25)<br>
No mesmo endpoint do item anterior, receber uma indicação de quantas músicas do TOP do artista você vai listar<br>
__/top/[artista]/[numeroDeMusicasTop]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/top/metallica/10
```
3. Retornar as músicas de um artista baseado na primeira letra do título da música<br>
Receber uma requisição em um endpoint com o nome do artista e a primeira letra do título e listar as músicas<br> 
__/top/[artista]/[primeiraLetraDoTituloDaMusica]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/top/metallica/a
```
4. Retornar todas as músicas do artista<br>
Receber uma requisição em um endpoint com o nome do artista e listar todas as músicas dele<br>
__/todas/[artista]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/todas/metallica
```
5. Retornar a letra de uma música específica<br>
Receber uma requisição em um endpoint com o nome do artista e o título da música e exibir a letra da música<br>
__/letra/[artista]/[tituloDaMusica]__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/letra/metallica/nothing-else-matters
```
6. Retornar a versão e demais informações sobre o software<br>
__/version__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/version
```
7. Retornar as informções de ajuda sobre o software<br>
__/help__
```
Exemplo:
https://vagalume-web-scrap.herokuapp.com/help
```
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
