#!/usr/bin/env python3

import csv
import os

def open_file(filename):

    if os.path.isfile(filename):
        if os.path.getsize(filename) > 0:
            readfile(filename)
        else:
            print("Erro: Arquivo vazio")
    else:
        print("Erro: Arquivo nao existe")



def readfile(filename):

    data = []
    keys = open(filename, "r").readline().strip().split(";")

    with open('2629_SP_2017_2.csv', 'rb') as csvfile:
         for book in csvfile.readlines():
             b = book.strip().replace(b"\t", b"")
             b_as_list = b.split(b";")
             book_dict = {}
             for valor in b_as_list:
                 if valor:
                     book_dict[keys[b_as_list.index(valor)]] = valor
             data.append(book_dict)

    del data[0]
    print(data)


if __name__ == "__main__":
    print("CTRL+C para sair")

    while True:
        open_file('2625_SP_2017_2.csv')
        print("----------------------------------------------------------------------------------------------------------------------")
