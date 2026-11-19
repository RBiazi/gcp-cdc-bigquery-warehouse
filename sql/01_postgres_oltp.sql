CREATE TABLE IF NOT EXISTS clientes (
    cliente_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cidade VARCHAR(60),
    estado CHAR(2),
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS produtos (
    produto_id SERIAL PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    preco_unitario NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    produto_id INT REFERENCES produtos(produto_id),
    quantidade INT NOT NULL,
    valor_total NUMERIC(10, 2) NOT NULL,
    status_pedido VARCHAR(20) DEFAULT 'APROVADO',
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO clientes (nome, email, cidade, estado) VALUES
('Ana Silva', 'ana@email.com', 'São Paulo', 'SP'),
('Carlos Souza', 'carlos@email.com', 'Jundiaí', 'SP'),
('Mariana Costa', 'mariana@email.com', 'Curitiba', 'PR')
ON CONFLICT (email) DO NOTHING;

INSERT INTO produtos (nome_produto, categoria, preco_unitario) VALUES
('Notebook Pro 15', 'Eletrônicos', 5500.00),
('Monitor Ultrawide 29', 'Periféricos', 1400.00),
('Teclado Mecânico', 'Periféricos', 450.00);

INSERT INTO pedidos (cliente_id, produto_id, quantidade, valor_total, status_pedido) VALUES
(1, 1, 1, 5500.00, 'APROVADO'),
(2, 2, 2, 2800.00, 'APROVADO'),
(3, 3, 1, 450.00, 'PENDENTE');
