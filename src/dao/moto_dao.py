from database.db_connection import get_connection

class MotoDAO:
    def __init__(self):
        pass

    def listar_categorias(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM categorias")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def inserir_moto(self, dados):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO motos (nome, ano, valor_compra, valor_venda, antigo_dono, status, placa, km, cor, categoria_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        conn.commit()
        conn.close()

    def listar_motos_completas(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT 
                m.id, m.nome, m.ano, 
                (m.valor_compra + COALESCE((SELECT SUM(valor) FROM gastos WHERE moto_id = m.id), 0)) as investimento_total,
                m.valor_venda, m.placa, m.status,
                c.nome as categoria_nome
            FROM motos m
            LEFT JOIN categorias c ON m.categoria_id = c.id
            ORDER BY m.id DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def buscar_moto_por_id(self, id_moto):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motos WHERE id=?", (id_moto,))
        moto = cursor.fetchone()
        conn.close()
        return moto

    def atualizar_moto(self, dados, id_moto):
        conn = get_connection()
        cursor = conn.cursor()
        dados_lista = list(dados)
        dados_lista.append(id_moto)
        cursor.execute("""
            UPDATE motos SET 
            nome=?, ano=?, valor_compra=?, valor_venda=?, antigo_dono=?, 
            status=?, placa=?, km=?, cor=?, categoria_id=? 
            WHERE id=?
        """, dados_lista)
        conn.commit()
        conn.close()

    def deletar_moto(self, id_moto):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM motos WHERE id=?", (id_moto,))
        conn.commit()
        conn.close()

    def inserir_gasto(self, moto_id, descricao, valor, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gastos (moto_id, descricao, valor, data) VALUES (?, ?, ?, ?)", 
                       (moto_id, descricao, valor, data))
        conn.commit()
        conn.close()

    def listar_todos_gastos_com_nomes(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.id, m.nome, g.descricao, g.valor, g.data 
            FROM gastos g 
            JOIN motos m ON g.moto_id = m.id 
            ORDER BY g.id DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_dashboard_stats(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM motos WHERE status='Em Estoque'")
        count = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(valor_compra) FROM motos WHERE status='Em Estoque'")
        compra = cursor.fetchone()[0] or 0.0
        cursor.execute("SELECT SUM(g.valor) FROM gastos g JOIN motos m ON g.moto_id = m.id WHERE m.status='Em Estoque'")
        gastos = cursor.fetchone()[0] or 0.0
        total_invest = compra + gastos
        cursor.execute("SELECT SUM(valor_venda) FROM motos WHERE status='Em Estoque'")
        venda = cursor.fetchone()[0] or 0.0
        conn.close()
        return count, total_invest, venda

    # --- ETAPA 5: CONSULTAS COMPLEXAS PARA O TRABALHO ---
    
    def relatorio_gastos_detalhado(self):
        # 1. Junção de 3 tabelas
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT g.data, c.nome, m.nome, g.descricao, g.valor
            FROM gastos g
            JOIN motos m ON g.moto_id = m.id
            JOIN categorias c ON m.categoria_id = c.id
            ORDER BY g.data DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def motos_acima_media_preco(self):
        # 2. Subconsulta
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT m.nome, m.valor_venda, c.nome
            FROM motos m
            JOIN categorias c ON m.categoria_id = c.id
            WHERE m.valor_venda > (SELECT AVG(valor_venda) FROM motos)
            ORDER BY m.valor_venda DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def relatorio_lucro_categorias(self):
        # 3. Agregação (Group By)
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT c.nome, COUNT(m.id), AVG(m.valor_venda - m.valor_compra)
            FROM categorias c
            JOIN motos m ON m.categoria_id = c.id
            GROUP BY c.nome
            HAVING COUNT(m.id) >= 1
            ORDER BY 3 DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def buscar_motos_por_termo(self, termo):
        # 4. String Matching (LIKE) + Limit
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT id, nome, placa, valor_venda FROM motos WHERE nome LIKE ? OR placa LIKE ? LIMIT 10"
        termo_like = f"%{termo}%"
        cursor.execute(sql, (termo_like, termo_like))
        rows = cursor.fetchall()
        conn.close()
        return rows
        
    def relatorio_motos_categorias_premium(self):
        # 5. Multiset (IN)
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT m.nome, c.nome, m.valor_venda
            FROM motos m
            JOIN categorias c ON m.categoria_id = c.id
            WHERE c.nome IN ('Sport', 'Touring', 'Custom')
            ORDER BY m.valor_venda DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    def get_stats_categorias_grafico(self):
        """Retorna dados para o gráfico: Nome da Categoria e Qtd de Motos"""
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT c.nome, COUNT(m.id) 
            FROM categorias c
            LEFT JOIN motos m ON m.categoria_id = c.id
            GROUP BY c.nome
            HAVING COUNT(m.id) > 0
            ORDER BY COUNT(m.id) DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows