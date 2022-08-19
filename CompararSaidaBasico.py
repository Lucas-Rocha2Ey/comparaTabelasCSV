import os
import csv
import sys
import time
import pandas as pd
from datetime import datetime

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

    if extensao_original == extensao_pos_conversao:
        print(f"Os arquivos possuem o mesmo formato {extensao_original}.\nResultado: TESTE APROVADO\n")
    else:
        print(f"RESULTADO ESPERADO:\nArquivo original: {extensao_original}\n"\
              f"Arquivo convertido: {extensao_original}\n"\
              f"RESULTADO OBTIDO: \nArquivo original: {extensao_original}\n"\
              f"Arquivo convertido: {extensao_pos_conversao}.\nResultado: TESTE REPROVADO")

def testeQuantidadeLinhas(arquivo_original, arquivo_pos_conversao):
    """
        Este teste verifica se ambos os arquivos possui a mesma quantidade de linhas.
        Para fazer a comparação, ambos os arquivos devem estar no formato csv.
        :param arquivo_original: Caminho do arquivo no formato original
        :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
        :return: Quantidade de linhas das tabelas comparadas
        """
    print("TESTE: QUANTIDADE DE LINHAS")
    df_arquivo_original = pd.read_csv(arquivo_original)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao)

    if df_arquivo_original.shape[0] == df_arquivo_convertido.shape[0]:
        print(f"Os arquivos possuem a mesma quantidade de linhas - {df_arquivo_original.shape[0]} linhas.\n" \
              "Resultado: TESTE APROVADO\n")
    else:
        print(f"RESULTADO ESPERADO:\nArquivo original: {df_arquivo_original.shape[0] } linhas\n" \
              f"Arquivo convertido: {df_arquivo_original.shape[0]} linhas\n" \
              f"RESULTADO OBTIDO: \nArquivo original: {df_arquivo_original.shape[0]} linhas\n" \
              f"Arquivo convertido: {df_arquivo_convertido.shape[0]} linhas.\nResultado: TESTE REPROVADO\n")

def testeQuantidadeColunas(arquivo_original, arquivo_pos_conversao):
    """
    Este teste verifica se ambos os arquivos possui a mesma quantidade de colunas.
    Para fazer a comparação, ambos os arquivos devem estar no formato csv.
    :param arquivo_original: Caminho do arquivo no formato original
    :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
    :return: Quantidade de colunas das tabelas comparadas
    """
    print("TESTE: QUANTIDADE DE COLUNAS")
    # Esta função abre o arquivo e retorna um objeto no formato file.
    file_original = open(arquivo_original)
    file_convertido = open(arquivo_pos_conversao)

    # Esta função le o arquivo File e retorna um Csv.
    csv_original = csv.reader(file_original)
    csv_convertido = csv.reader(file_convertido)

    # O next é uma função que lê linha a linha.
    header_original = next(csv_original)
    header_convertido = next(csv_convertido)

    if len(header_original) == len(header_convertido):
        print(f"Os arquivos possuem a mesma quantidade de colunas - {len(header_original)} colunas.\n"\
                "Resultado: TESTE APROVADO\n")
    else:
        print(f"RESULTADO ESPERADO:\nArquivo original: {len(header_original)} colunas\n" \
              f"Arquivo convertido: {len(header_original)} colunas\n" \
              f"RESULTADO OBTIDO: \nArquivo original: {len(header_original)} colunas\n" \
              f"Arquivo convertido: {len(header_convertido)} colunas.\nResultado: TESTE REPROVADO\n")

    file_original.close()
    file_convertido.close()

def testeConteudoColunas(arquivo_original, arquivo_pos_conversao):
    """
    Este teste verifica se os dois arquivos possuem as mesmas colunas na mesma ordem do original.
    Necessário que ambos os arquivos estejam em csv.
    :param arquivo_original: Caminho do arquivo no formato original
    :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
    :return: Lista com as colunas em cada uma das tabelas
    """
    print("TESTE: CONTEÚDO DAS COLUNAS")
    df_arquivo_original = pd.read_csv(arquivo_original)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao)

    if list(df_arquivo_original.columns) == list(df_arquivo_convertido.columns):
        print(f"Os arquivos possuem as mesmas colunas - {list(df_arquivo_original.columns)}.\n" \
              "Resultado: TESTE APROVADO\n")
    else:
        print(f"RESULTADO ESPERADO:\nArquivo original: {list(df_arquivo_original.columns)}\n" \
              f"Arquivo convertido: {list(df_arquivo_original.columns)}\n" \
              f"RESULTADO OBTIDO: \nArquivo original: {list(df_arquivo_original.columns)}\n" \
              f"Arquivo convertido: {list(df_arquivo_convertido.columns)}\nResultado: TESTE REPROVADO\n")

def testeConteudoLinhas(arquivo_original, arquivo_pos_conversao):
    """
        Este teste verifica se os dois arquivos possuem as mesmas linhas, na mesma ordem.
        Necessário que ambos os arquivos estejam em csv.
        :param arquivo_original: Caminho do arquivo no formato original
        :param arquivo_pos_conversao: Caminho do arquivo no formato após a conversão
        :return: Mensagem de teste aprovado ou a(s) Linha(s) que estão retornando resultados diferentes
    """
    print("TESTE: CONTEÚDO DAS LINHAS NA ORDEM")
    passou = True
    df_arquivo_original = pd.read_csv(arquivo_original)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao)

    try:
        for index, row in df_arquivo_original.iterrows():
            linha_arquivo_convertido = list(df_arquivo_convertido.iloc[index])
            if list(row) != linha_arquivo_convertido:
                print(f"Linha {int(index) + 1}:\n"\
                      f"RESULTADO ESPERADO:\nArquivo original: {list(row)}\nArquivo convertido: {list(row)}\n"
                      f"RESULTADO OBTIDO:\nArquivo original: {list(row)}\nArquivo convertido: {linha_arquivo_convertido}\n")
                passou = False

        if passou:
            print("Os arquivos possuem o mesmo conteúdo, na mesma ordem.\nResultado: TESTE APROVADO\n")
        else:
            print("Resultado: TESTE REPROVADO\n")
    except IndexError:
        print("Não é possível terminar o teste porque as duas tabelas não tem exatamente o mesmo número de linhas")
        print("Resultado: TESTE REPROVADO\n")

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
    df_arquivo_original = pd.read_csv(arquivo_original)
    df_arquivo_convertido = pd.read_csv(arquivo_pos_conversao)

    conjunto_linhas_arquivo_original = set()
    conjunto_linhas_arquivo_convertido = set()

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
        elif conjunto_linhas_arquivo_original.difference(conjunto_linhas_arquivo_convertido) != set():
            print(f"Há {len(conjunto_linhas_arquivo_original.difference(conjunto_linhas_arquivo_convertido))}"
                  " linhas no arquivo Original, mas ausente no convertido:")
            print("Resultado: TESTE REPROVADO!\n")
    except IndexError:
        print("Não é possível terminar o teste porque os arquivos não possuem exatamente o mesmo número de linhas")
        print("Resultado: TESTE REPROVADO!\n")



if sys.argv[1].lower() == '-h':
    print("Insira como parâmetros o nome do arquivo do relatório emitido no SAS e no Databricks, respectivamente")
    print("Exemplo: python CompararSaidaBasico.py relatorio_sas.csv relatorio_databricks.csv")
else:
    # Os dois arquivos passarei como parâmetros ao executar o prompt
    arquivo_1 = os.getcwd() + "\\" + sys.argv[1]
    arquivo_2 = os.getcwd() + "\\" + sys.argv[2]

    if testeExistenciaArquivos(arquivo_1, arquivo_2):

        #Imprimindo na tela
        # Mostrando na tela o relatório do teste
        print("Relatório final do teste - Comparação de Saídas\n")
        print(f"Arquivo original: {arquivo_1}")
        print(f"Arquivo convertido: {arquivo_2}\n\n")
        inicio = datetime.now()
        testeExtensao(arquivo_1, arquivo_2)
        testeQuantidadeLinhas(arquivo_1, arquivo_2)
        testeQuantidadeColunas(arquivo_1, arquivo_2)
        testeConteudoColunas(arquivo_1, arquivo_2)
        testeConteudoLinhas2(arquivo_1, arquivo_2)
        testeConteudoLinhas(arquivo_1, arquivo_2)
        fim = datetime.now() - inicio

        # Imprimindo na tela que o teste foi concluido
        print(f"Teste concluido em {round(fim.total_seconds(), 2)} segundos ")

        char = input("Deseja imprimir o relatório? [digite Y para 'sim'] ")
        if char.lower() == 'y':
            # Gerando o txt com o relatório
            sys.stdout = open('Relatorio Final do Teste - Comparação de Saídas.txt', 'w')
            print("Relatório final do teste\n")
            print(f"Data de Execução: {inicio.strftime('%d/%m/%Y %H:%M')}\n")
            print(f"Arquivo original: {arquivo_1}")
            print(f"Arquivo convertido: {arquivo_2}\n\n")
            testeExtensao(arquivo_1, arquivo_2)
            testeQuantidadeLinhas(arquivo_1, arquivo_2)
            testeQuantidadeColunas(arquivo_1, arquivo_2)
            testeConteudoColunas(arquivo_1, arquivo_2)
            testeConteudoLinhas2(arquivo_1, arquivo_2)
            testeConteudoLinhas(arquivo_1, arquivo_2)
            print(f"Teste concluido em {round(fim.total_seconds(), 2)} segundos ")
            sys.stdout = sys.__stdout__  # Este comando volta a imprimir no console
            sys.stdout.write("Relatório imprimido com sucesso!")
            time.sleep(2)
            sys.stdout.close()
        else:
            print("O script será fechado em 2 segundos...")
            time.sleep(2)
