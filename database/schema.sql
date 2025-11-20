-- Tabela de Categorias (Necessária para cumprir regra de 3 tabelas)
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

-- Tabela de Motos
CREATE TABLE IF NOT EXISTS motos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    ano INTEGER,
    valor_compra REAL,
    valor_venda REAL,
    antigo_dono TEXT,
    status TEXT,
    placa TEXT,
    km INTEGER,
    cor TEXT,
    categoria_id INTEGER,
    FOREIGN KEY(categoria_id) REFERENCES categorias(id)
);

-- Tabela de Gastos
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moto_id INTEGER,
    descricao TEXT,
    valor REAL,
    data TEXT,
    FOREIGN KEY(moto_id) REFERENCES motos(id) ON DELETE CASCADE
);