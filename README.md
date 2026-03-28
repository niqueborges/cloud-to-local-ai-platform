# cloud-to-local-ai-platform

Este projeto é uma adaptação de um sistema originalmente desenvolvido durante minha participação em um programa de bolsas com foco em AWS e Machine Learning. Nesta versão, a arquitetura foi reconstruída para rodar localmente com ferramentas open source.

## Funcionalidades

- [x] Gerenciamento de usuários (CRUD com FastAPI e SQLite)
- [x] Upload e análise de imagens
- [x] Detecção de rostos (OpenCV, execução local);Inclui detecção de rostos local substituindo AWS Rekognition.
- [ ] Processamento de áudio
- [ ] Chatbot

## Tecnologias

- Python
- FastAPI

## Como executar

```bash
uvicorn app.main:app --reload