import tkinter as tk
from database.db_connection import init_db
from src.ui.main_window import MotorcycleManagerApp, LoginWindow

def start_app():
    """
    Função callback que inicia a aplicação principal.
    Só é chamada se o login for realizado com sucesso.
    """
    # Cria a janela principal do sistema
    root = tk.Tk()
    
    # Inicializa a classe da aplicação passando a janela root
    app = MotorcycleManagerApp(root)
    
    # Mantém o loop da interface gráfica rodando
    root.mainloop()

if __name__ == '__main__':
    print("--- SISTEMA MOTOMANAGER PRO ---")
    
    # 1. Inicialização do Banco de Dados
    # Verifica se o arquivo .db existe. Se não existir, cria e popula com dados iniciais.
    print("1. Verificando banco de dados...")
    init_db()
    
    # 2. Inicia a Tela de Login
    # O Tkinter precisa de uma instância raiz (root) para a janela de login
    print("2. Abrindo tela de login...")
    login_root = tk.Tk()
    
    # Instancia a janela de login e passa a função 'start_app' para ser chamada depois
    login_app = LoginWindow(login_root, start_app)
    
    # Inicia o loop da janela de login
    login_root.mainloop()