# Cloud to Local AI Platform

API desenvolvida em FastAPI para processamento de imagens (detecção de faces via OpenCV) rodando localmente.

## Contexto e Objetivo

O projeto substitui serviços de visão computacional em nuvem por uma solução open source local. 
O objetivo principal é eliminar o custo recorrente e a latência de rede associados ao envio de imagens para APIs externas, garantindo o processamento nativo e seguro dos dados.

## Arquitetura

O sistema é modular e utiliza os seguintes padrões:
- **Router/Service/Schema/Model:** Isolamento de responsabilidades (Clean Architecture leve). O router não possui lógica de negócio.
- **Processamento em Background (Filas):** A detecção do OpenCV (Haar Cascade) é pesada. Utilizamos **Celery + Redis** para enfileirar as tarefas, liberando a API imediatamente e garantindo alta concorrência.
- **Armazenamento Sem Estado (Stateless):** Imagens são salvas em um Object Storage compatível com S3 (**MinIO**), enquanto metadados e credenciais ficam no banco relacional PostgreSQL. Nenhuma imagem é salva no disco local da API.

## Tecnologias e Infraestrutura

- **Backend:** FastAPI, Pydantic, Pillow
- **Visão Computacional:** OpenCV (`haarcascade_frontalface_default.xml`)
- **Segurança:** PyJWT, passlib (bcrypt)
- **Banco de Dados:** PostgreSQL (via driver puro Python `pg8000`) 
- **ORM:** SQLAlchemy
- **Armazenamento:** MinIO (S3-Compatible Object Storage)
- **Fila de Tarefas (Background):** Celery + Redis
- **Migrações:** Alembic
- **CI/CD:** Github Actions para testes no Pytest

---

## Como Executar

### 1. Iniciar os Serviços de Infraestrutura (Docker)
O projeto depende de **PostgreSQL**, **MinIO** e **Redis**. Para subir os serviços locais de desenvolvimento, certifique-se de ter o Docker instalado e rode:
```bash
docker-compose up -d --build
```
Isso também iniciará o **Celery Worker** em background para o processamento de imagens.

### 2. Baixar o Modelo do OpenCV
Baixe manualmente o classificador de faces do repositório oficial e coloque na pasta `app/models/`:
```bash
mkdir -p app/models
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml -O app/models/haarcascade_frontalface_default.xml
```

### 3. Instalar Dependências e Rodar a API
```bash
python -m venv .venv
source .venv/bin/activate  # ou .\.venv\Scripts\Activate.ps1 no Windows
pip install -r requirements.txt

# Execute as migrações do banco de dados (Alembic)
alembic upgrade head

uvicorn app.main:app --reload
```

A documentação interativa estará disponível em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Executando a API via Docker
Caso prefira não instalar o Python e dependências na sua máquina local, nós criamos um `Dockerfile` leve com o `python:3.12-slim` que já baixa o OpenCV. Para utilizá-lo:
```bash
# 1. Garanta que o banco de dados via docker-compose (Passo 1) está rodando
# 2. Construa a imagem da API
docker build -t cloud-to-local-ai .

# 3. Rode o container da API 
docker run -p 8000:8000 cloud-to-local-ai
```

---

## Endpoints e Autenticação (JWT)

Para garantir segurança, endpoints críticos exigem um token Bearer JWT.

1. **Criar Usuário:** `POST /users/` enviando um JSON com `name`, `email`, `password` e `birth_date`.
2. **Login:** `POST /auth/token` enviando `username` (email) e `password` via FormData para receber o JWT.
3. **Analisar Imagem (Protegido):** `POST /image/analyze` passando o token JWT no cabeçalho e a imagem via Multipart/Form-data. Retorna o ID da análise, status (`PENDING`) e a URL pré-assinada da imagem no MinIO.
4. **Visualizar Imagem (Público):** `GET /image/files/{filename}`. Redireciona automaticamente para a URL pré-assinada do Object Storage.
5. **Histórico (Protegido):** `GET /image/history`.

## Postman / Insomnia
Se preferir não usar a página local do Swagger `/docs`, o repositório contém o arquivo **`endpoints.json`**. Ele é uma exportação no formato nativo OpenAPI 3.1. 

Basta usar a função de *Import* do seu Postman ou Insomnia apontando para este arquivo, e todas as rotas e regras de payloads aparecerão mapeadas automaticamente para você!

---

## Estrutura do Código

```bash
app/
├── main.py
├── database.py
├── dependencies.py
├── worker.py           # Celery App e fila de tarefas em background
├── modules/
│   ├── auth/           # Geração e validação de JWT / senhas
│   ├── users/          # CRUD de usuários 
│   └── image_analysis/ # Regras de OpenCV e rotas de imagem
├── models/
│   └── haarcascade_frontalface_default.xml
...
```

## Próximos Passos
- Substituir o Haar Cascade (veloz, mas impreciso) por um modelo DNN mais robusto do OpenCV.
- Implementar WebSockets para notificar o Frontend em tempo real assim que o Celery concluir o processamento da imagem.

## Licença
Este projeto está sob a licença MIT.
