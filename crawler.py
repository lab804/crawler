#!/usr/bin/env python3

import requests
import re, os
import imaplib
import getpass
from pprint import pprint
import pymongo

# sessao global
session = requests.Session()

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = '993'
FROM = '(FROM "dados_pcd@cemaden.gov.br")'
EMAIL_ADDRESS = "dados_pcd@cemaden.gov.br"
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DOCUMENT_NAME = 'test'
COLLECTION_NAME = 'service'


def acessa_site(url):
    """acessa o site para gerar a sessao"""
    req = session.get(url, timeout=10)
    if req.status_code != 200:
        print("Erro na conexao")
        return None
    else:
        return req.content

def organiza_dados(content, base_url):
    cities_state = re.findall(b'\(\"(\w{2})\"\,\"(.*?)\"\,\"(\d+)\"', content)
    return cities_state

def formata_url_path(base_url, state, c):
    cities = c.replace(b" ", b"+")
    state = state.decode()
    print(state)
    cities = cities.decode()
    print(cities)
    base = '?idUF={est}&idCidade={city}&edMes=2&edAno=2017&edNome=Barbara&edEmail=scraping.camaden%40gmail.com&palavra='
    baseurl = base.format(est=state, city=cities)
    url_path = base_url+baseurl
    return url_path

def captura_captcha(url):
    fname = 'captcha.jpg'
    resp = session.get(url)
    with open(fname, 'wb') as f:
        try:
            f.write(resp.content)
            return True
        except Exception as e:
            print("Erro ao salvar o captcha: %s" % e)
            return False

def preenche_formulario(formulario):
    """preenche formulario para receber o email"""
    response = session.get(formulario)
    if response.status_code == 200:
        return True
    else:
        print("Formulario contem erros. Tente novamente...")
        return False

def salva_captcha_bd(cap_code):
    """Salva os codigos dos captchas ao final do arquivo captcha.csv"""
    try:
        arq = open('captcha.csv','a+')
        arq.writelines(cap_code+'\n')
        print("Registro do captcha gravado com sucesso")
        arq.close()
    except IOError:
        print("Erro ao abrir o arquivo captcha!")

def salva_captcha_img(cap_code):
    namecap = 'cap/'+cap_code+'.jpg'
    os.rename('captcha.jpg', namecap)
    print("Imagem captcha salva com sucesso")

def login_email(imap, email, senha):
    imap.login(email, senha)
    imap.select('Inbox')

def verifica_novo_email(imap):
    status, data = imap.search(None, FROM)
    return sum(1 for num in data[0].split())

def ler_email(imap, link_re, num):
    """ler os emails para capturar os que links que possuem
    o dowload do arquivo csv"""
    status, data = imap.fetch(num, '(RFC822)')
    print(num)
    # print ('Message %s\n%s\n' % (num, data[0][1]))
    return data[0][1]

def download_arquivo(url):
    """realiza o download do arquivo que contem
    os dados metereologicos daquela estacao"""
    linkname = url.split('/')[-1]
    local_filename = ('arq/'+linkname+'.csv')
    r = session.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.close()
                return local_filename
            else:
                return False

def ler_arquivo(content, num, imap):
    """le o arquivo e checa se tem conteudo"""
    if os.path.isfile(content):
        if os.path.getsize(content) > 0:
            keys = open(content, "r").readline().strip().split(";" or "\n")
            if keys[0] == 'municipio':
                return keys
            else:
                print("Arquivo nao foi lido. Download já foi realizado ou a sessao expirou!")
        else:
            print("Arquivo vazio!")

    else:
        print("Arquivo nao existe. Verifique se o nome ou diretório esta correto!")

    imap.store(num, '+FLAGS', r'\Deleted')
    imap.expunge()
    return False

def parsea_dados(keys, content):
    """limpamos os dados e estruturamos de uma forma
    que se encaixe no banco de dados"""
    data_file = []
    with open(content, 'rb') as csvfile:
        for line in csvfile.readlines():
            b = line.strip().replace(b"\t", b"")
            b_as_list = b.split(b";")
            dic = {}
            for data in b_as_list:
                if data:
                    dec = data.decode()
                    dic[keys[b_as_list.index(data)]] = dec
            data_file.append(dic)
    if len(data_file) < 2:
        print ("Arquivo nao contem dados. Verifique se ha dados no site!")
    else:
        del data_file[0]
        print(data_file)
        return data_file

def busca_registro(registro, data_hora=None):
    "busca no arquivo csv o dado anterior salvo no banco de dados: caso\
    tenha sucesso, apaga os dados anteriores; caso contrario, returna erro"
    for item in registro:
        print(item)
        print(data_hora)
        if data_hora:
        # if item['datahora'] == data_hora:
            print("Achei esta ultima data")
            return True
        else:
            print("Nao achei esta ultima data")
            return False

def conecta_mongodb():
    try:
        database_info=[]
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[DOCUMENT_NAME]
        collection = db[COLLECTION_NAME]
        return collection
    except Exception as e:
        print("Erro ao inserir dados")
        print(e)
        return False

def ultima_data(collection):
    """retorna dicionario com o ultimo documento inserido
    no banco de dados"""
    results = collection.find().limit(2).sort([("datahora", pymongo.DESCENDING)])
    if results.count()>0:
        for record in results:
            record = record['datahora'].decode()
            print(record)
            return record
    else:
        return False

def imprime_mongodb(collection):
    cursor = collection.find({})
    for document in cursor:
        pprint(document)

def inserir_dados(collection, documento):
    """insere o documento no banco de dados"""
    try:
        for dados in documento:
            collection.insert(dados)
        return True
    except Exception as e:
        print("Erro ao inserir os dados")
        print(e)
        return False

def main():
    """funcao principal"""
    base_url = "http://150.163.255.234/salvar/mapainterativo/downpluv.php"
    url_img = 'http://150.163.255.234/salvar/mapainterativo/securimage/securimage_show.php'
    imap_username = 'scraping.camaden@gmail.com'
    link_re = re.compile(b'href=\'(.*)?\'')
    database = conecta_mongodb()
    content = acessa_site(base_url)
    if not content:
        return
    else:
        # cities = organiza_dados(content, base_url)
        # for city in cities:
        #     url_format = formata_url_path(base_url, city[0], city[1])
        #     try:
        #         iscaptcha = captura_captcha(url_img)
        #         if iscaptcha:
        #             cap = input("Me fale as letras senhorita? ")
        #             print (cap)
        #             url_final = url_format+cap
        #             print(url_final)
        #             isget = preenche_formulario(url_final)
        #             if isget:
        #                 salva_captcha_img(cap)
        #                 salva_captcha_bd(cap)
        #         else:
        #             print("Ops! nao foi possivel baixar o captcha, cheque a url ou se algo mudou no site.")
        #     except requests.exceptions.HTTPError as e:
        #             print("%s '%s'" % (e, url))
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap_password = getpass.getpass("Enter your password --> ")
        login_email(imap, imap_username, imap_password)
        inbox = verifica_novo_email(imap)
        if inbox != 0:
            status, data = imap.search(None, FROM)
            for num in reversed(data[0].split()):
                data = ler_email(imap, link_re, num)
                link_download = link_re.findall(data)
                url_str= (b''.join(link_download).decode())
                isdownload = download_arquivo(url_str)
                if isdownload:
                    print("Sucesso no download do arquivo csv")
                    isvalid = ler_arquivo(isdownload, num, imap)
                    if isvalid:
                        if database:
                            ultimo_registro = ultima_data(database)
                            if not ultimo_registro:
                                print("Não ha registros anteriores no MongoDB. O arquivo de dados será lido por completo!")
                                dados = parsea_dados(isvalid, isdownload)
                                registrar = inserir_dados(database, dados)
                                if registrar:
                                    print("Dados inseridos com sucesso no MongoDB")
                                    imap.store(num, '+FLAGS', r'\Deleted')
                                    imap.expunge()
                                    print("Email contendo arquivo dos dados inseridos foi excluido")
                                else:
                                    print("Ocorreu um erro na insercao do dados no MongoDB")
                            else:
                                print("Ultimo registro encontrado. O arquivo de dados será lido a partir da ultima data registrada no MongoDB")
                                dados = parsea_dados(isvalid, isdownload)
                                registro = busca_registro(dados, ultimo_registro)
                                if registro:
                                    registrar = inserir_dados(database, dados)
                                    if registrar:
                                        print("Dados inseridos com sucesso no MongoDB")
                                        imap.store(num, '+FLAGS', r'\Deleted')
                                        imap.expunge()
                                        print("Email contendo arquivo dos dados inseridos foi excluido")
                                    else:
                                        print("Ocorreu um erro na insercao do dados no MongoDB")
                                else:
                                    print("A busca pelo dados do ultimo registro nao teve sucesso!")
                        else:
                            print("Erro ao se conectar com o MongoDB")
                else:
                    print("Arquivo invalido")
        else:
            print("Nao ha emails na caixa de entrada!")

if __name__ == "__main__":
    main()
