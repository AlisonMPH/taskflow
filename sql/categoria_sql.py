SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT
    )
"""

SQL_INSERIR = """
    INSERT INTO categoria (nome, descricao)
    VALUES (?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, descricao
    FROM categoria
    ORDER BY nome ASC
"""

SQL_ALTERAR = """
    UPDATE categoria
    SET nome=?, descricao=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM categoria
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, nome, descricao
    FROM categoria
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM CATEGORIA 
"""