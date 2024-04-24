# Workout API

Este projeto faz parte do Bootcamp da Digital Innovation One em parceria com a Vivo. A Workout API é uma API RESTful desenvolvida com o framework FastAPI em Python, destinada a gerenciar informações relacionadas a atletas, centros de treinamento e categorias esportivas.

## Funcionalidades Principais

- Cadastro, consulta, atualização e exclusão de atletas.
- Cadastro, consulta, atualização de centros de treinamento.
- Cadastro, consulta, atualização de categorias esportivas.
- Consulta de todos os atletas com informações detalhadas, incluindo nome, CPF, idade, peso, altura, sexo, centro de treinamento e categoria.
- Paginação de resultados para melhor organização e visualização dos dados.

## Requisitos

- Python 3.12.3 ou superior
- Pip (gerenciador de pacotes do Python)
- Banco de dados PostgreSQL (ou outro suportado pelo SQLAlchemy)
- Docker

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/workout-api.git
   ```

2. Acesse o diretório do projeto:

   ```bash
   cd workout-api
   ```
3. Suba um container docker com postgresql:

   ```bash
   docker-compose up
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Configure o arquivo `.env` com as variáveis de ambiente necessárias, como as credenciais do banco de dados.

6. Execute as migrações do banco de dados:

   ```bash
   alembic upgrade head
   ```

7. Inicie o servidor:

   ```bash
   uvicorn main:app --reload
   ```
A API estará disponível em `http://localhost:8000`.
Existe um aqruivo Makefile para facilitar o trabalho caso prefira

## Documentação da API

A documentação interativa da API pode ser acessada em `http://localhost:8000/docs`, onde é possível testar os endpoints e visualizar detalhes sobre os parâmetros e modelos de dados.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir um PR ou relatar problemas encontrados.

## Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).
