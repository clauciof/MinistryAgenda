from bs4 import BeautifulSoup
import scrapy
import pandas as pd


class MinistrySpider(scrapy.Spider):
    name = 'Ministryspider'
    start_urls = ['http://www.economia.gov.br/agendas/gabinete-do-ministro/ministro-da-economia/paulo-guedes/2020-03-09/']
    MinistryName = 'Ministério da Economia'
    MinisterName = 'Paulo Guedes'
    
    def parse(self, response):
        
        soup = BeautifulSoup(response.body, 'lxml')
    
        #extraindo os dados
        events = response.xpath('//div[@class="comprimisso-dados"]').getall()
        event_title = [x.string for x in soup.select('.comprimisso-titulo')] #Sim, a classe se chama comprimisso
        event_date = response.xpath('//time[@class="horario comprimisso-inicio"]/@datetime').getall()
        event_location = [x.text for x in soup.select('.comprimisso-local')]
        event_participants = response.xpath('//p[@class="comprimisso-participantes"]').getall()
        dia_atual = [ s for s in soup.select('.agenda-dia')[0].text.split() if s.isdigit() ]
        
        
        #tratando dados ausentes...
        d_locals = self.trata_local(response, event_location)
        d_participants = self.trata_participantes(response, event_participants)
        
        self.salva_csv(event_title, event_date, d_locals, d_participants)

    def trata_local(self, response, el):
        dados = response.xpath('//div[@class="comprimisso-dados"]').getall()
        dicionario = {}

        y=0
        for i in range(0, len(dados)):
            if dados[i].find("comprimisso-local") == -1:
                dicionario[i] = "N/A"
            else:
                dicionario[i] = el[y].replace('\n', '')
                y=y+1
        return dicionario

    def trata_participantes(self, response, ep):
        dados = response.xpath('//div[@class="comprimisso-dados"]').getall()
        dicionario = {}
        
        y=0
        for i in range(0, len(dados)):
            if dados[i].find("comprimisso-participantes") == -1:
                dicionario[i] = "N/A"
            else:
                string = ep[y]
                dicionario[i] = string[56:] # 56 = len(<p class="comprimisso-participantes ...")
                dicionario[i] = dicionario[i].replace('\r<br>', ', ')
                dicionario[i] = dicionario[i].replace('</p>', '')
                dicionario[i] = dicionario[i].replace('>', '')
                dicionario[i] = dicionario[i].split(', ')
                y = y+1
        return dicionario
        

    def salva_csv(self, et, ed, dl, dp):
        df = pd.DataFrame(columns = None)
    
        
        for i in range(0, len(et)):
            dicionario = {'MinistryName': self.MinistryName, 'MinisterName': self.MinisterName, 
            'EventDate': ed[i] , 'EventTitle': et[i], 'EventLocation': [dl[i]], 'EventParticipants': [dp[i]]}
            _df = pd.DataFrame(dicionario, index=[0])
            df = df.append(_df, ignore_index=True)
    


        with open('data.csv', 'a', encoding="utf-8") as f:
            df.to_csv(f, header=f.tell()==0, index=False)