#!/usr/bin/env python3

import csv

data = []

keys = open("2629_SP_2017_2.csv", "r").readline().strip().split(";")

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


    site = 'http://150.163.255.234/salvar/mapainterativo/downpluv.php'
    basename = '?idUF=SP&idCidade=ITAPETININGA&edMes=2&edAno=2017&edNome=Barbara&edEmail=barbara%40lab804.com.br&palavra='
    url = site + basename
