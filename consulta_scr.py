import pandas as pd
import json


def main():
    with open('/home/adriano/dev/projects/consulta_scr/source/teste2.csv', 'r', encoding='ISO-8859-1') as file:
        sheet = pd.read_csv(file, header=0, sep=',')
        df = pd.DataFrame(sheet)
        df.insert(len(df.columns)-1, 'message.listaDeResumoDasOperacoes', df.pop('message.listaDeResumoDasOperacoes'))
        # ['message.listaDeResumoDasOperacoes']

        df_json = df.pop('message.listaDeResumoDasOperacoes')
        # print(df_json)
        df_teste = df_json[0]

        json1 = json.loads(df_teste)
        print(json1)
        print(type(json1))

        # # routine trough all the rows
        # for row in df_json:
        #     print(row)

        # df2 = pd.DataFrame(pd.json_normalize(df['message.listaDeResumoDasOperacoes']))
        # print(df2)

        # makes a copy of parsed dataframe to another excel file
        # df.to_excel('/home/adriano/dev/projects/Teste/source/parsed.xlsx', index=False)
        # return df    # retornar o dataframe final

if __name__ == '__main__':
    print(main())
