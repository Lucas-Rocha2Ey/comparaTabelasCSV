import os
import sys
from datetime import datetime
import pandas as pd

"""
DIRETORIO_ATUAL = os.getcwd()
ARQUIVO_TEMPLATE = DIRETORIO_ATUAL + '\\df_train.csv'

print(ARQUIVO_TEMPLATE.split('\\'))
print(ARQUIVO_TEMPLATE.split('\\')[-1])
"""

"""
input_colunas = input("Insira o nome das colunas que são do tipo Data (separado por espaço)\n")
lista_colunas = input_colunas.split()
print(lista_colunas.__str__())
input_arquivos = input("Insira o nome das duas tabelas a comparar\n")
arquivo_original = input_arquivos.split()[0]
arquivo_convertido = input_arquivos.split()[1]
print(arquivo_original)
print(arquivo_convertido)
"""

"""
colunas_datas = ['DTEMIS', 'DTINICIO']
colunas = ['DTEMIS', 'DTINICIO', 'NOME', 'IDADE', 'SEXO', 'SALBRUTO']

if set(colunas).intersection(set(colunas_datas)) == set(colunas_datas):
    print('As colunas informadas existem na tabela')
else:
    print('Há colunas informadas que nao existem na tabela')
"""
"""
col_data_original = ['10/04/2008', '11/04/2008', '12/04/2008', '13/04/2008', '14/04/2008']
# col_data_convertido = ['10/04/2008', '11/04/2008', '12/04/2008', '13/04/2008', '14/04/2008'] # Fluxo normal
format_sas = 'DDMMYY10'
# col_data_convertido = ['10/04/2008', '11/04/2008', '12/04/2008', '13/04/2008', '15/04/2008'] # entra no if interno
col_data_convertido = ['2008-04-10', '2008-04-11', '2008-04-12', '2008-04-13', '2008-04-14'] # entra no Except
"""

"""
passou_teste = True

# Achar o formato de data em SAS equivalente em Datetime String
df_formatos_datas = pd.read_excel('Formato Datas.xlsx')
formato_equiv_databricks = \
    df_formatos_datas.loc[df_formatos_datas["FORMAT DATE SAS"] == format_sas, "FORMAT DATE DATABRICKS"].values[0]

for cada_data_original, cada_data_convertida in zip(col_data_original, col_data_convertido):
    try:
        # Desse formato, devo criar um objeto Datetime a partir da informação desse valor do relatório em SAS
        dt = datetime.strptime(cada_data_original, formato_equiv_databricks)
        dt_2 = datetime.strptime(cada_data_convertida, formato_equiv_databricks)
        if dt != dt_2:
            print(f"As datas {cada_data_original} e {cada_data_convertida} na coluna "
                  f"TESTE são diferentes")
            passou_teste = False
            print("Teste Reprovado")
            break
    except ValueError:
        print("Formato da data no relatório do Databricks não é o mesmo formato de data do relatório do SAS")
        print(f"Formato de data esperado no Databricks: {formato_equiv_databricks}")
        print(f"Formato de data obtido no Databricks: {cada_data_convertida}")
        passou_teste = False
        print("Teste Reprovado")
        break

if passou_teste:
    print("As datas possuem o mesmo formato")
    print("Teste aprovado")
"""
"""
coluna_2 = ['TESTE1', 'TESTE2', 'TESTE3', 'TESTE4', 'TESTE5']
coluna_3 = [14,15,67,34,41]

# Para testar o periodo do relatório, primeiro devo converter todas as colunas que eu informei para Datetime
# Depois comparar o valor minimo e máximo com os valores de entrada do relatório.
# O teste está aprovado sob duas condições: 1 - O periodo minimo do registro da coluna seja maior ou igual o periodo
# minimo informado pelo usuário e 2 - O periodo final do registro seja menor ou igual ao periodo final informado pelo
# usuário.
# Ex: Informo para testar registros entre 01/07/2022 - 31/07/2022. Se o periodo minimo encontrado no registo for
# a partir de 01/07 e o periodo final encontrado no registro for até 31/07 ou data anterior, o teste é aprovado.

periodo = input("Insira o periodo final e final do relatório (em formato DD/MM/YYYY)\n")
periodo_inicial = datetime.strptime(periodo.split()[0], "%d/%m/%Y")
periodo_final = datetime.strptime(periodo.split()[1], "%d/%m/%Y")

df_teste = pd.DataFrame({'DTEMIS': col_data_original, 'NOME': coluna_2, 'IDADE': coluna_3})
df_teste['DTEMIS'] = pd.to_datetime(df_teste['DTEMIS'], format="%d/%m/%Y")
periodo_min = df_teste['DTEMIS'].min()
periodo_max = df_teste['DTEMIS'].max()
print(df_teste.head())

condicao1 = periodo_inicial <= periodo_min
condicao2 = periodo_final >= periodo_max

if condicao1 and condicao2:
    print("Teste aprovado")
"""

"""
dictTestes = {1: "teste1()", 2:"teste2()", 3:"teste3()", 4:"teste4()",
              5: "teste5()", 6:"teste6()"}

df = pd.DataFrame({'Cod': [1,2,3,4,5,6,7],
                   'Teste': ["Teste de Extensão",
                             "Teste de Quantidade de Linhas",
                             "Teste de Quantidade de Colunas",
                             "Teste de Conteúdo das Colunas",
                             "Conteudo das Linhas",
                             "Conteudo das Linhas (em ordem)",
                             "Todos"]})
df.set_index('Cod', inplace=True)

print(df)
print(dictTestes)
input_testes = input("Digite o(s) código(s) dos testes que deseja executar, separado por espaço (Ex:1 3 4)\n")
lista_testes = input_testes.split()
for cadaCodigo in lista_testes:
    print(dictTestes.get(int(cadaCodigo)))
"""

"""
import unicodedata

colunas_sas = ["Coluna Teste", "Exposure Morte", "Exposure por Intern. H30", "id_pol", "açúcar"]
colunas_databricks = ["Coluna_Teste", "Exposure_Morte", "Exposure_por_Intern_H30", "ip_pol", "acucar"]
colunas_sas_transf = []

for cada_colunas_sas in colunas_sas:
    new_column = cada_colunas_sas.replace('. ', '_')
    new_column = cada_colunas_sas.replace('.', '_')
    new_column = cada_colunas_sas.replace(' ', '_')
    new_column = ''.join(ch for ch in unicodedata.normalize('NFKD', new_column) if not unicodedata.combining(ch))
    colunas_sas_transf.append(new_column)

for cada_coluna_sas_original, cada_coluna_sas_tratada in zip(colunas_sas, colunas_sas_transf):
    if cada_coluna_sas_original != cada_coluna_sas_tratada:
        print("Colunas foram apenas tratadas")
        break

print(colunas_sas_transf)
print(colunas_databricks)
"""
dados = [[1, 'Lucas', 19],[2, 'João', 18], [3, 'Melissa', 16]]
dados_2 = [[1, 'Lucas', 19.0], [2, 'João', ], [3, 'Melissa', 16]]

import pandas as pd
df_1 = pd.DataFrame(dados)
df_2 = pd.DataFrame(dados_2)

print(df_2.isin(df_1))

print("=======")

for columns in df_2.columns:
    print(f"Coluna {columns}:\n {df_2[columns].isin(df_1[columns]).value_counts()}\n")

print(df_2[2].isin(df_1[2]))



