import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from dtos.entrar_dto import EntrarDTO
from ler_html import ler_html
from dtos.novo_cliente_dto import NovoClienteDTO
from models.cliente_model import Cliente
from repositories.cliente_repo import ClienteRepo
from repositories.produto_repo import ProdutoRepo
from util.auth import (
    checar_autorizacao,
    conferir_senha,
    gerar_token,
    obter_hash_senha,
)

from util.cookies import adicionar_cookie_auth, adicionar_mensagem_sucesso
from util.pydantic import create_validation_errors

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/html/{arquivo}")
async def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response


@router.get("/")
async def get_root(request: Request):
    produtos = ProdutoRepo.obter_todos()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "produtos": produtos},
    )


@router.get("/contato")
async def get_contato(request: Request):
    return templates.TemplateResponse(
        "contato.html",
        {"request": request},
    )


@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "cadastro.html",
        {"request": request},
    )


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(cliente_dto: NovoClienteDTO):
    # Remover campo `confirmacao_senha` antes de inserir no banco de dados
    cliente_data = cliente_dto.model_dump(exclude={"confirmacao_senha"})
    cliente_data["senha"] = obter_hash_senha(cliente_data["senha"])
    novo_cliente = ClienteRepo.inserir(Cliente(**cliente_data))
    if not novo_cliente or not novo_cliente.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente.")
    return {"redirect": {"url": "/cadastro_realizado"}}


@router.get("/cadastro_realizado")
async def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse(
        "cadastro_confirmado.html",
        {"request": request},
    )


@router.get("/entrar")
async def get_entrar(
    request: Request,
    return_url: str = Query("/"),
):
    return templates.TemplateResponse(
        "entrar.html",
        {"request": request, "return_url": return_url},
    )


@router.post("/post_entrar", response_class=JSONResponse)
async def post_entrar(entrar_dto: EntrarDTO):
    cliente_entrou = ClienteRepo.obter_por_email(entrar_dto.email)
    if (
        (not cliente_entrou)
        or (not cliente_entrou.senha)
        or (not conferir_senha(entrar_dto.senha, cliente_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                entrar_dto,
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    token = gerar_token()
    if not ClienteRepo.alterar_token(cliente_entrou.id, token):
        raise DatabaseError(
            "Não foi possível alterar o token do cliente no banco de dados."
        )
    response = JSONResponse(content={"redirect": {"url": entrar_dto.return_url}})
    adicionar_mensagem_sucesso(
        response,
        f"Olá, <b>{cliente_entrou.nome}</b>. Seja bem-vindo(a) à Loja Virtual!",
    )
    adicionar_cookie_auth(response, token)
    return response


@router.get("/produto/{id:int}")
async def get_produto(request: Request, id: int):
    produto = ProdutoRepo.obter_um(id)
    return templates.TemplateResponse(
        "produto.html",
        {"request": request, "produto": produto},
    )


@router.get("/buscar")
async def get_buscar(
    request: Request,
    q: str,
    p: int = 1,
    tp: int = 6,
    o: int = 1,
):
    produtos = ProdutoRepo.obter_busca(q, p, tp, o)
    qtde_produtos = ProdutoRepo.obter_quantidade_busca(q)
    qtde_paginas = math.ceil(qtde_produtos / float(tp))
    return templates.TemplateResponse(
        "buscar.html",
        {
            "request": request,
            "produtos": produtos,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "termo_busca": q,
            "ordem": o,
        },
    )
    
@router.get("/tarefa")
def get_tarefas(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse(
        "tarefa.html",
        {"request": request},
    )
    
@router.get("/nova_tarefa")
def get_tarefas(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse(
        "nova_tarefa.html",
        {"request": request},
    )
    
