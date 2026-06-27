# Exercício 4.2 — Servidor MCP para Lista de Tarefas

Servidor MCP (Model Context Protocol) que expõe as operações da API REST de tarefas (exercício 4.1) como ferramentas para agentes de IA.

## Pré-requisitos

- Python 3.11+
- API do exercício 4.1 rodando em `http://localhost:8000`

## Instalação

```bash
pip install -r requirements.txt
```

## Ferramentas disponíveis

| Ferramenta | Descrição |
|---|---|
| `criar_tarefa` | Cria uma nova tarefa via POST /tarefas |
| `listar_tarefas` | Lista todas as tarefas via GET /tarefas |

## Como testar

Com a API 4.1 rodando em localhost:8000:

```bash
python cliente_teste.py
```
