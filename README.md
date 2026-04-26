# cloud-to-local-ai-platform

API para processamento de imagens com detecção de faces rodando
localmente, sem dependência de serviços em nuvem.

O projeto implementa um pipeline completo: upload → processamento →
detecção → persistência → entrega via HTTP.

------------------------------------------------------------------------

## Contexto

Este projeto é uma adaptação de um sistema desenvolvido durante um
programa com foco em AWS e Machine Learning. Aqui, a arquitetura foi
reimplementada para execução local usando ferramentas open source.

O objetivo é demonstrar como construir um serviço de visão computacional
com controle total sobre dados e infraestrutura.

------------------------------------------------------------------------

## Problema

Serviços de análise de imagem em nuvem têm custo recorrente, dependem de
rede e exigem envio de dados para terceiros.

Em alguns cenários, isso não é viável.

------------------------------------------------------------------------

## Solução

A aplicação expõe uma API que processa imagens localmente:

-   recebe arquivos via upload
-   executa detecção de faces com OpenCV
-   desenha bounding boxes
-   salva a imagem processada no sistema de arquivos
-   persiste metadados no banco
-   disponibiliza acesso à imagem via endpoint

------------------------------------------------------------------------

## Arquitetura

Separação em camadas:

-   Router: camada HTTP (FastAPI)
-   Service: processamento e regras de negócio
-   Models: schemas (Pydantic) e ORM (SQLAlchemy)
-   Database: SQLite

Essa separação mantém o código testável e reduz acoplamento.

### Fluxo

Upload → Service → OpenCV → Storage → Database → Response

------------------------------------------------------------------------

## Tecnologias

-   FastAPI
-   OpenCV
-   SQLite
-   SQLAlchemy
-   Pydantic
-   Pillow

------------------------------------------------------------------------

## Funcionalidades

-   CRUD de usuários
-   Upload de imagens
-   Detecção de faces
-   Armazenamento local
-   Acesso às imagens via URL
-   Histórico de análises

------------------------------------------------------------------------

## Endpoints principais

### POST /image/analyze

Recebe uma imagem e retorna o resultado da análise.

Response:

{ "filename": "example.jpg", "faces_detected": 2, "faces": \[ { "x":
100, "y": 120, "width": 80, "height": 80 } \], "url":
"http://127.0.0.1:8000/image/files/example.jpg" }

------------------------------------------------------------------------

### GET /image/files/{filename}

Retorna a imagem processada.

Exemplo:

http://127.0.0.1:8000/image/files/example.jpg

------------------------------------------------------------------------

### GET /image/history

Lista análises armazenadas no banco.

------------------------------------------------------------------------

## Como executar

git clone https://github.com/niqueborges/cloud-to-local-ai-platform.git
cd cloud-to-local-ai-platform

python -m venv venv

# Linux / Mac

source venv/bin/activate

# Windows

venv`\Scripts`{=tex}`\activate`{=tex}

pip install -r requirements.txt

uvicorn app.main:app --reload

Acesse:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## Estrutura do projeto

app/ ├── main.py ├── database.py ├── dependencies.py ├── modules/ │ ├──
users/ │ └── image_analysis/ │ ├── router.py │ ├── service.py │ ├──
models.py │ └── models_db.py ├── models/ │ └──
haarcascade_frontalface_default.xml

storage/ └── images/

------------------------------------------------------------------------

## Decisões técnicas

-   Processamento local para evitar dependência de cloud
-   UUID para evitar colisão de arquivos
-   Service layer para separar lógica do HTTP
-   SQLite para simplicidade e portabilidade

------------------------------------------------------------------------

## Limitações

-   Modelo Haar Cascade tem menor precisão que redes neurais modernas
-   Sem autenticação
-   Armazenamento local não escalável

------------------------------------------------------------------------

## Próximos passos

-   Relacionar análises com usuários
-   Melhorar modelo de detecção (ex: DNN)
-   Adicionar autenticação
-   Deploy em ambiente cloud (AWS)

------------------------------------------------------------------------

## Observações

Arquivos gerados não são versionados (ignorados via .gitignore).
