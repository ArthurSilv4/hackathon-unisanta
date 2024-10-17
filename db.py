import pandas as pd
import pyodbc
import json
from dotenv import load_dotenv
import os

# Função para ler o arquivo JSON
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Função para armazenar os dados no SQL Server
def store_data_in_sql_server(data, table_name, connection_string):
    # Converte os dados para um DataFrame do pandas
    df = pd.DataFrame(data)
    
    # Conecta ao SQL Server
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Cria a tabela se não existir
    create_table_query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
    CREATE TABLE {table_name} (
        {', '.join([f'{col} NVARCHAR(MAX)' for col in df.columns])}
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    
    # Insere os dados na tabela
    for index, row in df.iterrows():
        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['?' for _ in df.columns])})"
        cursor.execute(insert_query, tuple(row))
    
    conn.commit()
    cursor.close()
    conn.close()

# Caminho para o arquivo JSON
json_file_path = 'data.json'

# String de conexão para o SQL Server
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# String de conexão para o SQL Server
connection_string = os.getenv('SQL_SERVER_CONNECTION_STRING')

# Nome da tabela onde os dados serão armazenados
table_name = 'Eventos'

# Lê os dados do arquivo JSON
data = read_json_file(json_file_path)

# Armazena os dados no SQL Server
store_data_in_sql_server(data, table_name, connection_string)
