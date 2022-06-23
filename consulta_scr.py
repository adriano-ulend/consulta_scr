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
    """

    :param token:
    :param cnpj:
    :return:
    """

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


def extract() -> list:
    """
    Open a csv file to extract cnpj data from all clients on system database
    :return: list of all cnpj/uuid to be checked on credit-analysis
    """
    with open(f'{current_path}'+'/source/teste3.csv', 'r', encoding='utf-8') as file:
        sheet = pd.read_csv(file, encoding='utf-8')
        client_source = pd.DataFrame(sheet)

    return client_source


def all_clients(token_prod):

    all_clients_data = []
    all_clients_temp = []

    endpoint_all_clients = f"https://api.ulend.com.br/company/-/loan"

    response_all_clients = requests.get(
        endpoint_all_clients,
        headers={
            "Accept-version": 'v1+',
            "Authorization": f'{token_prod}'
        },
        params={"page": "1", "limit": "500"}
    )
    response_all_clients_json = response_all_clients.json()

    for client in response_all_clients_json['loan']:
        all_clients_temp.append(client['company_cnpj'])
        all_clients_temp.append(client['uuid'])
        all_clients_temp.append(client['company_name'])
        all_clients_data.append(all_clients_temp)
        all_clients_temp = []

    return all_clients_data


if __name__ == '__main__':
    print("SCR CONSULTING\n")


    signin_token = token()
    print(signin_token)

    all_clients(signin_token)
    print('ok')

    # t = extract()
    # print(t)

    cnpj_teste = '06914893000167'   # comercio de pneus anadia ltda
    data_teste = '2021-08'  # 2022-04 a 2021-05
    # id_teste = '62a7a27b4f7b441597ae3fd8'   # id no sistema do cliente

    print(check_scr(signin_token, cnpj_teste, data_teste))

    print(scr_hist(signin_token, cnpj_teste))

    print("\nend\n")

# CHECKLIST:
# 1. verificar como retornar o uuid do cliente para buscar o historico scr no mongo - all_list >> search
#     1.1. response de company/-/loan gera uma lista com info de clients (atende a demanda a ser analisada?)
# 2. testar condicional caso nao tenha historico de consulta scr na analise de credito
#     2.1. se nao tiver faz uma consulta scr dos ultimos 12 meses
# 3. validar response data da request para realizar uma nova consulta scr
# 4. varificar possiveis cenarios de erro (realizar teste com source file_test pelo extract)
# 5. validar output para ser input do parsed_scr
