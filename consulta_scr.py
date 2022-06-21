import pandas as pd
import json
import requests
import os


current_path = os.getcwd()

def token():
    try:
        # api = "https://localhost:8081"
        api = "https://api.ulend.com.br"

        # user = "gabriel@ulend.com.br"
        # password = "teste123"
        user = "report-service@ulend.com.br"
        password = "report"
        r = requests.post(
            f"{api}/auth/email/signin",
            json = {"email": user, "password": password}
        )

        response_json = r.json()
        token = response_json["token"]
    
        return token
    
    except Exception as err:
        return err


def check_scr(cnpj, data_op):

    endpoint_scr = 'https://api.ulend.com.br/partner-bank/scr'

    cnpj = cnpj
    data_base = data_op

    body_json = {
        "base": f"{data_base}", # base no formato ano-mes
        "document": f"{cnpj}"    # cnpj (so int mas como string)
    }

    res = requests.post(
        endpoint_scr, 
        json=body_json, 
        headers = {
            "Authorization": f'{token}'
        }
    )

    res_content = res.content
    res_status = res.status_code

    return res, res_status

def extract():
    with open(f'{current_path}'+'/source/teste3.csv', 'r', encoding='utf-8') as file:
        sheet = pd.read_csv(file, encoding='utf-8')
        client_source = pd.DataFrame(sheet, index=True)

    return client_source


if __name__ == '__main__':
    print("SCR CONSULTING\n")

    token = token()
    print(token)

    cnpj_teste = '57480048000161'
    data_teste = '2021-08'

    print(check_scr(cnpj_teste, data_teste))

    print("\nend\n")
