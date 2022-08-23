Ordem de execução dos testes:

1 - Abra o prompt de comando do Windows 
2 - Digite cd [diretório atual desta pasta na sua máquina]
3 - Insira o comando python CompararSaidaBasico.py [nome do csv extraido pelo sas].csv [nome do csv extraido pelo databricks].csv
4 - Abra o arquivo sas_proc_content_mock.csv e insira as informações das variaveis do proc content na tabela Alphabetic List of
Variables and Attributes, a partir da 3a linha, separados por vírgula. Mantenha cabeçalhos intactos. Após a edição, salve
5 - Extraia os dtypes em csv do databricks (só digitar no comando da célula display(nome_do_dataframe.dtypes)) e clicar no botão 
Donwload CSV, localizado abaixo da mensagem 'Showing all X rows.'
6 - Copie as informações (excluindo cabeçalhos _0 que vem no arquivo original) e cole no arquivo mock_data_dtypes_databricks.csv
a partir da segunda linha
7 - Volte ao prompt de comando e execute o teste comparar_dtypes.py e siga os passos do prompt (python comparar_dtypes.py)
8 - Antes de executar o passo 9, consulte na tabela de proc contents qual é o formato de data do SAS da coluna que contém o periodo
do relatório extraído. Voce vai precisar dessa informacão antes de executar o script.
9 - Execute o teste comparar_tipo_data.py e siga os passos do prompt (python comparar_tipo_data.py)

================================

Observações:

- Não esquecer de sempre digitar 'y' quando o prompt perguntar se quer exportar o relatório. 

- Os testes CompararSaidaBasico.py e comparar_dtypes.py exportam também um relatório em txt contendo detalhes dos testes realizados. 


