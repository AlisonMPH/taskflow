SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS item_pedido (
        id_pedido INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        nome_produto TEXT NOT NULL,
        valor_produto FLOAT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_item = valor_produto * quantidade,
        PRIMARY KEY(id_pedido, id_produto),
        FOREIGN KEY id_pedido REFERENCES pedido(id),
        FOREIGN KEY id_produto REFERENCES produto(id))
"""

SQL_INSERIR = """
    INSERT INTO item_pedido(id_pedido, id_produto, nome_produto, valor_produto, quantidade)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_POR_PEDIDO = """
    SELECT id_pedido, id_produto, nome_produto, valor_produto, quantidade, valor_item
    FROM item_pedido
    WHERE id_pedido=?
    ORDER BY #1
"""

SQL_OBTER_QUANTIDADE_POR_PEDIDO_PRODUTO = """
    SELECT COUNT(*)
    FROM item_pedido
    WHERE id_pedido=? AND id_produto=?
"""

SQL_ALTERAR = """
    UPDATE item_pedido
    SET quantidade=?, valor_produto=?
    WHERE id_pedido=? AND id_produto=?
"""

SQL_EXCLUIR = """
    DELETE FROM item_pedido    
    WHERE id_pedido=? AND id_produto=?
"""

SQL_OBTER_QUANTIDADE_POR_PEDIDO = """
    SELECT COUNT(*) FROM item_pedido
    WHERE id_pedido=?
"""