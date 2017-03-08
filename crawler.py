#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

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


def preenche_formulario(formulario):
    """preenche formulario para receber o email"""
    pass

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
    content = acessa_site(base_url)
    if not content:
        return
    print(content)

if __name__ == "__main__":
    main()
