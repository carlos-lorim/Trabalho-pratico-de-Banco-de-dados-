
# MotoManager Pro 🚀

Sistema de gestão para revenda e oficina de motociclos, desenvolvido em Python e SQLite.
Focado em UX (User Experience) e Business Intelligence para cálculo de lucro real.

---

## 👥 Equipe de Desenvolvimento
Este projeto foi desenvolvido pelos acadêmicos:

* **João Pedro P. de Freitas**
* **Carlos Augusto R. Lorim**
* **João Victor R. G. Nunes**
* **Thalles Henrique R. G. Pereira**

---

## 📋 Requisitos do Sistema
Para executar este projeto, você precisará ter instalado:

* **Python 3.10** ou superior.
* **Biblioteca Matplotlib** (para geração dos gráficos no dashboard).

O **Tkinter** (interface gráfica) e o **SQLite3** (banco de dados) já são nativos do Python e não requerem instalação extra.

---

## ⚙️ Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/carlos-lorim/Trabalho-pratico-de-banco-de-dados-.git](https://github.com/carlos-lorim/Trabalho-pratico-de-banco-de-dados-.git)
   cd Trabalho-pratico-de-Banco-de-dados-
Instale as dependências: Abra o terminal na pasta do projeto e execute:

Bash

pip install matplotlib
(Caso use Linux/Mac, pode ser necessário usar pip3)

## ▶️ Como Executar
Para iniciar a aplicação, execute o arquivo principal na raiz do projeto:

Bash

python main.py
O sistema verificará automaticamente a existência do banco de dados. Se não encontrar, ele criará o arquivo motos_projeto_final.db e populará com dados iniciais de teste.

## 🔐 Acesso ao Sistema
Para acessar o Dashboard, utilize as credenciais padrão:

Usuário: admin

Senha: admin

### 📊 1. Dashboard Visual (BI)
Painel de controle estratégico para tomada de decisão rápida.
* **Gráfico em Tempo Real:** Mostra a distribuição da frota por categoria.
* **KPIs Financeiros:** Indicadores de *Investimento Total*, *Valor de Venda Previsto* e *Lucro Projetado*.

### 📦 2. Gestão de Estoque (CRUD)
Controle total sobre os veículos da loja.
* **Cadastro Completo:** Registra modelo, placa, ano, cor e valores.
* **Cálculo Automático:** O sistema soma o valor de compra com os gastos para sugerir o lucro real.
* **Visualização Clean:** Tabela com *Zebra Striping* (linhas alternadas) para facilitar a leitura.

### 💰 3. Controle Financeiro
Acompanhamento detalhado de onde o dinheiro está sendo gasto.
* **Lançamento de Despesas:** Adicione custos de peças, mecânica e taxas para cada moto individualmente.
* **Atualização de Custo:** Cada gasto lançado abate automaticamente da margem de lucro daquele veículo específico.

### 🔍 4. Consultas SQL Complexas (Relatórios)
Ferramentas avançadas de análise de dados exigidas no projeto.
* **📑 Relatório Detalhado (JOIN):** Cruza dados de 3 tabelas para um histórico completo.
* **📈 Análise de Preço (Subquery):** Filtra veículos acima da média de preço do estoque.
* **🏆 Lucratividade (Agregação):** Mostra qual categoria de moto dá mais lucro.
* **⭐ Filtro Premium (IN):** Seleciona apenas motos de categorias de alto padrão.
# 📘 Guia de Utilização - MotoManager Pro

Este guia descreve passo a passo como operar o sistema de gestão para revenda e oficina de motociclos.

---

## 1. 🔐 Tela de Login
Ao iniciar a aplicação, você será recebido pela tela de autenticação. O sistema possui uma conta administrativa padrão para fins acadêmicos.

* **Usuário:** `admin`
* **Senha:** `admin`
* **Ação:** Insira as credenciais e clique no botão **"ENTRAR"** para acessar o sistema.

---

## 2. 📈 Dashboard (Painel de Controle)
A tela inicial apresenta um **Dashboard em Tempo Real** na parte superior, oferecendo uma visão gerencial imediata do negócio.

* **Total Frota:** Quantidade de veículos atualmente com status *"Em Estoque"*.
* **Investido:** Soma total do valor de compra de todas as motos + todas as despesas lançadas (peças, serviços, taxas).
* **Lucro Estimado:** Cálculo automático: *(Valor de Venda Esperado - Custo Total)*.
    * *Indicador Visual:* Se o valor estiver em **Verde**, o lucro é positivo. Se estiver em **Vermelho**, há prejuízo projetado.
* **Gráfico de Categorias:** Visualização gráfica da distribuição do estoque por tipo de moto (ex: Street, Sport, Custom).

---

## 3. 📦 Aba "Estoque" (Gerenciamento de Veículos)
Nesta aba, você realiza o controle completo (CRUD) dos veículos da loja.

### Cadastrar Nova Moto
1.  Preencha o formulário com os dados da moto (Modelo, Ano, Placa, KM, Cor, etc.).
2.  Defina os valores financeiros:
    * **Compra (R$):** Quanto a loja pagou pelo veículo.
    * **Venda (R$):** Por quanto a loja pretende vender.
3.  Selecione a **Categoria** e o **Status** (ex: "Em Estoque").
4.  Clique no botão **"SALVAR NOVO"**.
    * *Resultado:* A moto aparecerá na tabela abaixo e os indicadores do Dashboard serão atualizados.

### Editar ou Excluir
1.  **Selecionar:** Clique em qualquer linha da tabela para carregar os dados no formulário.
2.  **Editar:** Modifique os campos necessários e clique em **"ATUALIZAR SELEÇÃO"**.
3.  **Remover:** Para apagar um registro permanentemente, clique em **"EXCLUIR"**.

---

## 4. 🛠️ Aba "Financeiro" (Controle de Gastos)
Esta funcionalidade é essencial para o cálculo do **Lucro Real**. Aqui são lançados todos os custos adicionais que reduzem a margem de lucro de um veículo.

### Lançar uma Despesa
1.  **Veículo:** Selecione a moto na lista suspensa (combo box).
2.  **Descrição:** Digite o motivo do gasto (ex: *"Troca de Óleo"*, *"Pneu Traseiro"*, *"Documentação"*).
3.  **Valor (R$):** Insira o custo do serviço/peça.
4.  Clique em **"CONFIRMAR LANÇAMENTO"**.

### Impacto no Sistema
* O gasto é salvo no histórico e vinculado à moto selecionada.
* O **Valor Investido** daquela moto aumenta automaticamente.
* O **Lucro Estimado** daquela moto diminui proporcionalmente no Dashboard.

---

## 5. 📊 Aba "BI & Relatórios" (Consultas Avançadas)
Área dedicada à inteligência de negócios e consultas SQL complexas.

### 🔍 Busca Inteligente
* **Como usar:** Digite parte do nome do modelo ou da placa no campo de busca e clique em **"BUSCAR"**.
* **Tecnologia:** Utiliza a cláusula SQL `LIKE` para encontrar correspondências parciais no banco de dados.

### 📑 Relatórios Gerenciais (Botões)

| Relatório | Descrição Técnica (SQL) | O que ele mostra? |
| :--- | :--- | :--- |
| **Gastos Detalhados** | **JOIN (3 Tabelas)** | Uma lista completa unindo dados de *Motos*, *Categorias* e *Gastos* para auditoria financeira. |
| **Motos de Alto Valor** | **Subquery** | Lista apenas os veículos cujo valor de venda é **superior à média** de preço de todo o estoque atual. |
| **Lucro por Categoria** | **Aggregation (GROUP BY)** | Mostra a média de lucro projetado agrupada por categoria, permitindo saber qual tipo de moto é mais rentável. |
| **Categorias Premium** | **Multiset (IN)** | Filtra e exibe apenas veículos pertencentes a categorias específicas de alto padrão (ex: Sport, Touring, Custom). |

## 📂 Estrutura do Projeto
Plaintext

Projeto/
│
├── main.py                   # Arquivo principal (Entry Point)
├── motos_projeto_final.db    # Banco de Dados SQLite (Gerado auto)
│
├── database/                 # Scripts SQL e Conexão
│   ├── db_connection.py
│   ├── schema.sql
│   └── populate.sql
│
└── src/                      # Código Fonte
    ├── dao/                  # Camada de Acesso a Dados
    │   └── moto_dao.py
    └── ui/                   # Interface Gráfica
        ├── main_window.py
        └── styles.py
