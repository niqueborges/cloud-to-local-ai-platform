# cloud-to-local-ai-platform

Este projeto é uma adaptação de um sistema originalmente desenvolvido durante minha participação em um programa de bolsas com foco em AWS e Machine Learning. Nesta versão, a arquitetura foi reconstruída para rodar localmente com ferramentas open source. API para processamento de imagens com detecção de faces, executando localmente sem dependência de serviços em nuvem.

---

## Problema

Soluções de processamento de imagem costumam depender de serviços em nuvem, o que implica custo, latência e menor controle sobre os dados.

Este projeto demonstra como executar esse fluxo localmente, mantendo controle total sobre processamento e armazenamento.

---

## Solução

A aplicação fornece uma API capaz de:

- Receber upload de imagens
- Processar imagens localmente
- Detectar faces utilizando OpenCV
- Desenhar bounding boxes nas faces detectadas
- Armazenar imagens processadas no sistema de arquivos
- Servir imagens via endpoint HTTP

---

## Arquitetura

O projeto segue separação por camadas:

- **Router**: entrada HTTP (FastAPI)
- **Service**: lógica de negócio e processamento
- **Models**: validação de dados (Pydantic)
- **Database**: persistência (SQLAlchemy + SQLite)

### Fluxo da aplicação

Upload → Processamento → Detecção → Salvamento → Resposta

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

- CRUD completo de usuários
- Upload e análise de imagens
- Detecção de faces
- Armazenamento local de arquivos
- Endpoint para acesso às imagens processadas

---

## Como executar

```bash
git clone https://github.com/niqueborges/cloud-to-local-ai-platform.git
cd cloud-to-local-ai-platform

python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

Acesse a documentação interativa:

http://127.0.0.1:8000/docs

---

{
  "filename": "example.jpg",
  "faces_detected": 2,
  "faces": [
    {
      "x": 100,
      "y": 120,
      "width": 80,
      "height": 80
    }
  ]
}

---

GET /image/files/{filename}

# Exemplo:

http://127.0.0.1:8000/image/files/example.jpg

---

app/
├── main.py
├── database.py
├── dependencies.py
├── modules/
│   ├── users/
│   └── image_analysis/
│       ├── router.py
│       └── service.py
├── models/
│   └── haarcascade_frontalface_default.xml

storage/
└── images/

---

Próximos passos:

Persistência de metadados das imagens no banco
Relacionamento entre usuários e análises
Histórico de processamento
Melhorias no modelo de detecção
Possível integração com serviços cloud

Observações:
Arquivos gerados não são versionados (ignorados via .gitignore)
O projeto utiliza processamento local, sem dependência externa



