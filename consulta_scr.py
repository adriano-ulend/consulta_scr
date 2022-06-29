import pandas as pd
import json
import requests
import os
import itertools
import datetime


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


def check_scr(session_token, cnpj, data_op):
    """
    Check scr_data when the response from mongoDB is None for a scr analysis in a credit analysis of selected company

    :param session_token:
    :param cnpj:
    :param data_op:
    :return:
    """

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
            "Authorization": f'{session_token}'
        }
    )

    res_status = res.status_code

    return res_status


def scr_hist(session_token, uuid):
    """
    Extract from credit analysis of a company the history (last 12 months) of his scr consulting existed on mongoDB

    :param session_token: token from user report-service@ulend.com.br
    :param uuid: primary key set for company id field (only for company with approval for operating)
    :return: json with scr consulting history (last 12 months)
    """

    endpoint_hist = f"https://api.ulend.com.br/company/{uuid}/credit-analysis-of-company"

    res_hist = requests.get(
        endpoint_hist,
        headers={
            "Authorization": f'{session_token}'
        }
    )
    res_json = res_hist.json()
    scr_data = res_json['credit_analysis']['scr_historical']

    return scr_data


def extract() -> pd.DataFrame:
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

    for client in response_all_clients_json['loans']:
        all_clients_temp.append(client['company_cnpj'])
        all_clients_temp.append(client['company_name'])
        all_clients_data.append(all_clients_temp)
        all_clients_temp = []

    return all_clients_data


def get_client_uuid(token, cnpj):

    endpoint_client_uuid = f"https://api.ulend.com.br/company/-"

    response_all_clients = requests.get(
        endpoint_client_uuid,
        headers={
            "Accept-version": 'v2+',
            "Authorization": f'{token}'
        },
        params={"cnpj": f"{cnpj}"}
    )
    response_client_uuid_json = response_all_clients.json()
    client_uuid = response_client_uuid_json['company']['uuid']

    return client_uuid


def client_scr(token, cnpj) -> list:

    new_scr = []

    for month in range(1, 13):
        if month < 10:
            data_teste = f"2021-0{month}"
            h_scr = check_scr(token, cnpj, data_teste)
            new_scr.append(h_scr)
        else:
            data_teste = f"2021-{month}"
            h_scr = check_scr(token, cnpj, data_teste)
            new_scr.append(h_scr)

    return new_scr


if __name__ == '__main__':
    start = datetime.datetime.now()
    print("SCR CONSULTING\n")

    signin_token = token()
    # print(signin_token)

    data_clients = all_clients(signin_token)
    data_clients.reverse()
    # print(data_clients)
    data_scr = []
    list_scr = []

    # t = extract()
    # print(t)

    # cnpj_teste = '06914893000167'   # comercio de pneus anadia ltda
    # data_teste = '2021-08'  # 2022-04 a 2021-05
    # id_teste = '62a7a27b4f7b441597ae3fd8'   # id no sistema do cliente

    for item in data_clients[:20]:
        """
        5 fresh first companys
        ['07283581000165', 'THEMMA TRANSPORTES E LOGISTICA INTERNACIONAL DE CARGAS LTDA']
        ['07283581000165', 'THEMMA TRANSPORTES E LOGISTICA INTERNACIONAL DE CARGAS LTDA']
        ['07283581000165', 'THEMMA TRANSPORTES E LOGISTICA INTERNACIONAL DE CARGAS LTDA']
        ['73420838000108', 'LEANDRO MARANGONI COMERCIO DE COMBUSTIVEIS LTDA']
        ['15626673000129', 'NORTESUL COMERCIAL AGRICOLA LTDA']
        
        5 oldest companys
        ['16821725000180', 'LAVMIX LAVANDERIA PROFISSIONAL LTDA']
        ['05913922000103', 'WILMER HORTIFRUTIGRANJEIRO LTDA']
        ['28830783000150', 'CUCINA COMERCIAL LTDA']
        ['13671179000150', 'HABITAR IMOVEIS LTDA']
        ['23199116000105', 'SEGURA INTEGRACAO E SOLUCOES EM SEGURANCA ELETRONICA EIRELI']
        
        TOTAL= 500 >> Total liq: 303 - existente: 51, inexistente: 252

        
        """
        if item not in list_scr:
            list_scr.append(item)
    # print(list_scr)
    # cont_existente = 0
    # cont_inexistente = 0
    # list_exist =[]
    # list_inextist = []

    for company in list_scr:
        client_cnpj = company[0]
        client_name = company[1]

        try:
            client_uuid = get_client_uuid(signin_token, client_cnpj)
            historic_scr = scr_hist(signin_token, client_uuid)

            if len(historic_scr) == 0:
                data_scr.append('historic empty - make a new SCR consult')
                # cont_inexistente += 1
                # list_inextist.append(client_cnpj)
            else:
                # data_scr.append("1")
                data_scr.append(historic_scr)
                # print("imported scr hist")
                # cont_existente += 1
                # list_exist.append(client_cnpj)

        except Exception as err:
            # cont_inexistente += 1
            # print("step into except loop")
            hist_scr = client_scr(signin_token, client_cnpj)
            data_scr.append(hist_scr)
            # list_inextist.append(client_cnpj)

    # print(data_scr)
    # print(f"Total liq: {len(list_scr)} - existente: {cont_existente}, inexistente: {cont_inexistente}\n")
    # print(f"Existente: {list_exist}\n")
    # print(f"Inexistente: {list_inextist}")

    print("\nend\n")
    end = f"Exec time: {datetime.datetime.now() - start}"
    print(end)


# CHECKLIST:

# 1. validar formatacao tanto os dados existentes no sistema como os da nova consulta (nova consulta = ano de 2021)
# 3. verificar possiveis cenarios de erro (realizar teste com source file_test pelo extract)
# 4. validar output para ser input do parsed_scr (atualizar parser para receber o novo input)
