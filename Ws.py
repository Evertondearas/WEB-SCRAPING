import os 
import requests 
from bs4 import BeautifulSoup, SoupStrainer 
import re 
import zipfile 

def baixa_arquivos(link, local):
    
    response = requests.get(link, stream=True) 
    
    if response.status_code == 200:
        with open(local, mode='wb') as file: 
            for pedaco in response.iter_content(chunk_size=10240): 
               
                if(pedaco):
                    file.write(pedaco)

def zipa_arquivos(nome_zip, files):
    
    with zipfile.ZipFile(nome_zip, 'w') as zipf: 
        for arquivo in files:
            zipf.write(arquivo, os.path.basename(arquivo))

#Link da página onde os pdf´s vão ser baixados
LINK = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

list_files = []

response = requests.get(LINK) 
if response.status_code == 200:
    #Filtrando html para trazer apenas as tags <a> que tenha no href algo que comece com "Anexo" e termine com "pdf"
    filter_soup = SoupStrainer('a', href=re.compile(r'Anexo.*\.pdf$')) 
    soup = BeautifulSoup(response.text, 'html.parser', parse_only=filter_soup) #trazendo apenas as partes filtradas do html (<a>)
            
    #iterando sobre as tags filtradas        
    for link in soup:  
    
        href = link.get('href') #pega o link do href 
        destino = link.string + '.pdf'#pega o que está digitado no valor da tag o que resulta em uma string com início "anexo" e fim "pdf"    
        list_files.append(destino)
        baixa_arquivos(href, destino) 

    zipa_arquivos('Anexos.zip', list_files) 