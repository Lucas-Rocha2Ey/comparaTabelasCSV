import datetime
import os
import sys
import shutil
import time
from openpyxl import load_workbook, Workbook


# Checando que o arquivo de template existe
def does_file_exist(file_path):
    """ Check if file exists"""
    return os.path.exists(file_path)

def copy_file(file_path):
    """ This function copy a template and create a new file
     :return Target path of a new file"""
    diretorio_atual = os.getcwd()

    origem = file_path
    destino = diretorio_atual + '\\Relatório de teste.xlsx'
    try:
        shutil.copyfile(origem, destino)
        return destino
    except PermissionError:
        print("O arquivo não pode ser criado. Feche o arquivo e tente executar o script novamente")
        sys.exit(1)

def load_excel_file(file_path):
    """ This function loads a excel filed located on file_path parameter and it returns a Workbook class object."""
    workbook_file = load_workbook(file_path)
    return workbook_file

def save_excel_file(wb: Workbook, file_path):
    """ This functions saves a excel file at the file_path as a parameter."""
    wb.save(file_path)

def write_cell_excel(excel: Workbook, sheet_name, cell, value):
    """ This function writes a value at a cell and sheet inputted as parameters. """
    planilha = excel[sheet_name]
    planilha[cell] = value

def demo():
    """ Função de teste para testar as demais funções do excel """
    diretorio_atual = os.getcwd()
    arquivo_template = diretorio_atual + '\\Template - Relatório de teste.xlsx'
    file_exists = does_file_exist(arquivo_template)
    if file_exists:
        print("O arquivo de template existe")
        ##### Copia o arquivo para poder escrever
        new_file = copy_file(arquivo_template)
        ##### Abre o arquivo excel
        excel = load_excel_file(new_file)
        ##### Acessa a planilha
        write_cell_excel(excel, 'Sheet1', 'C6', 'Outro tester')
        write_cell_excel(excel, 'Sheet1', 'C9', datetime.datetime.now())
        write_cell_excel(excel, 'Sheet1', 'F9', 'Aprovado')
        #planilha = excel['Sheet1']
        ##### Escrevendo o nome do tester
        #planilha['C6'] = 'Lucas Rocha Gonçalves Soares'
        #planilha['C6'] = 'Rodrigo'
        #planilha['C9'] = datetime.datetime.now()
        save_excel_file(excel, new_file)
        print('Arquivo escrito com sucesso!')
    else:
        print("O arquivo de template não existe")
        sys.exit(1)
