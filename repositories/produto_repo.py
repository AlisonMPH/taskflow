import json
import sqlite3
from typing import List, Optional
from models.produto_model import Produto
from sql.produto_sql import *
from util.database import obter_conexao


class ProdutoRepo():

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, produto: Produto) -> Optional[Produto]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (
                    produto.nome,
                    produto.preco,
                    produto.descricao,
                    produto.estoque
                ))
                if cursor.rowcount > 0:
                    produto.id = cursor.lastrowid
                    return produto
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_todos(cls) -> List[Produto]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                produtos = [Produto(*t) for t in tuplas]
                return produtos
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def alterar(cls, produto: Produto) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR, (
                    produto.nome,
                    produto.preco,
                    produto.descricao,
                    produto.estoque,
                    produto.id
                ))
                return(cursor.rowcount > 0)
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return (cursor.rowcount > 0)
        except sqlite3.Error as ex:
            print(ex)
            return False
    
    @classmethod
    def obter_um(cls, id: int) -> Optional[Produto]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM, (id,)).fetchone()
                produto = Produto(*tupla)
                return produto
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def inserir_produtos_json(cls, arquivo_json: str):
        if ProdutoRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                produtos = json.load(arquivo)
                for produto in produtos:
                    ProdutoRepo.inserir(Produto(**produto))

    @classmethod
    def obter_busca(cls, termo: str, pagina: int, tamanho_pagina: int, ordem: int) -> List[Produto]:
        termo = "%"+termo+"%"
        offset = (pagina - 1) * tamanho_pagina
        match (ordem):
            case 1: SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "nome")
            case 2: SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "preco ASC")
            case 3: SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "preco DESC")
            case _: SQL_OBTER_BUSCA_ORDENADA = SQL_OBTER_BUSCA.replace("#1", "nome")
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_BUSCA_ORDENADA, (termo, termo, tamanho_pagina, offset)).fetchall()
                produtos = [Produto(*t) for t in tuplas]
                return produtos
        except sqlite3.Error as ex:
            print(ex)
            return None
        
    @classmethod
    def obter_quantidade_busca(cls, termo: str) -> Optional[int]:
        termo = "%"+termo+"%"
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE_BUSCA, (termo, termo)).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None