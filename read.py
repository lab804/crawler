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
