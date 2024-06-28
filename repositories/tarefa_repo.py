import json
import sqlite3
from typing import List, Optional
from models.tarefa_model import Tarefa
from sql.tarefa_sql import *
from util.database import obter_conexao


class TarefaRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA_TAREFA)

    @classmethod
    def inserir(cls, tarefa: Tarefa) -> Optional[Tarefa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR_TAREFA,
                    (
                        tarefa.titulo,
                        tarefa.descricao,
                        tarefa.data_vencimento,
                        tarefa.id_categoria,
                        tarefa.id_cliente,
                    ),
                )
                if cursor.rowcount > 0:
                    tarefa.id = cursor.lastrowid
                    return tarefa
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_tarefas_json(cls, arquivo_json: str):
        if TarefaRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                tarefas = json.load(arquivo)
                for tarefa in tarefas:
                    TarefaRepo.inserir(Tarefa(**tarefa))
                    
    @classmethod
    def obter_tarefas_do_cliente(cls, id_cliente: int) -> List[Tarefa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TAREFAS_CLIENTE, (id_cliente,)).fetchall()
                tarefas = [Tarefa(*t) for t in tuplas]
                return tarefas
        except sqlite3.Error as ex:
            print(ex)
            return []


    @classmethod
    def alterar_tarefa(cls, tarefa: Tarefa) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ATUALIZAR_TAREFA,
                    (
                        tarefa.titulo,
                        tarefa.descricao,
                        tarefa.data_vencimento,
                        tarefa.id_categoria,
                        tarefa.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR_TAREFA, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
        
    @classmethod
    def obter_tarefa_por_id(cls, id: int) -> Optional[Tarefa]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM, (id,)).fetchone()
                if tupla:
                    tarefa = Tarefa(*tupla)
                    return tarefa
                return None
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
    def inserir_tarefas_json(cls, arquivo_json: str):
        if TarefaRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                tarefas = json.load(arquivo)
                for tarefa in tarefas:
                    TarefaRepo.inserir(Tarefa(**tarefa))
