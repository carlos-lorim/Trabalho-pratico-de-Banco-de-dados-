import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.ui.styles import CORES, FONTES
from src.dao.moto_dao import MotoDAO

# --- CLASSE DE LOGIN ---
class LoginWindow:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.root.title("🔐 Acesso ao Sistema")
        self.root.geometry("400x350")
        self.root.configure(bg=CORES['bg_app'])
        self.on_success = on_success_callback
        
        # Centralizar
        frame = tk.Frame(root, bg="white", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="MotoManager Pro", font=FONTES['h1'], bg="white", fg=CORES['primary']).pack(pady=10)
        
        tk.Label(frame, text="Usuário:", font=FONTES['label'], bg="white").pack(anchor="w")
        self.user_entry = ttk.Entry(frame)
        self.user_entry.pack(fill="x", pady=5)
        self.user_entry.insert(0, "admin") # Pré-preenchido
        
        tk.Label(frame, text="Senha:", font=FONTES['label'], bg="white").pack(anchor="w")
        self.pass_entry = ttk.Entry(frame, show="*")
        self.pass_entry.pack(fill="x", pady=5)
        self.pass_entry.insert(0, "admin") # Pré-preenchido
        
        ttk.Button(frame, text="ENTRAR", command=self.check_login, style='Primary.TButton').pack(fill="x", pady=20)
        
        tk.Label(frame, text="Login padrão: admin / admin", font=("Segoe UI", 8), bg="white", fg="gray").pack()

    def check_login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if u == "admin" and p == "admin":
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Erro", "Acesso Negado! Tente admin/admin")

# --- CLASSE PRINCIPAL ---
class MotorcycleManagerApp:
    def __init__(self, root):
        self.root = root
        self.dao = MotoDAO()
        self.categorias_map = {}
        self.selected_id = None
        
        self.root.title("🚀 MotoManager Pro - Sistema Nota 10")
        self.root.geometry("1250x850")
        try:
            self.root.state('zoomed')
        except:
            self.root.attributes('-zoomed', True)
            
        self.root.minsize(1000, 700)
        self.root.configure(bg=CORES['bg_app'])
        
        self.setup_style()
        self.setup_variables()
        
        # Layout
        self.setup_dashboard()
        
        self.notebook_container = tk.Frame(self.root, bg=CORES['bg_app'])
        self.notebook_container.pack(fill='both', expand=True, padx=20, pady=15)

        self.notebook = ttk.Notebook(self.notebook_container)
        self.notebook.pack(fill='both', expand=True)
        
        self.tab_estoque = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estoque, text='   📦 ESTOQUE   ')
        self.setup_tab_estoque()
        
        self.tab_gastos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_gastos, text='   🛠️ GASTOS   ')
        self.setup_tab_gastos()

        self.tab_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_relatorios, text='   📊 CONSULTAS COMPLEXAS   ')
        self.setup_tab_relatorios()
        
        self.carregar_categorias()
        self.view_records()
        self.update_dashboard()

    def setup_variables(self):
        self.nome_text = tk.StringVar()
        self.ano_text = tk.StringVar()
        self.valor_compra_text = tk.StringVar()
        self.valor_venda_text = tk.StringVar()
        self.antigo_dono_text = tk.StringVar()
        self.status_text = tk.StringVar(value="Em Estoque")
        self.placa_text = tk.StringVar()
        self.km_text = tk.StringVar()
        self.cor_text = tk.StringVar()
        self.categoria_text = tk.StringVar()
        
        self.gasto_moto_selecionada = tk.StringVar()
        self.gasto_descricao = tk.StringVar()
        self.gasto_valor = tk.StringVar()
        self.busca_var = tk.StringVar()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=CORES['bg_app'])
        style.configure('TLabel', background=CORES['bg_app'], foreground=CORES['text'], font=FONTES['body'])
        style.configure('TLabelframe', background=CORES['bg_app'], bordercolor="#BDC3C7", relief="solid", borderwidth=1)
        style.configure('TLabelframe.Label', background=CORES['bg_app'], foreground=CORES['primary'], font=FONTES['h2'])
        style.configure('TEntry', fieldbackground='white', borderwidth=1, relief="solid")
        style.configure('TCombobox', fieldbackground='white', arrowsize=14)
        style.configure('TButton', font=('Segoe UI', 9, 'bold'), borderwidth=0, padding=8)
        style.map('TButton', background=[('active', '#BDC3C7')])
        style.configure('Success.TButton', background=CORES['success'], foreground='white')
        style.map('Success.TButton', background=[('active', '#219150')])
        style.configure('Danger.TButton', background=CORES['danger'], foreground='white')
        style.map('Danger.TButton', background=[('active', '#A93226')])
        style.configure('Primary.TButton', background=CORES['primary'], foreground='white')
        style.map('Primary.TButton', background=[('active', '#1F618D')])
        style.configure("Treeview", background="white", foreground=CORES['text'], fieldbackground="white", rowheight=32, font=FONTES['body'], borderwidth=0)
        style.map('Treeview', background=[('selected', CORES['select_row'])], foreground=[('selected', 'black')])
        style.configure("Treeview.Heading", font=FONTES['h2'], background=CORES['header_table'], foreground="white", relief="flat")
        style.configure("TNotebook", background=CORES['bg_app'], borderwidth=0)
        style.configure("TNotebook.Tab", padding=[15, 8], font=FONTES['h2'], background="#E0E0E0", foreground=CORES['text_light'])
        style.map("TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", CORES['primary'])])

    def carregar_categorias(self):
        cats = self.dao.listar_categorias()
        self.categorias_map = {nome: id_cat for id_cat, nome in cats}

    # --- DASHBOARD ---
    def setup_dashboard(self):
        self.dash_frame = tk.Frame(self.root, bg="white", height=120)
        self.dash_frame.pack(fill="x", side="top")
        tk.Frame(self.dash_frame, bg="#BDC3C7", height=1).pack(side="bottom", fill="x")
        
        # A linha abaixo causou o erro anteriormente
        container = tk.Frame(self.dash_frame, bg="white")
        container.pack(pady=15, padx=30, fill="x")
        
        self.card_total = self.create_card(container, "📦 ESTOQUE", "0", "#3498DB", 0)
        self.card_invest = self.create_card(container, "💰 INVESTIMENTO (TOTAL)", "R$ 0,00", "#E67E22", 1)
        self.card_venda = self.create_card(container, "📈 PREVISÃO FATURAMENTO", "R$ 0,00", "#9B59B6", 2)
        self.card_lucro = self.create_card(container, "💵 LUCRO PROJETADO", "R$ 0,00", "#2ECC71", 3)
        for i in range(4): container.grid_columnconfigure(i, weight=1)

    def create_card(self, parent, title, value, accent_color, col):
        frame = tk.Frame(parent, bg="white", highlightbackground="#ECF0F1", highlightthickness=1)
        frame.grid(row=0, column=col, padx=10, sticky="ew")
        tk.Frame(frame, bg=accent_color, width=4).pack(side="left", fill="y")
        content = tk.Frame(frame, bg="white", padx=15, pady=10)
        content.pack(side="left", fill="both", expand=True)
        tk.Label(content, text=title, bg="white", fg=CORES['text_light'], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        lbl_val = tk.Label(content, text=value, bg="white", fg=CORES['text'], font=FONTES['numbers'])
        lbl_val.pack(anchor="w", pady=(5,0))
        return lbl_val

    def update_dashboard(self):
        count, total_invest, venda = self.dao.get_dashboard_stats()
        lucro = venda - total_invest
        self.card_total.config(text=f"{count} Motos")
        self.card_invest.config(text=f"R$ {total_invest:,.2f}")
        self.card_venda.config(text=f"R$ {venda:,.2f}")
        self.card_lucro.config(text=f"R$ {lucro:,.2f}", fg=CORES['success'] if lucro >= 0 else CORES['danger'])

    # --- ABA 1: ESTOQUE ---
    def setup_tab_estoque(self):
        panel = ttk.Frame(self.tab_estoque, padding="20")
        panel.pack(fill="both", expand=True)

        lbl_frame = ttk.LabelFrame(panel, text=" 📝 DADOS DA MOTO ", padding="15")
        lbl_frame.pack(fill="x", pady=(0, 20))

        self.create_input(lbl_frame, "Modelo/Nome:", self.nome_text, 0, 0, 2)
        self.create_input(lbl_frame, "Ano Fab.:", self.ano_text, 0, 2)
        self.create_input(lbl_frame, "Placa:", self.placa_text, 0, 3)
        
        self.create_input(lbl_frame, "Valor Compra (R$):", self.valor_compra_text, 1, 0)
        self.create_input(lbl_frame, "Valor Venda (R$):", self.valor_venda_text, 1, 1)
        
        f_cat = ttk.Frame(lbl_frame)
        f_cat.grid(row=1, column=2, sticky='ew', padx=10, pady=5)
        ttk.Label(f_cat, text="Categoria:", font=FONTES['label'], foreground='#555').pack(anchor='w')
        self.combo_categoria_form = ttk.Combobox(f_cat, textvariable=self.categoria_text, state="readonly")
        self.combo_categoria_form.pack(fill='x', pady=(2,0))
        
        self.create_input(lbl_frame, "Cor:", self.cor_text, 1, 3)

        self.create_input(lbl_frame, "KM Atual:", self.km_text, 2, 0)
        self.create_input(lbl_frame, "Antigo Dono:", self.antigo_dono_text, 2, 1)
        
        f_status = ttk.Frame(lbl_frame)
        f_status.grid(row=2, column=2, columnspan=2, sticky='ew', padx=10, pady=5)
        ttk.Label(f_status, text="Status Atual:", font=FONTES['label'], foreground='#555').pack(anchor='w')
        ttk.Combobox(f_status, textvariable=self.status_text, values=["Em Estoque", "Vendido", "Oficina"], state="readonly").pack(fill='x', pady=(2,0))

        for i in range(4): lbl_frame.columnconfigure(i, weight=1)

        btn_frame = ttk.Frame(panel)
        btn_frame.pack(fill="x", pady=(0, 20))
        ttk.Button(btn_frame, text="✅ SALVAR MOTO", command=self.add_record, style='Success.TButton', width=20).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 ATUALIZAR", command=self.update_record, style='Primary.TButton').pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🧹 LIMPAR", command=self.clear_fields).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ EXCLUIR", command=self.delete_record, style='Danger.TButton').pack(side="right")

        tree_frame = ttk.Frame(panel)
        tree_frame.pack(fill="both", expand=True)
        cols = ('id', 'nome', 'cat', 'ano', 'invest', 'venda', 'placa', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse')
        
        headers = [('id', '#', 40), ('nome', 'MODELO', 200), ('cat', 'CATEGORIA', 100), 
                   ('ano', 'ANO', 70), ('invest', 'INVEST. (R$)', 110), ('venda', 'VENDA (R$)', 110), 
                   ('placa', 'PLACA', 90), ('status', 'STATUS', 100)]
        
        for c, t, w in headers:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w)
            
        self.tree.pack(fill="both", expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.get_selected_row)

    def create_input(self, parent, label, var, r, c, colspan=1):
        container = ttk.Frame(parent)
        container.grid(row=r, column=c, columnspan=colspan, sticky='ew', padx=10, pady=5)
        ttk.Label(container, text=label, font=FONTES['label'], foreground='#555').pack(anchor='w')
        ttk.Entry(container, textvariable=var).pack(fill='x', pady=(2, 0))

    # --- ABA 2: GASTOS ---
    def setup_tab_gastos(self):
        main_frame = ttk.Frame(self.tab_gastos, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        left_frame = ttk.LabelFrame(main_frame, text=" REGISTRAR DESPESA ", padding="20")
        left_frame.pack(side="left", fill="both", expand=False, padx=(0, 15), ipadx=10)
        
        c_moto = ttk.Frame(left_frame)
        c_moto.pack(fill='x', pady=(0, 15))
        ttk.Label(c_moto, text="1. Selecione a Moto:", font=FONTES['label'], foreground='#555').pack(anchor='w')
        self.combo_motos = ttk.Combobox(c_moto, textvariable=self.gasto_moto_selecionada, state="readonly")
        self.combo_motos.pack(fill='x', pady=(2, 0))

        self.create_input_simple(left_frame, "2. Descrição:", self.gasto_descricao)
        self.create_input_simple(left_frame, "3. Valor (R$):", self.gasto_valor)
        
        ttk.Button(left_frame, text="💾 LANÇAR GASTO", command=self.save_expense, style='Primary.TButton').pack(fill="x", pady=20)
        
        right_frame = ttk.LabelFrame(main_frame, text=" HISTÓRICO ", padding="10")
        right_frame.pack(side="right", fill="both", expand=True)
        
        cols = ('id', 'moto', 'desc', 'valor', 'data')
        self.tree_gastos = ttk.Treeview(right_frame, columns=cols, show='headings')
        for c in cols: self.tree_gastos.heading(c, text=c.upper()); self.tree_gastos.column(c, width=100)
        self.tree_gastos.pack(fill="both", expand=True)
        self.view_expenses()

    def create_input_simple(self, parent, label, var):
        c = ttk.Frame(parent); c.pack(fill='x', pady=(0, 15))
        ttk.Label(c, text=label, font=FONTES['label'], foreground='#555').pack(anchor='w')
        ttk.Entry(c, textvariable=var).pack(fill='x', pady=(2, 0))

  # --- SUBSTITUA O MÉTODO setup_tab_relatorios POR ESTE ---
    def setup_tab_relatorios(self):
        frame = ttk.Frame(self.tab_relatorios, padding="20")
        frame.pack(fill="both", expand=True)
        
        # 1. Área de Busca (Topo)
        frm_busca = ttk.LabelFrame(frame, text=" 🔍 Busca Inteligente (Filtro SQL) ", padding=15)
        frm_busca.pack(fill="x", pady=(0, 15))
        
        ttk.Label(frm_busca, text="Digite Modelo ou Placa:", font=FONTES['label']).pack(side="left", padx=(0,10))
        ttk.Entry(frm_busca, textvariable=self.busca_var, width=40).pack(side="left", padx=5)
        ttk.Button(frm_busca, text="🔎 BUSCAR AGORA", command=self.executar_busca, style='Primary.TButton').pack(side="left", padx=10)

        # 2. Botões de Consultas (Meio)
        btn_box = ttk.LabelFrame(frame, text=" 📊 Selecione um Relatório Complexo (Etapa 5) ", padding=15)
        btn_box.pack(fill='x', pady=(0, 15))
        
        grid_frm = tk.Frame(btn_box, bg=CORES['bg_app'])
        grid_frm.pack(fill='x')

        # Botões grandes e claros
        b1 = ttk.Button(grid_frm, text="📑 Detalhes Completos\n(3 Tabelas JOIN)", command=self.rel_3_tabelas, width=25)
        b1.grid(row=0, column=0, padx=10, pady=5)
        
        b2 = ttk.Button(grid_frm, text="💰 Motos Acima da Média\n(Subquery SQL)", command=self.rel_subquery, width=25)
        b2.grid(row=0, column=1, padx=10, pady=5)
        
        b3 = ttk.Button(grid_frm, text="📈 Lucro por Categoria\n(Group By + AVG)", command=self.rel_agregacao, width=25)
        b3.grid(row=0, column=2, padx=10, pady=5)
        
        b4 = ttk.Button(grid_frm, text="⭐ Categorias Premium\n(Cláusula IN)", command=self.rel_multiset, width=25)
        b4.grid(row=0, column=3, padx=10, pady=5)
        
        # Centralizar botões
        for i in range(4): grid_frm.columnconfigure(i, weight=1)

        # 3. Área de Resultado (Tabela Dinâmica ao invés de Texto)
        res_frame = ttk.LabelFrame(frame, text=" Resultados da Consulta ", padding=10)
        res_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(res_frame)
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(res_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        # Treeview Dinâmica (Sem colunas definidas inicialmente)
        self.tree_relatorios = ttk.Treeview(res_frame, show='headings', 
                                            yscrollcommand=scroll_y.set, 
                                            xscrollcommand=scroll_x.set)
        self.tree_relatorios.pack(fill="both", expand=True)
        
        scroll_y.config(command=self.tree_relatorios.yview)
        scroll_x.config(command=self.tree_relatorios.xview)

    # --- SUBSTITUA O MÉTODO _exibir_resultado POR ESTE ---
    def _exibir_resultado(self, titulo, colunas, dados):
        # Limpa a tabela atual
        self.tree_relatorios.delete(*self.tree_relatorios.get_children())
        
        # Redefine as colunas dinamicamente baseadas na consulta
        self.tree_relatorios['columns'] = colunas
        
        # Configura os cabeçalhos
        for col in colunas:
            self.tree_relatorios.heading(col, text=col.upper())
            # Ajusta largura: Descrição e Moto ficam maiores, o resto menor
            width = 300 if col in ['Descrição', 'Moto', 'Modelo'] else 120
            self.tree_relatorios.column(col, width=width, anchor="center")
            
        # Insere os dados
        if not dados:
            messagebox.showinfo("Aviso", "Nenhum registro encontrado para esta consulta.")
            return

        for row in dados:
            valores_formatados = []
            for item in row:
                # Formata Moeda se for float
                if isinstance(item, float):
                    valores_formatados.append(f"R$ {item:,.2f}")
                else:
                    valores_formatados.append(item)
            
            self.tree_relatorios.insert('', 'end', values=valores_formatados)

    def rel_3_tabelas(self):
        dados = self.dao.relatorio_gastos_detalhado()
        cols = ["Data", "Categoria", "Moto", "Descrição", "Valor (R$)"]
        self._exibir_resultado("GASTOS DETALHADOS", cols, dados)

    def rel_subquery(self):
        dados = self.dao.motos_acima_media_preco()
        cols = ["Modelo", "Venda (R$)", "Categoria"]
        self._exibir_resultado("MOTOS ACIMA DA MÉDIA", cols, dados)

    def rel_agregacao(self):
        dados = self.dao.relatorio_lucro_categorias()
        cols = ["Categoria", "Qtd", "Lucro Médio"]
        self._exibir_resultado("LUCRO POR CATEGORIA", cols, dados)

    def rel_multiset(self):
        dados = self.dao.relatorio_motos_categorias_premium()
        cols = ["Modelo", "Categoria", "Venda (R$)"]
        self._exibir_resultado("MOTOS PREMIUM (IN)", cols, dados)

    def executar_busca(self):
        dados = self.dao.buscar_motos_por_termo(self.busca_var.get())
        cols = ["ID", "Modelo", "Placa", "Venda (R$)"]
        self._exibir_resultado("RESULTADO DA BUSCA", cols, dados)

    # --- FUNÇÕES AUXILIARES ---
    def view_records(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in self.dao.listar_motos_completas():
            l = list(row)
            l[3] = f"R$ {l[3]:.2f}" if l[3] is not None else "R$ 0.00"
            l[4] = f"R$ {l[4]:.2f}" if l[4] is not None else "-"
            self.tree.insert('', 'end', values=l)
        self.carregar_categorias()
        self.combo_categoria_form['values'] = list(self.categorias_map.keys())
        motos = self.dao.listar_motos_completas()
        self.combo_motos['values'] = [f"{m[0]} - {m[1]}" for m in motos]

    def add_record(self):
        try:
            cat_nome = self.categoria_text.get()
            cat_id = self.categorias_map.get(cat_nome)
            if not cat_id:
                messagebox.showerror("Erro", "Selecione uma Categoria válida!")
                return
            dados = (
                self.nome_text.get(), self.ano_text.get(), self.valor_compra_text.get(),
                self.valor_venda_text.get(), self.antigo_dono_text.get(), self.status_text.get(),
                self.placa_text.get(), self.km_text.get(), self.cor_text.get(), cat_id
            )
            self.dao.inserir_moto(dados)
            self.clear_fields(); self.view_records(); self.update_dashboard()
            messagebox.showinfo("Sucesso", "Moto adicionada!")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def update_record(self):
        if not self.selected_id: return
        try:
            cat_id = self.categorias_map.get(self.categoria_text.get())
            dados = (
                self.nome_text.get(), self.ano_text.get(), self.valor_compra_text.get(),
                self.valor_venda_text.get(), self.antigo_dono_text.get(), self.status_text.get(),
                self.placa_text.get(), self.km_text.get(), self.cor_text.get(), cat_id
            )
            self.dao.atualizar_moto(dados, self.selected_id)
            self.view_records(); self.clear_fields(); self.update_dashboard()
            messagebox.showinfo("Sucesso", "Atualizado!")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def delete_record(self):
        if self.selected_id and messagebox.askyesno("Confirmar", "Excluir?"):
            self.dao.deletar_moto(self.selected_id)
            self.clear_fields(); self.view_records(); self.update_dashboard()

    def save_expense(self):
        try:
            moto_str = self.gasto_moto_selecionada.get()
            if not moto_str:
                messagebox.showerror("Erro", "Selecione uma moto!")
                return
            moto_id = int(moto_str.split(' - ')[0])
            val = float(self.gasto_valor.get())
            dt = datetime.now().strftime("%d/%m/%Y")
            self.dao.inserir_gasto(moto_id, self.gasto_descricao.get(), val, dt)
            self.gasto_valor.set(""); self.gasto_descricao.set("")
            self.view_expenses(); self.view_records(); self.update_dashboard()
            messagebox.showinfo("Sucesso", "Gasto lançado!")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def view_expenses(self):
        for i in self.tree_gastos.get_children(): self.tree_gastos.delete(i)
        for row in self.dao.listar_todos_gastos_com_nomes():
            self.tree_gastos.insert('', 'end', values=row)

    def get_selected_row(self, event):
        sel = self.tree.selection()
        if not sel: return
        iid = self.tree.item(sel[0], 'values')[0]
        self.selected_id = iid
        moto = self.dao.buscar_moto_por_id(iid)
        if moto:
            self.nome_text.set(moto[1]); self.ano_text.set(moto[2])
            self.valor_compra_text.set(moto[3]); self.valor_venda_text.set(moto[4])
            self.antigo_dono_text.set(moto[5]); self.status_text.set(moto[6])
            self.placa_text.set(moto[7]); self.km_text.set(moto[8]); self.cor_text.set(moto[9])
            cat_id = moto[10]
            for nome, cid in self.categorias_map.items():
                if cid == cat_id:
                    self.categoria_text.set(nome)
                    break

    def clear_fields(self):
        for var in [self.nome_text, self.ano_text, self.valor_compra_text, self.valor_venda_text, 
                    self.antigo_dono_text, self.placa_text, self.km_text, self.cor_text, self.categoria_text]: var.set("")
        self.selected_id = None