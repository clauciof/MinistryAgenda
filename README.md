# Ministy-Agenda
Python Scraping  da agenda do Ministerio da Economia presente no site do ministério

## Descrição 
Scraping feito utilizando o framework Scrapy e Python. A partir da página do [ministério da economia] (http://www.economia.gov.br/agendas/gabinete-do-ministro/ministro-da-economia/paulo-guedes/) extrai-se a agenda do ministro Paulo Guedes
Após coletar os dados o spider cria um dataset e salva no arquivo criado data.csv 
O Crawler é executado no arquivo crawler.py. Primeiro ele lê o arquivo offers.csv onde estão localizados os 40 000 links.
Após finalizar a coleta, os dados coletados (nome do produto, preço, nome do site e link) são salvos em um banco de dados MySQL trabalhando localhost ( nome do banco etl ) . Também é criado um arquivo dados.csv com os mesmos dados.

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


## Autor

* **Cláucio Gonçalves Mendes de Carvalho Filho** - (https://github.com/clauciof)


