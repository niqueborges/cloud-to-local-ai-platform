# cloud-to-local-ai-platform

API para processamento de imagens com detecção de faces rodando localmente, sem envio de dados para serviços externos.

---

## Demo rápida

1. Suba a API
2. Acesse: http://127.0.0.1:8000/docs
3. Use o endpoint /image/analyze com uma imagem

Teste básico:

GET /
→ { "message": "API is running" }

Exemplo com curl:

curl -X POST "http://127.0.0.1:8000/image/analyze" \
  -F "file=@test.jpg"

---

## Contexto

Projeto baseado em um sistema anterior com AWS e Machine Learning, reescrito para execução local usando ferramentas open source.

O foco é manter controle sobre dados e reduzir dependência de rede.

---

## Problema

Serviços de visão computacional em nuvem geram custo recorrente, exigem envio de dados e dependem de conectividade.

---

## Solução

API que processa imagens localmente:

- recebe arquivos via upload
- detecta faces com OpenCV
- desenha bounding boxes
- salva imagem processada
- persiste metadados no banco
- expõe acesso via HTTP

---

## Arquitetura

Separação por módulos:

- router: camada HTTP
- service: regras de negócio
- models: ORM (SQLAlchemy)
- schemas: validação (Pydantic)
- database: conexão SQLite

Detalhes:

- router não contém lógica
- service concentra processamento
- service não depende do FastAPI
- acesso ao banco via Session

### Fluxo interno

1. Upload recebido como bytes  
2. Conversão para numpy (Pillow)  
3. Conversão para grayscale  
4. Detecção com Haar Cascade  
5. Desenho das bounding boxes  
6. Salvamento da imagem  
7. Persistência no banco  
8. Retorno da resposta  

---

## Tecnologias

- FastAPI
- OpenCV
- SQLite
- SQLAlchemy
- Pydantic
- Pillow

---

## Funcionalidades

- CRUD de usuários
- Upload de imagens
- Detecção de faces
- Armazenamento local
- Acesso às imagens via URL
- Histórico de análises

---

## Endpoints principais

### POST /image/analyze

Recebe uma imagem e retorna o resultado da análise.

Response:

{
  "filename": "example.jpg",
  "faces_detected": 2,
  "faces": [
    { "x": 100, "y": 120, "width": 80, "height": 80 }
  ],
  "url": "/image/files/example.jpg"
}

---

### GET /image/files/{filename}

Retorna a imagem processada.

---

### GET /image/history

Lista análises armazenadas no banco.

---

## Banco de dados

SQLite local (app.db) usando SQLAlchemy.

- tabelas criadas automaticamente na inicialização
- duas entidades principais:
  - users
  - image_analysis

---

## Como executar

git clone https://github.com/niqueborges/cloud-to-local-ai-platform.git
cd cloud-to-local-ai-platform

python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

Acesse:
http://127.0.0.1:8000/docs

---

## Estrutura do projeto

## Estrutura do projeto

```bash
app/
├── main.py
├── database.py
├── dependencies.py
├── modules/
│   ├── users/
│   │   ├── router.py
│   │   ├── service.py
│   │   ├── models.py
│   │   └── schemas.py
│   └── image_analysis/
│       ├── router.py
│       ├── service.py
│       ├── models.py
│       └── schemas.py
├── models/
│   └── haarcascade_frontalface_default.xml

storage/
└── images/

README.md
requirements.txt
.gitignore

---

## Dependência importante

O arquivo haarcascade_frontalface_default.xml deve existir em:

app/models/

Sem ele, a detecção de faces não funciona.

---

## Decisões técnicas

- processamento local sem uso de cloud
- separação router/service para isolar lógica
- SQLite por simplicidade
- armazenamento em disco para imagens
- uso de Haar Cascade por baixo custo computacional

---

## Limitações

- menor precisão comparado a modelos baseados em redes neurais
- sem autenticação
- armazenamento local não escala
- não otimizado para alta concorrência

---

## Próximos passos

- substituir Haar Cascade por modelo DNN do OpenCV
- integrar modelo baseado em CNN
- adicionar autenticação JWT
- relacionar análises com usuários
- preparar deploy em ambiente cloud

---

## Observações

Arquivos gerados não são versionados (ignorados via .gitignore).

## Licença

Este projeto está sob a licença MIT.

Veja o arquivo [LICENSE](./LICENSE).md para mais detalhes.


