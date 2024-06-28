from datetime import datetime
from http.client import HTTPResponse
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from dtos.alterar_cliente_dto import AlterarClienteDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from dtos.nova_tarefa_dto import NovaTarefaDTO
from models.cliente_model import Cliente
from models.tarefa_model import Tarefa
from repositories.categoria_repo import CategoriaRepo
from repositories.cliente_repo import ClienteRepo
from repositories.tarefa_repo import TarefaRepo
from util.auth import conferir_senha, obter_hash_senha
from util.cookies import (
    adicionar_mensagem_alerta,
    adicionar_mensagem_erro,
    adicionar_mensagem_sucesso,
    excluir_cookie_auth,
)
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/cliente")
templates = obter_jinja_templates("templates/cliente")

@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(
        "pages/sobre.html",
        {
            "request": request,
        },
    )
    
@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro.html",
        {
            "request": request,
        },
    )

@router.get("/tarefas", response_class=HTMLResponse)
async def listar_tarefas(request: Request):
    id_cliente = request.state.cliente.id
    tarefas = TarefaRepo.obter_tarefas_do_cliente(id_cliente)
    return templates.TemplateResponse(
        "pages/tarefa.html",
        {
            "request": request,
            "tarefas": tarefas,
        },
    )

@router.get("/nova_tarefa", response_class=HTMLResponse)
async def nova_tarefa(request: Request):
    categorias = CategoriaRepo.obter_todos()
    return templates.TemplateResponse(
        "pages/nova_tarefa.html",
        {
            "request": request,
            "categorias": categorias,
        },
    )

@router.get("/tarefas/{id}/alterar", response_class=HTMLResponse)
async def alterar_tarefa(request: Request, id: int):
    categorias = CategoriaRepo.obter_todos()
    tarefa = TarefaRepo.obter_tarefa_por_id(id)
    if not tarefa:
        return HTTPResponse(status_code=404)

    return templates.TemplateResponse(
        "pages/alterar_tarefa.html",
        {
            "request": request,
            "categorias": categorias,
            "tarefa": tarefa,
        },
    )

@router.post("/tarefas/{id}/alterar", response_class=HTMLResponse)
async def alterar_tarefa(request: Request, id: int, titulo: str = Form(...), descricao: str = Form(...), data_vencimento: str = Form(...), id_categoria: int = Form(...)):
    tarefa = TarefaRepo.obter_tarefa_por_id(id)
    if not tarefa:
        return HTMLResponse(status_code=404)

    tarefa_atualizada = Tarefa(
        id=id,
        titulo=titulo,
        descricao=descricao,
        data_vencimento=data_vencimento,
        id_categoria=id_categoria
    )
    
    if TarefaRepo.alterar_tarefa(tarefa_atualizada):
        response = RedirectResponse("/cliente/tarefas", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Tarefa alterada com sucesso!")
    else:
        response = JSONResponse(status_code=500, content={"error": "Não foi possível alterar a tarefa."})
        
    return response

@router.delete("/excluir_tarefa/{id}")
async def excluir_tarefa(id: int):
    if TarefaRepo.excluir(id):
        response = RedirectResponse("/cliente/tarefas", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Tarefa excluida com sucesso!")
    else:
        response = JSONResponse(status_code=500, content={"error": "Não foi possível excluir a tarefa."})
        
    return response

@router.post("/post_nova_tarefa")
async def criar_tarefa(request: Request):
    form = await request.form()
    titulo = form.get("titulo")
    descricao = form.get("descricao")
    data_vencimento = form.get("data_vencimento")
    id_categoria = form.get("id_categoria")
    id_cliente = request.state.cliente.id 

    nova_tarefa = Tarefa(
        titulo=titulo,
        descricao=descricao,
        data_vencimento=data_vencimento,
        id_categoria=id_categoria,
        id_cliente=id_cliente
    )
    if TarefaRepo.inserir(nova_tarefa):
        response = RedirectResponse("/cliente/tarefas", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Tarefa criada com sucesso!")
    else:
        response = JSONResponse(status_code=500, content={"error": "Não foi possível criar a tarefa."})

    return response

@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(request: Request, alterar_dto: AlterarClienteDTO):
    id = request.state.cliente.id
    cliente_data = alterar_dto.model_dump()
    response = JSONResponse({"redirect": {"url": "/cliente/cadastro"}})
    if ClienteRepo.alterar(Cliente(id, **cliente_data)):
        adicionar_mensagem_sucesso(response, "Cadastro alterado com sucesso!")
    else:
        adicionar_mensagem_erro(
            response, "Não foi possível alterar os dados cadastrais!"
        )
    return response


@router.get("/senha")
async def get_senha(request: Request):
    return templates.TemplateResponse(
        "pages/senha.html",
        {"request": request},
    )


@router.post("/post_senha", response_class=JSONResponse)
async def post_senha(request: Request, alterar_dto: AlterarSenhaDTO):
    email = request.state.cliente.email
    cliente_bd = ClienteRepo.obter_por_email(email)
    nova_senha_hash = obter_hash_senha(alterar_dto.nova_senha)
    response = JSONResponse({"redirect": {"url": "/cliente/senha"}})
    if not conferir_senha(alterar_dto.senha, cliente_bd.senha):
        adicionar_mensagem_erro(response, "Senha atual incorreta!")
        return response
    if ClienteRepo.alterar_senha(cliente_bd.id, nova_senha_hash):
        adicionar_mensagem_sucesso(response, "Senha alterada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar sua senha!")
    return response


@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request):
    if request.state.cliente:
        ClienteRepo.alterar_token(request.state.cliente.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    excluir_cookie_auth(response)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso!")
    return response
