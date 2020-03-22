# Ministy-Agenda
Python Scraping  da agenda do Ministerio da Economia presente no site do ministério

## Descrição 
Scraping feito utilizando o framework Scrapy e Python. A partir da página do [ministério da economia](http://www.economia.gov.br/agendas/gabinete-do-ministro/ministro-da-economia/paulo-guedes/) extrai-se a agenda do ministro Paulo Guedes
Após coletar os dados o spider cria um dataset e salva no arquivo criado data.csv 

### Pré Requisitos

Python3 e bibliotecas BeautifulSoup4, Pandas e Scrapy.

#### Instalação
```
pip install pandas
pip install Scrapy
pip install bs4
```

### Execução
No diretório /spiders executar o comando:
```
scrapy runspider spider.py
```

## Visualização do dataset

![alt Text](https://github.com/clauciof/Ministy-Agenda/blob/master/visualizacao.png)



## Autor

* **Cláucio Gonçalves Mendes de Carvalho Filho** - (https://github.com/clauciof)


