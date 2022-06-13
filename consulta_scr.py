import pandas as pd
import json


def main():
    with open('/home/adriano/dev/projects/consulta_scr/source/teste2.csv', 'r', encoding='utf-8') as file:
        sheet = pd.read_csv(file)
        df = pd.DataFrame(sheet)
        # df.insert(len(df.columns)-1, 'message.listaDeResumoDasOperacoes', df.pop('message.listaDeResumoDasOperacoes'))
        data_parsed = []

        # column_names_source = [
        #     _id,
        #     message.cnpjDaIFSolicitante,
        #     message.codigoDoCliente,
        #     message.dataBaseConsultada,
        #     message.listaDeResumoDasOperacoes
        # 'cnpjCliente',
        # 'dataConsulta',
        # 'dataBase',
        # 'codigoModalidade',
        # ]

        column_names_parsed = [
            '_id',
            'message.cnpjDaIFSolicitante',
            'createdAt',
            'message.dataBaseConsultada',
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
        df_parsed = pd.DataFrame(columns=column_names_parsed)




        # for row in df.iterrows():
        #     for col, item in row[1].items():
        #         data_dict = {}
        #         data_dict['_id'] = item

        # print(df_parsed)
        # id_parsed = df['_id']
        # print(id_parsed)

        # for row, item in df_parsed['_id'].iteritems():
        #     print(row, type(row))
        #     print(item, type(item))

        #     # extrair a coluna com o json e atribuir a outro dataframe
        #     df_json = pd.DataFrame.pop(row['message.listaDeResumoDasOperacoes'])
        #     df_teste = df_json
        #
        #     # coluna do json passando os dados pra list
        #     json1 = json.loads(df_teste)
        #     print('num de objetos do json: ', len(json1))
        #     # print(json1)
        #     # print(type(json1))  # list
        #
        # # routine trough all the rows
        # for row in json1:
        #     print(len(row))
        #     # print(row)
        #
        # df_parsed['cnpjCliente'] = df['message.cnpjDaIFSolicitante']
        # df_parsed['dataConsulta'] = df['createdAt']
        # df_parsed['dataBase'] = df['message.dataBaseConsultada']
        # print(df_parsed)

        # df2 = pd.DataFrame(pd.json_normalize(df['message.listaDeResumoDasOperacoes']))
        # print(df2)

        # makes a copy of parsed dataframe to another excel file
        # df.to_excel('/home/adriano/dev/projects/Teste/source/parsed.xlsx', index=False)
        # return df    # retornar o dataframe final

if __name__ == '__main__':
    print(main())
