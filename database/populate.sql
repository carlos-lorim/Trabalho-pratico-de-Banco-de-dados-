-- Limpar dados antigos (opcional, para evitar duplicatas se rodar de novo)
DELETE FROM gastos;
DELETE FROM motos;
DELETE FROM categorias;
DELETE FROM sqlite_sequence;

-- 1. Inserir Categorias (5 registros)
INSERT INTO categorias (nome) VALUES ('Street');
INSERT INTO categorias (nome) VALUES ('Sport');
INSERT INTO categorias (nome) VALUES ('Custom');
INSERT INTO categorias (nome) VALUES ('Off-Road');
INSERT INTO categorias (nome) VALUES ('Scooter');
INSERT INTO categorias (nome) VALUES ('Touring');

-- 2. Inserir Motos (Mínimo 10)
INSERT INTO motos (nome, ano, valor_compra, valor_venda, antigo_dono, status, placa, km, cor, categoria_id) VALUES 
('Honda CG 160', 2022, 12000, 15000, 'João Silva', 'Em Estoque', 'ABC-1234', 15000, 'Vermelha', 1),
('Yamaha MT-07', 2020, 35000, 42000, 'Maria Souza', 'Em Estoque', 'XYZ-9876', 8000, 'Azul', 2),
('Harley Iron 883', 2019, 45000, 52000, 'Roberto Carlos', 'Vendido', 'HAR-1903', 12000, 'Preta', 3),
('Honda Biz 125', 2023, 14000, 16500, 'Ana Paula', 'Em Estoque', 'BIZ-2023', 2000, 'Branca', 5),
('BMW GS 1250', 2021, 85000, 98000, 'Dr. Pedro', 'Oficina', 'ADV-1250', 25000, 'Cinza', 6),
('Kawasaki Ninja 400', 2022, 28000, 34000, 'Lucas Mendes', 'Em Estoque', 'KAW-0400', 5000, 'Verde', 2),
('Triumph Tiger 900', 2021, 58000, 65000, 'Fernanda Lima', 'Em Estoque', 'TRI-0900', 18000, 'Branca', 6),
('Yamaha XTZ 250 Lander', 2023, 23000, 26000, 'Claudio T.', 'Em Estoque', 'XTZ-0250', 1000, 'Azul', 4),
('Honda CB 500X', 2018, 30000, 36000, 'Juliana R.', 'Vendido', 'CBX-5000', 32000, 'Vermelha', 6),
('Royal Enfield Meteor', 2022, 24000, 28000, 'Marcos P.', 'Em Estoque', 'ROY-0350', 4500, 'Marrom', 3),
('Suzuki Haojue 150', 2024, 11000, 14000, 'Loja A', 'Em Estoque', 'SUZ-0150', 0, 'Preta', 1);

-- 3. Inserir Gastos (Mínimo 10 - vinculados às motos acima)
-- IDs das motos dependem da ordem de inserção (1 a 11)
INSERT INTO gastos (moto_id, descricao, valor, data) VALUES 
(1, 'Troca de Óleo', 150.00, '15/11/2025'),
(1, 'Retrovisor Novo', 80.00, '16/11/2025'),
(2, 'Pneu Traseiro Pirelli', 1200.00, '10/11/2025'),
(3, 'Polimento e Detalhe', 350.00, '01/11/2025'),
(5, 'Revisão Geral Motor', 2500.00, '20/11/2025'),
(5, 'Pastilha de Freio', 400.00, '20/11/2025'),
(6, 'Slider de Proteção', 600.00, '18/11/2025'),
(7, 'Instalação de Baú', 1500.00, '12/11/2025'),
(8, 'Lavagem Especial', 50.00, '19/11/2025'),
(10, 'Troca de Bateria', 450.00, '14/11/2025'),
(2, 'Manopla Esportiva', 120.00, '11/11/2025');