# A Fazer em 11 de Junho de 2024

## Cadastro do Cliente

- Acertar menu ativo do cabeçalho
- Adicionar SQL para tornar e revogar um cliente administrador
- Alterar SQL de Cliente e ClienteRepo.inserir para o campo telefone ficar logo após endereco
- Criar classe Cliente
- Criar repositório para a entidade cliente
- Criar página para cadastro de cliente
- Importar arquivo Python de validação de formulários (/util/validators.py)
- Criar DTO baseada em Pydantic para novo cliente
- Adicionar arquivos javascript para máscara e envio de formulário via JSON
- Adicionar atributo data-mask="..." aos inputs do cadastro de cliente
- Criar rota para cadastro de cliente (post) em main_routes.py
- Criar rota e página para cadastro confirmado (get) em main_routes.py
- Renomear arquivo para cadastro_confirmado.html

## Autenticação

- Alterar responsividade, botão "Entrar", links, action, json-form, button[submit] (entrar.html)
- Importar arquivo Python de autenticação (/util/auth.py)
- Importar arquivo Python de criação de cookies (/util/cookies.py)
- Importar arquivo Python para criação de validações customizadas com Pydantic (/util/pydantic.py)
- Importar arquivo Python para tratamento de exceções (/util/exceptions.py) e adicionar as páginas erro.html e 404.html
- Criar /dto/login_dto.py
- Adicionar método no repo para buscar cliente por email
- Adicionar método no repo para alterar token do cliente
- Adicionar método no repo para buscar cliente por token
- Adicionar cliente_logado: Cliente = Depends(obter_cliente_logado) como parâmetro de todas as rotas get e adicionar "cliente": cliente_logado ao modelo do template retornado
- Complementar o template header.html para mostrar estado do cliente (logado/deslogado)
- Criar rota para login (post) em main\_routes.py
- Adicionar middleware de atualização do token de autenticação
- Criar rota para logout (get) em main\_routes.py
- Elemento main do HTML foi movido para a página base e removido dos demais
- Criado o bloco topo na página base
- Carousel foi movido para um include
- Includes de exibição de mensagens por cookies adicionados à página base

## Carrinho e Pedidos

- Adicionar página do carrinho protegida somente para clientes
- Adicionar página de pedidos protegida somente para clientes

## Área Restrita

- Adicionar página do perfil protegida somente para clientes
