import requests

# armazenamos a sessao da requisicao (cookies, sessions, headers...)
session = requests.Session()

def captcha(url, fname):
    """ download captcha """
    resp = session.get(url)
    with open(fname, 'wb') as f:
        try:
            f.write(resp.content)
            return True
        except Exception as e:
            print("erro ao salvar o captcha: %s" % e)
            return False

def main():
    """ funcao principal """
    urlsite = 'http://150.163.255.234/salvar/mapainterativo/downpluv.php'
    path = urlsite+'?idUF=SP&idCidade=ITAPETININGA&edMes=2&edAno=2017&edNome=Barbara&edEmail=barbara%40lab804.com.br&palavra={palavra}'
    urlimagem = 'http://150.163.255.234/salvar/mapainterativo/securimage/securimage_show.php'
    fname = 'qtest.jpg'
    try:
        iscaptcha = captcha(urlimagem, fname)
        if iscaptcha:
            palavra = input("Me fale as letras senhorita? ")
            finalurl = path.format(palavra=palavra)
            response = session.get(finalurl)
            if response.status_code == 200:
                print(response.content)
            else:
                print("Deu pau, tente novamente...")
        else:
            print("ops nao foi possivel baixar o captcha, cheque a url ou se algo mudou no site.")
    except requests.exceptions.HTTPError as e:
        print("%s '%s'" % (e, url))

if __name__ == "__main__":
    print("CTRL+C para sair")
    while True:
        main()
