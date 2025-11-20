import sqlite3
import os

DB_NAME = 'motos_projeto_final.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Cria tabelas e popula dados iniciais se o banco não existir"""
    # Verifica se o arquivo do banco já existe para não resetar sempre
    novo_banco = not os.path.exists(DB_NAME)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Caminho para os scripts SQL
    base_dir = os.path.dirname(__file__)
    schema_path = os.path.join(base_dir, 'schema.sql')
    populate_path = os.path.join(base_dir, 'populate.sql')
    
    # Executa Schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())
        
    # Executa Populate apenas se for banco novo
    if novo_banco:
        try:
            with open(populate_path, 'r', encoding='utf-8') as f:
                cursor.executescript(f.read())
            print("Banco de dados populado com sucesso!")
        except FileNotFoundError:
            print("Arquivo populate.sql não encontrado, banco criado vazio.")
            
    conn.commit()
    conn.close()