#!/usr/bin/env python3

import csv
import os

class ReadFile(object):

    def __init__(self, filename, city=None, state=None, date_hour=None):
        """Inicializa as variáveis recebidas como parametros"""
        self.filename = filename
        self.city = city
        self.state = state
        self.date_hour = date_hour

        def __exit__(self):
            self.filename.close()

    def start_file(self):
        """Inicia o arquivo a ser lido: verifica se existe, se esta vazio.
        Caso exista e não esteja vazio, a arquivo sera aberto e lido"""
        if os.path.isfile(self.filename):
            if os.path.getsize(self.filename) > 0:
                self.open_file()
            else:
                print("Erro: Arquivo vazio")
        else:
            print("Erro: Arquivo nao existe")

    def read_full_file(self, keys):
        """Responsavel por realizar a leitura dos dados no arquivo baixado.
        Além disso, cria um dicionário com todos dados colhidos
        e os encaminha para o banco de dados"""
        data_file = []
        with open(self.filename, 'rb') as csvfile:
            for line in csvfile.readlines():
                b = line.strip().replace(b"\t", b"")
                b_as_list = b.split(b";")
                dic = {}
                for data in b_as_list:
                    if data:
                        dic[keys[b_as_list.index(data)]] = data
                data_file.append(dic)
        if len(data_file) < 2:
            print ("Arquivo nao contem dados. Verifique se ha dados no site!")
        else:
            del data_file[0]
            print(data_file)

    def open_file(self):
        """Responsável por abrir e verificar o arquivo. Dentre as
        verificações, estão:
        Caso o arquivo não comece com 'municipio' em sua primeiro linha
        (padrão dos arquivos), emite um alerta notificando que o download
        deste mesmo arquivo ja foi realizado.
        Caso o arquivo esteja correto, Inicia a leitura do mesmo."""
        keys = open(filename, "r").readline().strip().split(";" or "\n")
        if keys[0] == 'municipio':
            if self.date_hour==None:
                self.read_full_file(keys)
            else:
                self.read_file(keys)
        else:
            print("Download já foi realizado")


if __name__ == "__main__":
    print("CTRL+C para sair")

    filename = '2629_SP_2017_2.csv'
    city = "Moji mirim"
    state = "sp"
    # date_hour = "2017-02-01 22:10:00"

    file = ReadFile(filename, city, state, date_hour=None)
    file.start_file()
