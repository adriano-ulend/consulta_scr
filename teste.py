import csv
import random
import requests

url = "https://www.ulend.com.br/"
r = requests.get(url)
print(r.status_code)

def random_cnpj():

    with open('source/check.csv', 'r', encoding='utf-8') as file:
        sheet = csv.reader(file, delimiter=',')
        list_random = []
        c = 0

        for row in sheet:
            x = random.randint(0, len(row))
            list_random.append(row[x])

        return list_random


if __name__ == '__main__':
    print('TESTE FILE\n')

    c=0
    while c<5:
        print(random_cnpj())
        c+=1
