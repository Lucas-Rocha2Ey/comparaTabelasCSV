import os
import csv
import sys
import time
import pandas as pd
import numpy as np
import escrevendo_planilha_excel as epe
from datetime import datetime
import unicodedata

DIRETORIO_ATUAL = os.getcwd()
ARQUIVO_TEMPLATE = DIRETORIO_ATUAL + '\\Template - Relatório de teste.xlsx'
DIRETORIO_DESTINO = DIRETORIO_ATUAL + '\\Relatório de teste.xlsx'

sep_sas = ',' # O vírgula é o separador padrão.

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

def testeExtensao(arquivo_original, arquivo_pos_conversao):
    """
    O objetivo do teste é comparar se a extensão dos dois arquivos é a mesma.
    :param arquivo_original: Caminho do arquivo no formato original
    :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
    :return: Relatório final do teste
    """
    print("TESTE: FORMATO DOS ARQUIVOS")
    extensao_original = os.path.splitext(arquivo_original)[-1]
    extensao_pos_conversao = os.path.splitext(arquivo_pos_conversao)[-1]

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C9', datetime.now())
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D9', extensao_original)
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E9', extensao_pos_conversao)

    if extensao_original == extensao_pos_conversao:
        print(f"Os arquivos possuem o mesmo formato {extensao_original}.\nResultado: TESTE APROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F9', 'APROVADO')
    else:
        print(f"RESULTADO ESPERADO:\nArquivo original: {extensao_original}\n"\
              f"Arquivo convertido: {extensao_original}\n"\
              f"RESULTADO OBTIDO: \nArquivo original: {extensao_original}\n"\
              f"Arquivo convertido: {extensao_pos_conversao}.\nResultado: TESTE REPROVADO")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F9', 'REPROVADO')

def testeQuantidadeLinhas(arquivo_original, arquivo_pos_conversao):
    """
        Este teste verifica se ambos os arquivos possui a mesma quantidade de linhas.
        Para fazer a comparação, ambos os arquivos devem estar no formato csv.
        :param arquivo_original: Caminho do arquivo no formato original
        :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
        :return: Quantidade de linhas das tabelas comparadas
        """
    print("TESTE: QUANTIDADE DE LINHAS")
    df_arquivo_original = pd.read_csv(arquivo_original, encoding='ISO-8859-1', sep=sep_sas)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao, encoding='ISO-8859-1')

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C10', datetime.now())
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D10', df_arquivo_original.shape[0])
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E10', df_arquivo_convertido.shape[0])

    if df_arquivo_original.shape[0] == df_arquivo_convertido.shape[0]:
        print(f"Os arquivos possuem a mesma quantidade de linhas - {df_arquivo_original.shape[0]} linhas.\n" \
              "Resultado: TESTE APROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F10', 'APROVADO')
    else:
        print(f"RESULTADO ESPERADO:\nArquivo original: {df_arquivo_original.shape[0] } linhas\n" \
              f"Arquivo convertido: {df_arquivo_original.shape[0]} linhas\n" \
              f"RESULTADO OBTIDO: \nArquivo original: {df_arquivo_original.shape[0]} linhas\n" \
              f"Arquivo convertido: {df_arquivo_convertido.shape[0]} linhas.\nResultado: TESTE REPROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F10', 'REPROVADO')

def testeQuantidadeColunas(arquivo_original, arquivo_pos_conversao):
    """
    Este teste verifica se ambos os arquivos possui a mesma quantidade de colunas.
    Para fazer a comparação, ambos os arquivos devem estar no formato csv.
    :param arquivo_original: Caminho do arquivo no formato original
    :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
    :return: Quantidade de colunas das tabelas comparadas
    """
    print("TESTE: QUANTIDADE DE COLUNAS")
    df_arquivo_original = pd.read_csv(arquivo_original, encoding='ISO-8859-1', sep=sep_sas)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao, encoding='ISO-8859-1')

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C11', datetime.now())
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D11', df_arquivo_original.shape[1])
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E11', df_arquivo_convertido.shape[1])

    if df_arquivo_original.shape[1] == df_arquivo_convertido.shape[1]:
        print(f"Os arquivos possuem a mesma quantidade de colunas - {df_arquivo_original.shape[1]} colunas.\n"\
                "Resultado: TESTE APROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F11', 'APROVADO')
    else:
        print(f"RESULTADO ESPERADO:\nArquivo original: {df_arquivo_original.shape[1]} colunas\n" \
              f"Arquivo convertido: {df_arquivo_original.shape[1]} colunas\n" \
              f"RESULTADO OBTIDO: \nArquivo original: {df_arquivo_original.shape[1]} colunas\n" \
              f"Arquivo convertido: {df_arquivo_convertido.shape[1]} colunas.\nResultado: TESTE REPROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F11', 'REPROVADO')


def testeConteudoColunas(arquivo_original, arquivo_pos_conversao):
    """
    Este teste verifica se os dois arquivos possuem as mesmas colunas na mesma ordem do original.
    Necessário que ambos os arquivos estejam em csv.
    :param arquivo_original: Caminho do arquivo no formato original
    :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
    :return: Lista com as colunas em cada uma das tabelas
    """
    print("TESTE: CONTEÚDO DAS COLUNAS")
    df_arquivo_original = pd.read_csv(arquivo_original, encoding='ISO-8859-1', sep=sep_sas)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao, encoding='ISO-8859-1')

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C12', datetime.now())
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D12', list(df_arquivo_original.columns).__str__())
    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E12', list(df_arquivo_convertido.columns).__str__())

    if list(df_arquivo_original.columns) == list(df_arquivo_convertido.columns):
        print(f"Os arquivos possuem as mesmas colunas - {list(df_arquivo_original.columns)}.\n" \
              "Resultado: TESTE APROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F12', 'APROVADO')
    else:
        ##### Colunas do SAS vao passar por um tratamento se contém espaços e pontos e passará por uma
        ##### nova comparação
        colunas_sas_transf = []

        for cada_colunas_sas in df_arquivo_original.columns:
            new_column_1 = cada_colunas_sas.replace('. ', '_') # Substitui '. ' por '_'
            new_column_2 = new_column_1.replace('.', '_')
            new_column_3 = new_column_2.replace(' - ', '_')
            new_column_4 = new_column_3.replace('- ', '_')
            new_column_5 = new_column_4.replace('-', '_')
            new_column = new_column_5.replace(' ', '_')
            # Linha abaixo retira acentos/caracteres especiais
            new_column = ''.join(
                ch for ch in unicodedata.normalize('NFKD', new_column) if not unicodedata.combining(ch))
            colunas_sas_transf.append(new_column)

        if colunas_sas_transf == list(df_arquivo_convertido.columns):
            print(f"Os arquivos possuem as mesmas colunas, porém sofreu tratamento de espaços ou acentos especiais\n" \
                  "Resultado: TESTE APROVADO\n")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F12',
                                 'APROVADO - COM TRATAMENTO DE ESPAÇO E CARACTERES ESPECIAIS')
        else:
            print(f"RESULTADO ESPERADO:\nArquivo original: {list(df_arquivo_original.columns)}\n" \
                  f"Arquivo original - tratado: {colunas_sas_transf}\n" \
                  f"Arquivo convertido: {colunas_sas_transf}\n" \
                  f"RESULTADO OBTIDO: \nArquivo original: {list(df_arquivo_original.columns)}\n" \
                  f"Arquivo original - tratado: {colunas_sas_transf}\n" \
                  f"Arquivo convertido: {list(df_arquivo_convertido.columns)}\nResultado: TESTE REPROVADO\n")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F12', 'REPROVADO')







def testeConteudoLinhas(arquivo_original, arquivo_pos_conversao):
    """
        Este teste verifica se os dois arquivos possuem as mesmas linhas, na mesma ordem.
        Necessário que ambos os arquivos estejam em csv.
        :param arquivo_original: Caminho do arquivo no formato original
        :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
        :return: Mensagem de teste aprovado ou a(s) Linha(s) que estão retornando resultados diferentes
    """
    print("TESTE: CONTEÚDO DAS LINHAS NA ORDEM")
    df_arquivo_original = pd.read_csv(arquivo_original, encoding='ISO-8859-1', sep=sep_sas)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao, encoding='ISO-8859-1')

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C13', datetime.now())

    #colocando as colunas iguais das duas tabelas
    if (df_arquivo_original.columns != df_arquivo_convertido.columns).all():
        df_arquivo_original.columns = df_arquivo_convertido.columns

    try:
        if any(df_arquivo_original.dtypes != df_arquivo_convertido.dtypes):
            # Data types são diferentes, tentando converter
            df_arquivo_convertido = df_arquivo_convertido.astype(df_arquivo_original.dtypes)
        if df_arquivo_original.equals(df_arquivo_convertido):
            print("Os arquivos possuem o mesmo conteúdo, na mesma ordem.\nResultado: TESTE APROVADO\n")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E13', 'MESMO CONTEÚDO DO SAS, NA ORDEM')
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F13', 'APROVADO')
        else:
            diff_mask = (df_arquivo_original != df_arquivo_convertido) & ~(df_arquivo_original.isnull() \
                                                                           & df_arquivo_convertido.isnull())
            ne_stacked = diff_mask.stack()
            changed = ne_stacked[ne_stacked]
            changed.index.names = ['linha', 'coluna databricks']
            difference_locations = np.where(diff_mask)
            changed_sas = df_arquivo_original.values[difference_locations]
            changed_databricks = df_arquivo_convertido.values[difference_locations]
            df_diferenca = pd.DataFrame({'linha': changed.index.get_level_values('linha') + 1,
                                         'coluna databricks': changed.index.get_level_values('coluna databricks'),
                                         'SAS': changed_sas, 'DATABRICKS': changed_databricks})
            print(f"Quantidade de linhas diferentes = {len(df_diferenca['linha'].unique())}")
            print("Linhas que se diferem do SAS e Databricks:\n")
            print(df_diferenca)
            print("Resultado: TESTE REPROVADO\n")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E13', 'CONTEÚDO DIFERENTE DO SAS')
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F13', 'REPROVADO')
    except IndexError:
        print("Não é possível terminar o teste porque as duas tabelas não tem exatamente o mesmo número de linhas")
        print("Resultado: TESTE REPROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E13', 'QUANTIDADE DE LINHAS NÃO BATE COM SAS')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F13', 'REPROVADO')
    except ValueError:
        if df_arquivo_original.shape[0] < df_arquivo_convertido.shape[0]:
            print(f'Não é possível terminar o teste porque há '
                  f'{int(df_arquivo_convertido.shape[0]) - int(df_arquivo_original.shape[0])} '
                  f'linhas na tabela convertida, ausente na linha original.')
        if df_arquivo_original.shape[0] > df_arquivo_convertido.shape[0]:
            print(f'Não é possível terminar o teste porque há '
                  f'{int(df_arquivo_original.shape[0]) - int(df_arquivo_convertido.shape[0])} '
                  f'linhas na tabela original, ausente na linha convertida.')
        print("Resultado: TESTE REPROVADO\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E13', 'QUANTIDADE DE LINHAS NÃO BATE COM SAS')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F13', 'REPROVADO')

def testeConteudoLinhas2(arquivo_original, arquivo_pos_conversao):
    """
        Este teste verifica se os dois arquivos possuem as mesmas linhas, independente.
        Necessário que ambos os arquivos estejam em csv.
        :param arquivo_original: Caminho do arquivo no formato original
        :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
        :return: Mensagem de teste aprovado ou a(s) Linha(s) que estão retornando resultados diferentes
    """
    print("TESTE: CONTEÚDO DAS LINHAS")
    passou = True
    df_arquivo_original = pd.read_csv(arquivo_original, encoding='ISO-8859-1', sep=sep_sas)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao, encoding='ISO-8859-1')

    conjunto_linhas_arquivo_original = set()
    conjunto_linhas_arquivo_convertido = set()

    epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C14', datetime.now())

    try:
        # Adicionando cada linha aos conjuntos
        for index, row in df_arquivo_original.iterrows():
            conjunto_linhas_arquivo_original.add(tuple(df_arquivo_original.iloc[index]))

        for index, row in df_arquivo_convertido.iterrows():
            conjunto_linhas_arquivo_convertido.add(tuple(df_arquivo_convertido.iloc[index]))

        # Se a interseção entre os dois arquivos for igual o conjunto das linhas originais,
        # Significa que ambos os conjuntos são iguais.
        if conjunto_linhas_arquivo_original.intersection(conjunto_linhas_arquivo_convertido)\
                == conjunto_linhas_arquivo_original:
            print("Os arquivos possuem o mesmo conteúdo.\nResultado: TESTE APROVADO\n")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D14', 'OK')
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E14', 'MESMO CONTEÚDO')
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F14', 'APROVADO')
        elif conjunto_linhas_arquivo_original.difference(conjunto_linhas_arquivo_convertido) != set():
            print(f"Há {len(conjunto_linhas_arquivo_original.difference(conjunto_linhas_arquivo_convertido))}"
                  " linhas no arquivo Original, mas ausente no convertido:")
            print("Resultado: TESTE REPROVADO!\n")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D14', 'OK')
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E14', f"Há "
            f"{len(conjunto_linhas_arquivo_original.difference(conjunto_linhas_arquivo_convertido))}"
            f" linhas ausente no relatório")
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F14', 'REPROVADO ')
    except IndexError:
        print("Não é possível terminar o teste porque os arquivos não possuem exatamente o mesmo número de linhas")
        print("Resultado: TESTE REPROVADO!\n")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'D14', 'OK')
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'E14', f"Não é possível terminar o teste porque os arquivos" 
        f"não possuem exatamente o mesmo número de linhas")
        epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'F14', 'REPROVADO ')





if sys.argv[1].lower() == '-h':
    print("Insira como parâmetros o nome do arquivo do relatório emitido no SAS e no Databricks, respectivamente")
    print("Exemplo: python CompararSaidaBasico.py relatorio_sas.csv relatorio_databricks.csv")
else:
    # Os dois arquivos passarei como parâmetros ao executar o prompt
    arquivo_1 = os.getcwd() + "\\" + sys.argv[1]
    arquivo_2 = os.getcwd() + "\\" + sys.argv[2]

    if testeExistenciaArquivos(arquivo_1, arquivo_2):

        sep_option = int(input("Defina a opção para o separador usado no arquivo do SAS (1- ;, 2- , 3- Nenhum)\n"))
        if sep_option == 1:
            sep_sas = ';'
        elif sep_option == 2:
            sep_sas = ','
        else:
            sep_sas = None

        print("\nTabela de Testes\n")
        df = pd.DataFrame({'Cod': [1, 2, 3, 4, 5, 6],
                           'Teste': ["Teste de Extensão",
                                     "Teste de Quantidade de Linhas",
                                     "Teste de Quantidade de Colunas",
                                     "Teste de Conteúdo das Colunas",
                                     "Conteudo das Linhas",
                                     "Todos"]})
        df.set_index('Cod', inplace=True)
        print(df)

        input_testes = input("Digite o(s) código(s) dos testes que deseja executar, separado por espaço (Ex:1 3 4)\n")
        lista_testes = input_testes.split()

        #Imprimindo na tela
        # Mostrando na tela o relatório do teste
        print("Relatório final do teste - Comparação de Saídas\n")
        print(f"Arquivo original: {arquivo_1}")
        print(f"Arquivo convertido: {arquivo_2}\n\n")
        inicio = datetime.now()
        if '6' in lista_testes:
            testeExtensao(arquivo_1, arquivo_2)
            testeQuantidadeLinhas(arquivo_1, arquivo_2)
            testeQuantidadeColunas(arquivo_1, arquivo_2)
            testeConteudoColunas(arquivo_1, arquivo_2)
            testeConteudoLinhas(arquivo_1, arquivo_2)
        else:
            for cadaCodigo in lista_testes:
                if int(cadaCodigo) == 1:
                    testeExtensao(arquivo_1, arquivo_2)
                elif int(cadaCodigo) == 2:
                    testeQuantidadeLinhas(arquivo_1, arquivo_2)
                elif int(cadaCodigo) == 3:
                    testeQuantidadeColunas(arquivo_1, arquivo_2)
                elif int(cadaCodigo) == 4:
                    testeConteudoColunas(arquivo_1, arquivo_2)
                elif int(cadaCodigo) == 5:
                    testeConteudoLinhas(arquivo_1, arquivo_2)
        fim = datetime.now() - inicio

        # Imprimindo na tela que o teste foi concluido
        print(f"Teste concluido em {round(fim.total_seconds(), 2)} segundos ")

        char = input("Deseja imprimir o relatório? [digite Y para 'sim'] ")
        if char.lower() == 'y':
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C3', arquivo_1.split('\\')[-1])
            epe.write_cell_excel(ARQUIVO_EXCEL, 'Sheet1', 'C4', arquivo_2.split('\\')[-1])
            # Gerando o txt com o relatório
            sys.stdout = open('Relatorio Final do Teste - Comparação de Saídas.txt', 'w')
            print("Relatório final do teste\n")
            print(f"Data de Execução: {inicio.strftime('%d/%m/%Y %H:%M')}\n")
            print(f"Arquivo original: {arquivo_1}")
            print(f"Arquivo convertido: {arquivo_2}\n\n")
            if '6' in lista_testes:
                testeExtensao(arquivo_1, arquivo_2)
                testeQuantidadeLinhas(arquivo_1, arquivo_2)
                testeQuantidadeColunas(arquivo_1, arquivo_2)
                testeConteudoColunas(arquivo_1, arquivo_2)
                testeConteudoLinhas(arquivo_1, arquivo_2)
            else:
                for cadaCodigo in lista_testes:
                    if int(cadaCodigo) == 1:
                        testeExtensao(arquivo_1, arquivo_2)
                    elif int(cadaCodigo) == 2:
                        testeQuantidadeLinhas(arquivo_1, arquivo_2)
                    elif int(cadaCodigo) == 3:
                        testeQuantidadeColunas(arquivo_1, arquivo_2)
                    elif int(cadaCodigo) == 4:
                        testeConteudoColunas(arquivo_1, arquivo_2)
                    elif int(cadaCodigo) == 5:
                        testeConteudoLinhas(arquivo_1, arquivo_2)
            print(f"Teste concluido em {round(fim.total_seconds(), 2)} segundos ")
            epe.save_excel_file(ARQUIVO_EXCEL, DIRETORIO_DESTINO)
            sys.stdout = sys.__stdout__  # Este comando volta a imprimir no console
            sys.stdout.write("Relatório imprimido com sucesso!")
            time.sleep(2)
            sys.stdout.close()
        else:
            print("O script será fechado em 2 segundos...")
            time.sleep(2)
