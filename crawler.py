#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import os

# sessao global
session = requests.Session()

def acessa_site(url):
    """acessa o site para gerar a sessao"""
    req = session.get(url, timeout=10)
    if req.status_code != 200:
        print("Erro na conexao")
        return None
    else:
        return req.content

def organiza_dados(content, base_url):
    cities_state = re.findall('\(\"(\w{2})\"\,\"(.*?)\"\,\"(\d+)\"', content)
    return cities_state

def formata_url_path(base_url, state, c):
    cities = c.replace(" ", "+")
    print(state)
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
        print(response.content)
        return True
    else:
        print("Deu pau, tente novamente...")
        return False

def salva_captcha_bd(cap_code):
    """Salva os codigos dos captchas ao final do arquivo captcha.csv"""
    try:
        arq = open('captcha.csv','a+')
        arq.writelines(cap_code+'\n')
        print("Registro gravado com sucesso")
    except IOError:
        print("Erro ao abrir o arquivo!")

def salva_captcha_img(cap_code):
        namecap = 'cap/'+cap_code+'.jpg'
        os.rename('captcha.jpg', namecap)
        print("Arquivo salvo com sucesso")

def ler_email(email, senha):
    """ler os emails para capturar os que links que possuem
    o dowload do arquivo csv"""
    pass

def download_arquivo(url):
    """realiza o download do arquivo que contem
    os dados metereologicos daquela estacao"""
    pass

def ler_arquivo(content):
    """le o arquivo e checa se tem conteudo"""
    pass

def parsea_dados(content):
    """limpamos os dados e estruturamos de uma forma
    que se encaixe no banco de dados"""
    pass

def ultima_data():
    """retorna dicionario com o ultimo documento inserido
    no banco de dados"""
    pass

def inserir_dados(documento):
    """insere o documento no banco de dados"""
    pass

def main():
    """funcao principal"""
    base_url = "http://150.163.255.234/salvar/mapainterativo/downpluv.php"
    url_img = 'http://150.163.255.234/salvar/mapainterativo/securimage/securimage_show.php'
    content = acessa_site(base_url)
    if not content:
        return
    else:
        cities = organiza_dados(content, base_url)
        for city in cities:
            url_format = formata_url_path(base_url, city[0], city[1])
            try:
                iscaptcha = captura_captcha(url_img)
                if iscaptcha:
                    cap = raw_input("Me fale as letras senhorita? ")
                    url_final = url_format+cap
                    print(url_final)
                    isget = preenche_formulario(url_final)
                    if isget:
                        salva_captcha_img(cap)
                        salva_captcha_bd(cap)
                else:
                    print("Ops! nao foi possivel baixar o captcha, cheque a url ou se algo mudou no site.")
            except requests.exceptions.HTTPError as e:
                print("%s '%s'" % (e, url))

if __name__ == "__main__":
    main()
