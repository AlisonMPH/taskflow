from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from dtos.alterar_cliente_dto import AlterarClienteDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from models.cliente_model import Cliente
from models.tarefa_model import Tarefa
from repositories.cliente_repo import ClienteRepo
from util.auth import checar_autorizacao, conferir_senha, obter_cliente_logado, obter_hash_senha
from util.cookies import (
    adicionar_mensagem_erro,
    adicionar_mensagem_sucesso,
    excluir_cookie_auth,
)


router = APIRouter(prefix="/cliente")

templates = Jinja2Templates(directory="templates")


@router.get("/pedidos")
async def get_pedidos(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse(
        "pedidos.html",
        {"request": request},
    )


@router.get("/dados")
async def get_dados(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse(
        "dados_cliente.html",
        {"request": request},
    )


@router.post("/post_dados", response_class=JSONResponse)
async def post_dados(request: Request, alterar_dto: AlterarClienteDTO):
    checar_autorizacao(request)
    id = request.state.cliente.id
    cliente_data = alterar_dto.model_dump()
    response = JSONResponse({"redirect": {"url": "/cliente/dados"}})
    if ClienteRepo.alterar(Cliente(id, **cliente_data)):
        adicionar_mensagem_sucesso(response, "Dados alterados com sucesso!")
    else:
        adicionar_mensagem_erro(
            response, "Não foi possível alterar os dados cadastrais!"
        )
    return response


@router.get("/senha")
async def get_senha(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse(
        "senha_cliente.html",
        {"request": request},
    )


@router.post("/post_senha", response_class=JSONResponse)
async def post_senha(request: Request, alterar_dto: AlterarSenhaDTO):
    checar_autorizacao(request)
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


@router.get("/carrinho")
async def get_carrinho(request: Request):
    checar_autorizacao(request)
    return templates.TemplateResponse(
        "carrinho.html",
        {"request": request},
    )


@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request):
    checar_autorizacao(request)
    if request.state.cliente:
        ClienteRepo.alterar_token(request.state.cliente.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    excluir_cookie_auth(response)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso.")
    return response

@router.get("/cliente/{id_cliente}/tarefa", response_model=list[Tarefa])
def buscar_tarefas_cliente(
    id_cliente: int = 11, #Path(..., title="ID do Cliente"),
    cliente_logado: Cliente = Depends(obter_cliente_logado),  # Exemplo de autenticação de cliente
):
    if (cliente_logado):
        tarefas = ClienteRepo.obter_tarefas_por_cliente(id_cliente)
    if not tarefas:
        raise HTTPException(status_code=404, detail=f"Tarefas do cliente {id_cliente} não encontradas")
    return tarefas