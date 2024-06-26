from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.categoria_repo import CategoriaRepo
from repositories.cliente_repo import ClienteRepo
from repositories.tarefa_repo import TarefaRepo
from routes import main_routes, cliente_routes
from util.auth import checar_permissao, middleware_autenticacao
from util.exceptions import configurar_excecoes

ClienteRepo.criar_tabela()
ClienteRepo.inserir_clientes_json("sql/clientes.json")
TarefaRepo.criar_tabela()
TarefaRepo.inserir_tarefas_json("sql/tarefas.json")
CategoriaRepo.criar_tabela()
CategoriaRepo.inserir_categorias_json("sql/categorias.json")

app = FastAPI(dependencies=[Depends(checar_permissao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware(middleware_type="http")(middleware_autenticacao)
configurar_excecoes(app)
app.include_router(main_routes.router)
app.include_router(cliente_routes.router)