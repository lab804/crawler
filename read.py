#!/usr/bin/env python3

import csv
import os

def open_file(filename):
    """Responsavel por abrir o arquivo e verificar se o arquivo existe. Caso exista, verifica se nao esta vazio"""
    if os.path.isfile(filename):
        if os.path.getsize(filename) > 0:
            read_file(filename)
        else:
            print("Erro: Arquivo vazio")
    else:
        print("Erro: Arquivo nao existe")



def read_file(filename):
    """Responsavel por realizar a leitura dos dados no arquivo. Verifica se esta corrompido ou caso esteja faltando dados"""
    data = []
    keys = open(filename, "r").readline().strip().split(";")
    if keys[0] == 'municipio':
        with open('2629_SP_2017_2.csv', 'rb') as csvfile:
             for book in csvfile.readlines():
                 if book:
                     print("Arquivo nao contem dados")
                 else:
                     b = book.strip().replace(b"\t", b"")
                     b_as_list = b.split(b";")
                     book_dict = {}
                     for valor in b_as_list:
                         if valor:
                             book_dict[keys[b_as_list.index(valor)]] = valor
                     data.append(book_dict)
             del data[0]
             print(data)
    else:
        print("Arquivo corrompido ou já baixado")


if __name__ == "__main__":
    print("CTRL+C para sair")

    filename = '2629_SP_2017_2.csv'

    open_file(filename)
