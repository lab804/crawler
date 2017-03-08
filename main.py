#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
import requests
import re
import os

class RequestFile(object):

    def __init__(self):
        """Inicializa as variáveis necessárias da classe e a sessao"""
        self.session = requests.Session()
        self.urlsite = 'http://150.163.255.234/salvar/mapainterativo/downpluv.php'

    def start(self):
        """Inicia a captura de dados e o captcha atraves da url"""
        response = self.session.get(self.urlsite)
        cities_state = re.findall('\(\"(\w{2})\"\,\"(.*?)\"\,\"(\d+)\"', response.text)
        for cities in cities_state:
            self.url_complete(self.urlsite, cities[0], cities[1])

    def captcha(self, url):
        """ Realiza download da imagem do captcha"""
        fname = 'captcha.jpg'
        resp = self.session.get(url)
        with open(fname, 'wb') as f:
            try:
                f.write(resp.content)
                return True
            except Exception as e:
                print("Erro ao salvar o captcha: %s" % e)
                return False

    def url_complete(self, urlsite, state, cities):
        """ Completa a url com estado, cidade e o código do captcha.
        Verifica o status code da requisição da página; Caso tenha sucesso,
        salva imagem do captcha com o seu código de nome na pasta '/cap' """
        urlimagem = 'http://150.163.255.234/salvar/mapainterativo/securimage/securimage_show.php'
        path = self.formatting(urlsite, state, cities)
        print(path)
        try:
            iscaptcha = self.captcha(urlimagem)
            if iscaptcha:
                cap = input("Me fale as letras senhorita? ")
                finalurl = path+cap
                response = self.session.get(finalurl)
                if response.status_code == 200:
                    print(response.content)
                    self.write_file(cap)
                    namecap = 'cap/'+cap+'.jpg'
                    os.rename('captcha.jpg', namecap)
                else:
                    print("Deu pau, tente novamente...")
            else:
                print("Ops nao foi possivel baixar o captcha, cheque a url ou se algo mudou no site.")
        except requests.exceptions.HTTPError as e:
            print("%s '%s'" % (e, url))

    @staticmethod
    def formatting(urlsite, state, c):
        """Formada path com os dados de cidade e estado de acordo com a lista gerado por Start()"""
        cities = c.replace(" ", "+")
        print(cities)
        base = '?idUF={est}&idCidade={city}&edMes=2&edAno=2017&edNome=Barbara&edEmail=scraping.camaden%40gmail.com&palavra='
        baseurl = base.format(est=state, city=cities)
        urlpath = urlsite+baseurl
        return urlpath

    @staticmethod
    def write_file(cap_code):
        """Salva os codigos dos captchas ao final do arquivo captcha.csv"""
        try:
            arq = open('captcha.csv','a+')
            arq.writelines(cap_code+'\n')
            print("Registro gravado com sucesso")
        except IOError:
            print("Erro ao abrir o arquivo!")

if __name__ == "__main__":
    print("CTRL+C para sair")

    while True:
        init = RequestFile()
        init.start()
