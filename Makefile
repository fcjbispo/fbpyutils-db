.PHONY: help venv install build test clean

# Detecta o sistema operacional para usar caminhos adequados
OS := $(shell uname 2>/dev/null || echo Windows_NT)

# Define VENV_PATH, usando UV_PROJECT_ENVIRONMENT se disponível, senão .venv
VENV_PATH ?= .venv
ifneq ($(UV_PROJECT_ENVIRONMENT),)
VENV_PATH := $(UV_PROJECT_ENVIRONMENT)
endif

help:
	@echo "Alvos disponíveis:"
	@echo "  make venv    : Cria o ambiente virtual ($(VENV_PATH)) se não existir"
	@echo "  make install : Instala as dependências de desenvolvimento em $(VENV_PATH)"
	@echo "  make build   : Compila o projeto (usando uv build)"
	@echo "  make test    : Executa os testes com pytest"
	@echo "  make clean   : Remove arquivos de build/artefatos de teste"
	@echo ""
	@echo "Variáveis de ambiente:"
	@echo "  UV_PROJECT_ENVIRONMENT: Caminho do ambiente virtual (padrão: .venv)"
	@echo ""

venv:
ifeq ($(OS),Windows_NT)
	if not exist $(VENV_PATH) (uv venv $(VENV_PATH))
else
	test -d $(VENV_PATH) || uv venv $(VENV_PATH)
endif

install: venv
ifeq ($(OS),Windows_NT)
	uv sync --group dev
else
	uv sync --group dev
endif

build: install test
ifeq ($(OS),Windows_NT)
	uv build
else
	uv build
endif

test: install
ifeq ($(OS),Windows_NT)
	uv run pytest -s -vv
else
	uv run pytest -s -vv
endif

clean:
	rm -rf dist build .pytest_cache .mypy_cache *.egg-info
