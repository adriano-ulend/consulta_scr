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
            json={"email": user, "password": password}
        )

        response_json = r.json()
        token = response_json["token"]
    
        return token
    
    except Exception as err:
        return err


def check_scr(token, cnpj, data_op):

    endpoint_scr = 'https://api.ulend.com.br/partner-bank/scr'

    cnpj = cnpj
    data_base = data_op

    body_json = {
        "base": f"{data_base}", # base no formato ano-mes
        "document": f"{cnpj}"    # cnpj (so int mas como string)
    }

    res = requests.get(
        endpoint_scr, 
        params=body_json,
        headers={
            "Authorization": f'{token}'
        }
    )

    res_content = res.json()
    res_status = res.status_code

    return res_status


def scr_hist(token, cnpj):

    endpoint_company_data = f"https://api.ulend.com.br/company"

    response_company = requests.get(
        endpoint_company_data,
        headers={
            "Accept-version": 'v2+',
            "Authorization": f'{token}'
        },
        params={"cnpj": f"{cnpj}"}
    )

    response_company_json = response_company.json()

    cod_cliente = response_company_json['companies'][0]['uuid']
    # cod_cliente = '5aShIs_VEeyDTgJCrBYABA'  # uuid

    endpoint_hist = f"https://api.ulend.com.br/company/{cod_cliente}/credit-analysis-of-company"

    res_hist = requests.get(
        endpoint_hist,
        headers={
            "Authorization": f'{token}'
        }
    )
    res_json = res_hist.json()
    scr_data = res_json['credit_analysis']['scr_historical']

    return scr_data


def extract():
    with open(f'{current_path}'+'/source/teste3.csv', 'r', encoding='utf-8') as file:
        sheet = pd.read_csv(file, encoding='utf-8')
        client_source = pd.DataFrame(sheet)

    return client_source


if __name__ == '__main__':
    print("SCR CONSULTING\n")

    signin_token = token()
    print(signin_token)

    # t = extract()
    # print(t)

    cnpj_teste = '06914893000167'   # comercio de pneus anadia ltda
    data_teste = '2021-08'  # 2022-04 a 2021-05

    print(check_scr(signin_token, cnpj_teste, data_teste))

    print(scr_hist(signin_token, cnpj_teste))

    print("\nend\n")

# CHECKLIST:
# 1. verificar como retornar o uuid do cliente para buscar o historico scr no mongo
# 2. testar condicional caso nao tenha historico de consulta scr no mongo
# 3. validar response data da request para realizar uma nova consulta scr
# 4. varificar possiveis cenarios de erro (realizar teste com source file_test pelo extract)
# 5. validar output para ser input do parsed_scr
