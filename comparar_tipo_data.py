import os
import time
import sys
from datetime import datetime
import pandas as pd
import escrevendo_planilha_excel as epe


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
                for i in [16,18]:
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

def testeExistenciaArquivos(arquivo_original, arquivo_pos_conversao):
    """
    O objetivo do teste é verificar se inseri dois arquivos que existem no diretório no qual estou rodando o teste
    :param arquivo_original: Caminho do arquivo no formato original
    :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
    :return: True se ambos os arquivos existem e False se pelo menos um arquivo foi inserido
    """
    if os.path.exists(arquivo_original) and os.path.exists(arquivo_pos_conversao):
        return True
    elif not(os.path.exists(arquivo_original)) and not(os.path.exists(arquivo_pos_conversao)):
        print("Ambos os arquivos não existem no diretório. Fim do teste")
    elif not os.path.exists(arquivo_original):
        print("Primeiro arquivo informado não existe no diretório. Fim do teste.")
    elif not os.path.exists(arquivo_pos_conversao):
        print("Segundo arquivo informado não existe no diretório. Fim do teste.")


    return False

def validacaoColunas(colunas_datas, arquivo_original, arquivo_convertido):
    """
    Função que testa se as colunas inseridas pelo usuário existem nos dois arquivos csv
    :param colunas_datas: Lista de colunas informadas pelo usuário
    :param arquivo_original: Arquivo csv do relatório original exportado em SAS
    :param arquivo_convertido: Arquivo csv do relatório exportado no Databricks
    :return: True, caso todas as colunas informadas existem nos dois arquivos csv
    """
    df_arquivo_original = pd.read_csv(arquivo_original)
    df_arquivo_convertido = pd.read_csv(arquivo_convertido)

    condicao_1 = set(df_arquivo_original.columns).intersection(set(colunas_datas)) == set(colunas_datas)
    condicao_2 = set(df_arquivo_convertido.columns).intersection(set(colunas_datas)) == set(colunas_datas)

    if condicao_1 and condicao_2:
        return True
    else:
        return False

def validacaoFormatoSAS(format_sas):
    """
    Esta função verifica se o formato de data inserido pelo usuário é válido.
    :param format_sas: String com formato de data.
    :return:
    """
    pd_formatos_datas = pd.read_excel('Formato Datas.xlsx')

    if format_sas in pd_formatos_datas['FORMAT DATE SAS'].values:
        return True
    else:
        return False


def compara_tipo_data(lista_colunas, arquivo_original, arquivo_convertido, format_sas):
    """
    Teste para comparar as colunas que recebem Data se respeitam o mesmo formato
    :param lista_colunas: Colunas do tipo Data informado pelo usuário
    :param arquivo_original: Path completo do arquivo do relatório csv gerado pelo SAS
    :param arquivo_convertido: Path completo do arquivo do relatório csv gerado pelo Databricks
    :param format_sas: Formato de dado em SAS no formato String
    :return:
    """
    if pre_condicao1 and pre_condicao2 and pre_condicao3:
        # print('Faça o teste')
        passou_teste = True

        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D16', format_sas)

        df_original = pd.read_csv(arquivo_original)
        df_convertido = pd.read_csv(arquivo_convertido)

        # Achar o formato de data em SAS equivalente em Datetime String
        df_formatos_datas = pd.read_excel('Formato Datas.xlsx')
        formato_equiv_databricks = \
            df_formatos_datas.loc[df_formatos_datas["FORMAT DATE SAS"] == format_sas, "FORMAT DATE DATABRICKS"].values[
                0]


        # Comparar data a data (dois a dois) se são exatamente iguais
        for cada_coluna_data in lista_colunas:
            for cada_data_original, cada_data_convertida in zip(df_original[cada_coluna_data].values,
                                                                df_convertido[cada_coluna_data].values):
                try:
                    # Crio objeto Datetime a partir da data do relatório em SAS
                    dt = datetime.strptime(cada_data_original, formato_equiv_databricks)
                    # Crio objeto Datetime a partir da data do relatório em Databricks
                    dt_2 = datetime.strptime(cada_data_convertida, formato_equiv_databricks)
                    if dt != dt_2:
                        print(f"As datas {cada_data_original} e {cada_data_convertida} na coluna "
                              f"{cada_coluna_data} são diferentes")
                        passou_teste = False
                        print("Teste Reprovado")
                        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E16', f"As datas {cada_data_original} e "
                                                                             f"{cada_data_convertida} na coluna "
                                                                             f"{cada_coluna_data} são diferentes")
                        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F16', 'REPROVADO')
                        break
                except ValueError:
                    # Não consegui converter a data convertida para o formato equivalente em Databricks
                    print(
                        "Formato da data no relatório do Databricks não é o mesmo formato de data do relatório do SAS")
                    print(f"Formato de data esperado no Databricks: {formato_equiv_databricks}")
                    print(f"Formato de data obtido no Databricks: {cada_data_convertida}")
                    passou_teste = False
                    print("Teste Reprovado")
                    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E16', formato_equiv_databricks)
                    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F16', 'REPROVADO')
                    break
        if passou_teste:
            print("As datas possuem o mesmo formato")
            print("Teste aprovado")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E16', formato_equiv_databricks )
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F16', 'APROVADO')
    else:
        print('Teste abortado: arquivo(s) com nome inválido')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F16', 'ABORTADO')

def compara_periodo_relatorio(coluna_data, periodo, arquivo_original, arquivo_convertido, format_sas):
    # Converte os periodos informados para datetime
    periodo_inicial = datetime.strptime(periodo.split()[0], "%d/%m/%Y")
    periodo_final = datetime.strptime(periodo.split()[1], "%d/%m/%Y")

    # Importa os dois relatórios
    df_original = pd.read_csv(arquivo_original)
    df_convertido = pd.read_csv(arquivo_convertido)

    # Converte a coluna de data informada para datetime
    df_formatos_datas = pd.read_excel('Formato Datas.xlsx')
    formato_equiv_databricks = \
        df_formatos_datas.loc[df_formatos_datas["FORMAT DATE SAS"] == format_sas, "FORMAT DATE DATABRICKS"].values[
            0]
    df_original[coluna_data] = pd.to_datetime(df_original[coluna_data], format=formato_equiv_databricks)
    df_convertido[coluna_data] = pd.to_datetime(df_convertido[coluna_data], format=formato_equiv_databricks)

    # Capturando o periodo do relatório emitido pelo SAS
    periodo_min_original = df_original[coluna_data].min()
    periodo_max_original = df_original[coluna_data].max()

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D18', f'[\
    {datetime.strftime(periodo_min_original, "%d/%m/%Y")}-\
    {datetime.strftime(periodo_max_original, "%d/%m/%Y")}]')

    # Capturando o periodo do relatório emitido pelo Databricks
    periodo_min_convertido = df_original[coluna_data].min()
    periodo_max_convertido = df_original[coluna_data].max()

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E18', f'[\
    {datetime.strftime(periodo_min_convertido, "%d/%m/%Y")}-\
    {datetime.strftime(periodo_max_convertido, "%d/%m/%Y")}]')

    condicao1 = (periodo_inicial <= periodo_min_original) and (periodo_final >= periodo_max_original)
    condicao2 = (periodo_inicial <= periodo_min_convertido) and (periodo_final >= periodo_max_convertido)

    if condicao1 and condicao2:
        print("O periodo dos dois relatórios condiz com o periodo informado pelo usuário")
        print("Teste Aprovado")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F18', 'APROVADO')
    else:
        print("O periodo dos dois relatórios NÃO condiz com o periodo informado pelo usuário")
        print(f"Período informado pelo usuário: {periodo.__str__()}")
        periodo_min_original_str = datetime.strftime(periodo_min_original, formato_equiv_databricks)
        periodo_max_original_str = datetime.strftime(periodo_max_original, formato_equiv_databricks)
        print(f"Período do relatório em SAS: [{periodo_min_original_str} {periodo_max_original_str}]")
        periodo_min_convertido_str = datetime.strftime(periodo_min_convertido, formato_equiv_databricks)
        periodo_max_convertido_str = datetime.strftime(periodo_max_convertido, formato_equiv_databricks)
        print(f"Período do relatório em Databricks: [{periodo_min_convertido_str} {periodo_max_convertido_str}]")
        print("Teste Reprovado")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F18', 'REPROVADO')




DIRETORIO_ATUAL = os.getcwd()

print("Teste de validação de formato de datas")
input_colunas = input("Insira o nome das colunas que são do tipo Data (separado por espaço) [DD/MM/YYYY]\n")
lista_colunas = input_colunas.split()

format_sas = input("Insira o formato de data original em SAS\n")

input_arquivos = input("Insira o nome das duas tabelas a comparar\n")

arquivo_original = DIRETORIO_ATUAL + "\\" + input_arquivos.split()[0]
arquivo_convertido = DIRETORIO_ATUAL + "\\" + input_arquivos.split()[1]

pre_condicao1 = testeExistenciaArquivos(arquivo_original, arquivo_convertido)
pre_condicao2 = validacaoColunas(lista_colunas, arquivo_original, arquivo_convertido)
pre_condicao3 = validacaoFormatoSAS(format_sas)

compara_tipo_data(lista_colunas, arquivo_original, arquivo_convertido, format_sas)

time.sleep(1)
os.system('cls')

print("Teste do período de datas")
input_periodo = input("Insira o período inicial e final do relatório usado para extrair a base [DD/MM/YYYY]\n")
coluna_data = input("Insira a coluna de data que representa o periodo do relatório\n")
compara_periodo_relatorio(coluna_data, input_periodo, arquivo_original, arquivo_convertido, format_sas)

time.sleep(1)
os.system('cls')

char = input("Deseja imprimir o relatório? [digite Y para 'sim'] ")
if char.lower() == 'y':
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C16', datetime.now())
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C18', datetime.now())
    epe.save_excel_file(ARQUIVO_EXCEL, DIRETORIO_DESTINO)
    print("Relatório atualizado com sucesso")
    print(f"Relatório disponível em {DIRETORIO_DESTINO}")
    time.sleep(2)