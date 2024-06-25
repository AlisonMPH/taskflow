SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora DATETIME NOT NULL,
        valor_total FLOAT NOT NULL,
        endereco TEXT NOT NULL,
        estado INTEGER NOT NULL,
        id_cliente INTEGER,
        FOREIGN KEY id_cliente REFERENCES cliente(id))
"""

SQL_INSERIR = """
    INSERT INTO pedido(data_hora, valor_total, endereco, estado, id_cliente)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, data_hora, valor_total, endereco, estado, id_cliente, cliente.nome AS nome_cliente
    FROM pedido LEFT JOIN cliente ON id_cliente = cliente.id
    ORDER BY data_hora DESC
"""

SQL_ALTERAR = """
    UPDATE pedido
    SET data_hora=?, valor_total=?, endereco=?, estado=?, id_cliente=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM pedido    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, data_hora, valor_total, endereco, estado, id_cliente, cliente.nome AS nome_cliente
    FROM pedido LEFT JOIN cliente ON id_cliente = cliente.id
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM pedido
"""

SQL_OBTER_PERIODO = """
    SELECT id, data_hora, valor_total, endereco, estado, id_cliente, cliente.nome AS nome_cliente
    FROM pedido LEFT JOIN cliente ON id_cliente = cliente.id
    WHERE data_hora BETWEEN ? AND ?
    ORDER BY data_hora DESC
"""

SQL_OBTER_QUANTIDADE_PERIODO = """
    SELECT COUNT(*) FROM pedido
    WHERE data_hora BETWEEN ? AND ?
"""

SQL_OBTER_POR_CLIENTE = """
    SELECT id, data_hora, valor_total, endereco, estado
    FROM pedido
    WHERE (id_cliente = ?) AND (data_hora BETWEEN ? AND ?)
    ORDER BY id DESC
"""