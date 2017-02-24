#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
import requests
import re
import shutil
import os

# armazenamos a sessao da requisicao (cookies, sessions, headers...)
session = requests.Session()

def start():
    urlsite = 'http://150.163.255.234/salvar/mapainterativo/downpluv.php'
    response = session.get(urlsite)
    cities_state = re.findall('\(\"(\w{2})\"\,\"(.*?)\"\,\"(\d+)\"', response.text)
    for cities in cities_state:
        urlcomplete(urlsite, cities[0], cities[1])

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

def urlcomplete(urlsite, state, cities):

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
                print(response.content)
                os.rename('captcha.jpg', cap)
            else:
                print("Deu pau, tente novamente...")
        else:
            print("ops nao foi possivel baixar o captcha, cheque a url ou se algo mudou no site.")
    except requests.exceptions.HTTPError as e:
        print("%s '%s'" % (e, url))

def formating(urlsite, state, c):

    cities = c.replace(" ", "+")
    print(cities)
    base = '?idUF={est}&idCidade={city}&edMes=2&edAno=2017&edNome=Barbara&edEmail=barbara%40lab804.com.br&palavra='
    baseurl = base.format(est=state, city=cities)
    urlpath = urlsite+baseurl
    return urlpath

if __name__ == "__main__":
    print("CTRL+C para sair")
    while True:
        start()
        break
