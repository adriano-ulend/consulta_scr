import csv
import json
import pandas as pd


def main():
    with open('/home/adriano/dev/projects/consulta_scr/source/teste2.csv', 'r', encoding='utf-8') as file:
        sheet = csv.reader(file, delimiter=',')

        # column_names_source = [
        #     _id, - 0
        #     createdAt, - 1
        #     message.cnpjDaIFSolicitante, - 3
        #     message.codigoDoCliente, - 4
        #     message.dataBaseConsultada, - 7
        #     message.listaDeResumoDasOperacoes - 10
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
            #    line 0 = headers
            if e == 0:
                header = [line[0], line[1], line[3], line[4], line[7], 'modalidade', 'cod-val']
                data_header.append(header)
            else:
                json_line = json.loads(line[10])
                # print('num de objetos do json: ', len(json_line))
                # print(json_line)
                # print(type(json_line))  # list

                for item in json_line:
                    # print(f'item: {item}')
                    # print(f'type: {type(item)}')
                    # list_temp = []
                    modalidade = item['modalidade']

                    for data_venc in item['listaDeVencimentos']:
                        vencimento_temp = ''
                        vencimento_temp = f"{data_venc['codigoVencimento']}-{data_venc['valorVencimento']}"
                        # print(vencimento_temp)

                        selected_params = [line[0], line[1], line[3], line[4], line[7], modalidade, vencimento_temp]
                        data_list.append(selected_params)

        table = pd.DataFrame(data_list, columns=data_header)
        df_cod_val = table.pop('cod-val')
        df_vencimentos = pd.DataFrame(columns=column_names_parsed)

        for index, val in df_cod_val.iterrows():
            # print(index, type(index))
            # print(val, type(val))
            d1 = val.str.split('-')
            print(str(d1[0]), " >> ", str(d1[1]))

        # verificar como trazer os valores separados de codVencimento e valorVencimento (em d1) gerados no df_cod_val
        # ver como adicionar o valor vencimento a coluna codVencimento do df_vencimento


if __name__ == '__main__':
    print(main())
