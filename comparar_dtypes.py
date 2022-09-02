import re
import sys
import os
import time
import escrevendo_planilha_excel as epe

import pandas as pd
from datetime import datetime

DIRETORIO_ATUAL = os.getcwd()
ARQUIVO_TEMPLATE = DIRETORIO_ATUAL + '\\Template - Relatório de teste.xlsx'
DIRETORIO_DESTINO = DIRETORIO_ATUAL + '\\Relatório de teste.xlsx'

def carregarExcel():
    try:
        file_exists = epe.does_file_exist(ARQUIVO_TEMPLATE)
        if file_exists:
            ##### Verificar se o arquivo relatório de teste já existe
            file_template_exists = epe.does_file_exist(DIRETORIO_DESTINO)
            ###### Se ele não existe, faça a cópia do arquivo template e crie um novo relatório de teste
            if not file_template_exists:
                ##### Copia o arquivo para poder escrever
                new_file = epe.copy_file(ARQUIVO_TEMPLATE)
                ##### Abre o arquivo excel
                excel = epe.load_excel_file(new_file)
            else:
                ##### Abre o arquivo excel
                excel = epe.load_excel_file(DIRETORIO_DESTINO)
                ##### Verificar se os campos dos testes do Tipo de Colunas já está preenchido.
                ###### Se tiver preenchido, apagar os campos e informar o usuário para executar comparar_dtypes.py após
                ###### a execução do CompararSaidaBasico.py. Aqui terá que atualizar o C15 para a faixa das colunas dos
                ###### testes
                for i in [15,16,18]:
                    if epe.read_cell_excel(excel, 'Sheet1', f'C{i}') is not None:
                        epe.write_cell_excel(excel, 'Sheet1', f'C{i}', None)
                        epe.write_cell_excel(excel, 'Sheet1', f'D{i}', None)
                        epe.write_cell_excel(excel, 'Sheet1', f'E{i}', None)
                        epe.write_cell_excel(excel, 'Sheet1', f'F{i}', None)
            return excel
        else:
            sys.stdout = sys.__stdout__  # Este comando volta a imprimir no console
            sys.stdout.write("Não é possível escrever o relatório no Excel!")
            time.sleep(2)
            sys.exit(1)
    except PermissionError:
        print("Não é possível carregar o arquivo. Feche todas as planilhas do excel e tente novamente")
        sys.exit(1)


ARQUIVO_EXCEL = carregarExcel()


# importar as duas tabelas
df_dtypes_databricks = pd.read_csv("mock_data_dtypes_databricks.csv")
df_dtypes_sas = pd.read_csv("sas_proc_content_mock.csv", sep=',', header=1)

def testar_tipos(df_dtypes_databricks, df_dtypes_sas):
    status_approved = True  # Flag que irá mudar no final do teste para ver se o teste foi aprovado ou não.

    print(df_dtypes_sas)

    for cada_variavel in df_dtypes_sas['Variable'].values:
        try:
            tipo_variavel_sas = df_dtypes_sas.query(f"Variable == '{cada_variavel}'")['Type'].values[0]
            type_length = int(df_dtypes_sas.query(f"Variable == '{cada_variavel}'")['Len'].values[0])
            tipo_variavel_databricks = df_dtypes_databricks.query(f"columns == '{cada_variavel}'")['dtype'].values[0]
        except ValueError as value_error:
            status_approved = False
            if value_error.args[0] == 'cannot convert float NaN to integer':
                print("Existe pelo menos um campo da coluna 'Len' vazia na tabela proc_contents no SAS.\n"
                      "Abortando teste...")
                epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F15', 'ABORTADO')
                break

        if 'char' in tipo_variavel_sas.lower():
            if type_length == 1:
                # Pesquisar se a equivalente a Char:
                if 'char' in tipo_variavel_databricks.lower():
                    print(f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                          f"Tipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                else:
                    status_approved = False
                    print(f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                    f"Tipo Databricks: {tipo_variavel_databricks}\nResultado Esperado: char\n")
            else:
                # Pesquisar se a equivalente a String:
                if 'string' in tipo_variavel_databricks.lower():
                    print(f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                          f"Tipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                else:
                    status_approved = False
                    print(f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                          f"Tipo Databricks: {tipo_variavel_databricks}\nResultado Esperado: string\n")
        if 'num' in tipo_variavel_sas.lower():
            if type_length == 1:
                # Pesquisar se a equivalente a Int:
                if 'int' in tipo_variavel_databricks.lower():
                    print(f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                          f"Tipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                else:
                    status_approved = False
                    print(f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                          f"Tipo Databricks: {tipo_variavel_databricks}\nResultado Esperado: int\n")
            else:
                # Tenho que verificar se o campo format está Nulo ou se tem um formato específico (YYYYMMDD/DATE/etc.)
                type_format = df_dtypes_sas.query(f"Variable == '{cada_variavel}'")['Format'].values[0]
                if 'best' in type_format.lower():
                    if type_format.split('.')[1] != '':
                        if int(type_format.split('.')[1]) > 0:
                            if ('float' in tipo_variavel_databricks.lower()) or ('double' in tipo_variavel_databricks.lower()):
                                print(
                                    f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                    f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                            else:
                                status_approved = False
                                print(
                                    f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                    f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                                    f"Resultado Esperado: float ou double\n")
                    else:
                        if 'int' in tipo_variavel_databricks.lower():
                            print(
                                f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                        else:
                            status_approved = False
                            print(
                                f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                                f"Resultado Esperado: int\n")
                elif 'comma' in type_format.lower():
                    if int(type_format.split('.')[1]) > 0:
                        if ('float' in tipo_variavel_databricks.lower()) or ('double' in tipo_variavel_databricks.lower()):
                            print(
                                f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                        else:
                            status_approved = False
                            print(
                                f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                                f"Resultado Esperado: float ou double\n")
                    else:
                        if 'int' in tipo_variavel_databricks.lower():
                            print(
                                f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                        else:
                            status_approved = False
                            print(
                                f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                                f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                                f"Resultado Esperado: int\n")
                elif (re.match(r"^DATET.*", type_format)) or (re.match(r".*TIME.*", type_format)):
                    # checa se é o tipo datetime
                    if 'datetime' or 'string' in tipo_variavel_databricks.lower():
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                    else:
                        status_approved = False
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                            f"Resultado Esperado: datetime\n")
                elif (re.match(r".*DATE.*", type_format)) or (re.match(r"^[DMY]{2}.*", type_format)):
                    # checa se é tipo date
                    if 'date' or 'string' in tipo_variavel_databricks.lower():
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                    else:
                        status_approved = False
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                            f"Resultado Esperado: date ou datetime\n")
                elif ('word' in type_format.lower()) or ('negparen' in type_format.lower()):
                    # tipo negparenw.d no sas => -12345 = (12345)
                    # Numero negativo é representado em parenteses.
                    # tipo wordw.d no sas => 7 = SEVEN
                    # Numeros são escritos por extenso.
                    if 'string' in tipo_variavel_databricks.lower():
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                    else:
                        status_approved = False
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                            f"Resultado Esperado: string\n")
                else:
                    # caso seja NUM, tamanho do campo > 1 e não tiver estabelecido um formato específico -> float,double
                    if ('float' in tipo_variavel_databricks.lower()) or ('double' in tipo_variavel_databricks.lower()):
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"Tipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                    else:
                        status_approved = False
                        print(
                        f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                        f"Tipo Databricks: {tipo_variavel_databricks}\nResultado Esperado: float ou double\n")

    if status_approved:
        print("Resultado do teste: APROVADO")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D15', 'OK')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E15', 'Todos os campos equivalentes')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F15', 'APROVADO')
    else:
        print("Resultado do teste: REPROVADO")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D15', 'OK')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E15', 'Há campos não equivalentes')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F15', 'REPROVADO')


char = input("Aperte enter se já inseriu o tipo dos formatos originais do SAS no arquivo 'sas_proc_content_mock.csv'")
char = input("Aperte enter se já inseriu o tipo dos formatos originais do Databricks no arquivo"
             "'mock_data_dtypes_databricks.csv'")

inicio = datetime.now()
print("Iniciando teste de Tipo de Colunas...\n")
testar_tipos(df_dtypes_databricks, df_dtypes_sas)
fim = datetime.now() - inicio
print(f"Teste concluido em {round(fim.total_seconds(), 2)} segundos ")

char = input("Deseja imprimir o relatório? [digite Y para 'sim'] ")
if char.lower() == 'y':
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C15', inicio)
    sys.stdout = open('Relatório Final do Teste de Tipo de Colunas.txt', 'w')
    print("Teste: Tipo de Colunas\n")
    print(f"Data de Execução: {inicio.strftime('%d/%m/%Y %H:%M')}\n")
    testar_tipos(df_dtypes_databricks, df_dtypes_sas)
    print(f"Teste concluido em {round(fim.total_seconds(), 2)} segundos ")
    sys.stdout = sys.__stdout__   # Este comando volta a imprimir no console
    epe.save_excel_file(ARQUIVO_EXCEL, DIRETORIO_DESTINO)
    sys.stdout.write("Relatório imprimido com sucesso!")
    time.sleep(2)
    sys.stdout.close()
else:
    print("O script será fechado em 2 segundos...")
    time.sleep(2)






