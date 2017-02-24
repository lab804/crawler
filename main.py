#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
import requests
import re
import os

# armazenamos a sessao da requisicao (cookies, sessions, headers...)
session = requests.Session()

def start():
    """ start captura dados url"""
    urlsite = 'http://150.163.255.234/salvar/mapainterativo/downpluv.php'
    response = session.get(urlsite)
    cities_state = re.findall('\(\"(\w{2})\"\,\"(.*?)\"\,\"(\d+)\"', response.text)
    for cities in cities_state:
        url_complete(urlsite, cities[0], cities[1])

def captcha(url):
    """ download captcha """
    fname = 'captcha.jpg'
    resp = session.get(url)
    with open(fname, 'wb') as f:
        try:
            f.write(resp.content)
            return True
        except Exception as e:
            print("erro ao salvar o captcha: %s" % e)
            return False

def url_complete(urlsite, state, cities):
    """ trata os dados coletados e mundo a url completa"""
    urlimagem = 'http://150.163.255.234/salvar/mapainterativo/securimage/securimage_show.php'
    path = formating(urlsite, state, cities)
    print(path)
    try:
        iscaptcha = captcha(urlimagem)
        if iscaptcha:
            cap = input("Me fale as letras senhorita? ")
            finalurl = path+cap
            response = session.get(finalurl)
            if response.status_code == 200:
                write_file(cap)
                rename_file(cap)
                print(response.content)
            else:
                print("Deu pau, tente novamente...")
        else:
            print("ops nao foi possivel baixar o captcha, cheque a url ou se algo mudou no site.")
    except requests.exceptions.HTTPError as e:
        print("%s '%s'" % (e, url))

def formating(urlsite, state, c):
    """formata path a partir dos dados coletaods"""
    cities = c.replace(" ", "+")
    print(cities)
    base = '?idUF={est}&idCidade={city}&edMes=2&edAno=2017&edNome=Barbara&edEmail=barbara%40lab804.com.br&palavra='
    baseurl = base.format(est=state, city=cities)
    urlpath = urlsite+baseurl
    return urlpath

def rename_file(cap_code):
    """renomeia arquivo captcha com nome-codigo"""
    namecap = 'cap/'+cap_code+'.jpg'
    os.rename('captcha.jpg', namecap)

def write_file(cap_code):
    """registra os codigos do captcha atual ao final do arquivo csv"""
    try:
        arq = open('captcha.csv','a+')
        arq.writelines('\n'+cap_code)
        print("Registro gravado com sucesso")
        arq.close()
    except IOError:
        print("Erro ao abrir o arquivo!")

if __name__ == "__main__":
    print("CTRL+C para sair")

    while True:
        start()
