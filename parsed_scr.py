import csv
import json
import pandas as pd


def main():
    """
    Read a .CSV file and extract all data from specific columns into a DataFrame and parsing data from column
    'message.listaDeResumoDasOperacoes' as a json and creating another Dataframe through iterable method

    :return: Two Dataframe joined into one showing a table with all data (codigoVencimento e valorVencimento for each
    'modalidade' for each CNPJ from the file source
    """

    with open('/home/adriano/dev/projects/consulta_scr/source/teste2.csv', 'r', encoding='utf-8') as file:
        # teste.csv = file original / teste2.csv = test file
        sheet = csv.reader(file, delimiter=',')

        # column_names_original = [
        #     '_id', index 0
        #     'createdAt', index 1
        #     'message.codigoDoCliente', index 4
        #     'message.dataBaseConsultada', index 7
        #     'dict_mod_CodigoValor'
        # ]

        column_names_parsed = [
            'modalidade',
            'v20',
            'v40',
            'v60',
            'v80',
            'v110',
            'v120',
            'v130',
            'v140',
            'v150',
            'v160',
            'v165',
            'v170',
            'v175',
            'v180',
            'v190',
            'v199',
            'v205',
            'v210',
            'v220',
            'v230',
            'v240',
            'v245',
            'v250',
            'v255',
            'v260',
            'v270',
            'v280',
            'v290',
            'v310',
            'v320',
            'v330'
        ]

        data_list = []
        data_header = []
        for e, line in enumerate(sheet):
            #    line [0] = headers - line[1+n] = data

            if e == 0:
                # header = column_names_source
                header = [line[0], line[1], line[4], line[7], 'dict_mod_CodigoValor']
                data_header.append(header)

            else:
                # check if have data to be parsed (if not skip the line)
                if line[10] == "":
                    print(f'{line[0]} on line {e} does not have any SCR data on the record')
                else:
                    json_line = json.loads(line[10])

                    for item in json_line:
                        modalidade = item['modalidade']

                        vencimento_temp = {}
                        mod_venc_temp = {}
                        for data_venc in item['listaDeVencimentos']:
                            vencimento_temp[f"{data_venc['codigoVencimento']}"] = f"{data_venc['valorVencimento']}"

                            mod_venc_temp[f"{modalidade}"] = vencimento_temp

                        selected_params = [line[0], line[1], line[4], line[7], mod_venc_temp]
                        data_list.append(selected_params)

        table = pd.DataFrame(data_list, columns=data_header)

        # separate data and parse that into a table (with new columns)
        df_cod_val = table.pop('dict_mod_CodigoValor')
        dict_cod_val = df_cod_val.to_dict(orient='list')
        df_vencimentos = pd.DataFrame(columns=column_names_parsed)

        for dict_item in dict_cod_val.values():
            for dict_value in dict_item:
                for cod_v, val_v in dict_value.items():
                    df_vencimentos.loc[df_vencimentos.shape[0], 'modalidade'] = cod_v

                    for venc_cod, vencim_valor in val_v.items():
                        df_vencimentos.loc[df_vencimentos.shape[0] - 1, f"{venc_cod}"] = vencim_valor

        df_vencimentos = df_vencimentos.fillna(0)

        # merge the first table with the second (json parsed into a table) to create the final dataframe
        table_parsed = pd.merge(table, df_vencimentos, how='left', left_index=True, right_index=True)

        # makes a copy of final dataframe to another excel file (.csv format)
        table_parsed.to_csv('/home/adriano/dev/projects/consulta_scr/source/parsed_scr.csv', index=False)

        return "consulta_scr gerado"


if __name__ == '__main__':
    main()

# Alinhamento 21-06:
# 1. endpoint no sistema que verifica se existe historico de dados no BD da Ulend (se existir busca no BD, senao realiza a nova consulta SCR)
    # utilizar a data_base como o mes/ano de operação na Ulend (default: periodo de 12 meses de historico)
# 2. verificar o dados do body para realizar a request para o endpoint (response demora uns 5sec - webhook da Parati >> salva no Mongo)
