SQL_CRIAR_TABELA_TAREFA = """
    CREATE TABLE IF NOT EXISTS tarefa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data_vencimento DATETIME,
        id_categoria INTEGER,
        id_cliente INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id),
        FOREIGN KEY (id_cliente) REFERENCES cliente(id))
"""

SQL_INSERIR_TAREFA = """
    INSERT INTO tarefa(titulo, descricao, data_vencimento, id_categoria, id_cliente)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_TAREFAS_CLIENTE = """
    SELECT t.id, t.titulo, t.descricao, t.data_vencimento, c.nome AS nome_categoria
    FROM TAREFA t
    JOIN categoria c ON t.id_categoria = c.id
    WHERE t.id_cliente = ?
    ORDER BY t.data_vencimento ASC
"""

SQL_ATUALIZAR_TAREFA = """
    UPDATE TAREFA
    SET titulo = ?, descricao = ?, data_vencimento = ?, id_categoria = ?
    WHERE id = ? AND id_cliente = ?
"""

SQL_EXCLUIR_TAREFA = """
    DELETE FROM TAREFA
    WHERE id = ? AND id_cliente = ?
"""

SQL_OBTER_UM = """
    SELECT id, titulo, descricao, data_vencimento, id_categoria, id_cliente
    FROM TAREFA
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM TAREFA 
"""

SQL_OBTER_TAREFAS_POR_CLIENTE = """
    SELECT id, titulo, descricao, data_vencimento, id_cliente
    FROM tarefa
    WHERE id_cliente = ?
    ORDER BY data_vencimento DESC
"""
