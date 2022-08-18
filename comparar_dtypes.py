import pandas as pd
import re

# importar as duas tabelas
df_dtypes_databricks = pd.read_csv("mock_data_dtypes_databricks.csv")
df_dtypes_sas = pd.read_csv("sas_proc_content_mock.csv", sep=';', header=1, usecols=[1,2,3,4,5])

def testar_tipos(df_dtypes_databricks, df_dtypes_sas):
    status_approved = True  # Flag que irá mudar no final do teste para ver se o teste foi aprovado ou não.

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
                    if 'datetime' in tipo_variavel_databricks.lower():
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
                    if 'date' in tipo_variavel_databricks.lower():
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\nResultado: OK\n")
                    else:
                        status_approved = False
                        print(
                            f"Variável {cada_variavel}\nTipo SAS:{tipo_variavel_sas}\nTamanho do campo:{type_length}\n"
                            f"FORMAT: {type_format}\nTipo Databricks: {tipo_variavel_databricks}\n"
                            f"Resultado Esperado: date ou datetime\n")
                elif 'word' in type_format.lower():
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
    else:
        print("Resultado do teste: REPROVADO")

testar_tipos(df_dtypes_databricks, df_dtypes_sas)