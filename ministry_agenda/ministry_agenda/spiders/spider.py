from bs4 import BeautifulSoup
import scrapy
import pandas as pd
import random


class MinistrySpider(scrapy.Spider):
    name = 'Ministryspider'
    start_urls = ['http://www.economia.gov.br/agendas/gabinete-do-ministro/ministro-da-economia/paulo-guedes/']
    MinistryName = 'Ministério da Economia'
    MinisterName = 'Paulo Guedes'
    id_ = []
    
    
    def parse(self, response):
        
        soup = BeautifulSoup(response.body, 'lxml')
    
        #extraindo os dados
        eventos = response.xpath('//div[@class="comprimisso-dados"]').getall()
        evento_titulo = [x.string for x in soup.select('.comprimisso-titulo')] #Sim, a classe se chama comprimisso
        evento_data = response.xpath('//time[@class="horario comprimisso-inicio"]/@datetime').getall()
        evento_local = [x.text for x in soup.select('.comprimisso-local')]
        evento_participantes = response.xpath('//p[@class="comprimisso-participantes"]').getall()
        dias = response.xpath('//a[@title="Agenda"]/@href').getall()
        meses = self.url_months(response)
            
        #tratando dados ausentes e retornando um dicionario com locais e participantes
        d_locais = self.trata_local(response, evento_local)
        d_participantes = self.trata_participantes(response, evento_participantes)
        
        self.salva_csv(evento_titulo, evento_data, d_locais, d_participantes)
        

        #percorrendo os links do calendario
        for dia in dias:
            yield scrapy.Request( str(dia), callback=self.parse)
        
        for mes in meses:
            yield scrapy.Request( str(mes), callback=self.parse)


    def url_months(self, response):
        meses_table = response.xpath('//table[@id="t-2020"]').getall()
        soup = BeautifulSoup(meses_table[0], 'lxml')
        meses = soup.find_all('a', href=True)
        url_meses = [mes['href'] for mes in meses]        
                
        return url_meses


    def trata_local(self, response, el): # Atribui N/A para locais ausentes
        dados = response.xpath('//div[@class="comprimisso-dados"]').getall()
        dicionario = {}

        y=0
        for i in range(0, len(dados)):
            if dados[i].find("comprimisso-local") == -1:
                dicionario[i] = "N/A"
            else:
                dicionario[i] = el[y].replace('\n', '').replace('Local:', '')               
                y=y+1
        return dicionario

    def trata_participantes(self, response, ep):  # Atribui N/A para participantes ausentes
        dados = response.xpath('//div[@class="comprimisso-dados"]').getall()
        dicionario = {}
        
        y=0
        for i in range(0, len(dados)):
            if dados[i].find("comprimisso-participantes") == -1:
                dicionario[i] = "N/A"
            else:   # Elimina tags presentes na string
                string = ep[y]
                dicionario[i] = string[56:]     # Elimina <p class="comprimisso-participantes ..." 
                dicionario[i] = dicionario[i].replace('\r<br>', ', ').replace('</p>', '').replace('>', '').split(', ')
                y = y+1
        return dicionario
        

    def salva_csv(self, et, ed, dl, dp):
        df = pd.DataFrame(columns = ['id', 'MinistryName', 'MinisterName', 'EventDate', 'EventTitle', 'EventLocation', 'EventParticipants'])

        for i in range(0, len(et)):
            id_aux = random.randrange(10000)
            while id_aux in self.id_:
                id_aux = random.randrange(10000)    
            self.id_.append(id_aux)

            dicionario = {'id': id_aux, 'MinistryName': self.MinistryName, 'MinisterName': self.MinisterName, 
            'EventDate': ed[i] , 'EventTitle': et[i], 'EventLocation': [dl[i]], 'EventParticipants': [dp[i]]}
            df_aux = pd.DataFrame(dicionario, index=[0])
            df = df.append(df_aux, ignore_index=True)
    
        
        with open('data.csv', 'a', encoding="utf-8") as f:
            df.to_csv(f, header=f.tell()==0, index=False)
        