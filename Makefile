# Makefile pour PDF Converter Pro

.PHONY: help install install-dev test lint format clean build run run-dev docker-build docker-run docker-dev stop logs

# Variables
PYTHON := python3
PIP := pip3
DOCKER_IMAGE := pdf-converter-pro
DOCKER_CONTAINER := pdf-converter-container

help: ## Afficher cette aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Installer les dépendances de production
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: ## Installer les dépendances de développement
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy

test: ## Exécuter les tests
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-watch: ## Exécuter les tests en mode watch
	pytest tests/ -v --cov=src -f

lint: ## Vérifier le code avec flake8
	flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503

type-check: ## Vérifier les types avec mypy
	mypy src/ --ignore-missing-imports

format: ## Formater le code avec black
	black src/ tests/ --line-length=100

format-check: ## Vérifier le formatage sans modifier
	black src/ tests/ --line-length=100 --check

clean: ## Nettoyer les fichiers temporaires
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

build: ## Construire l'image Docker
	docker build -t $(DOCKER_IMAGE) .

build-dev: ## Construire l'image Docker de développement
	docker build -f Dockerfile.dev -t $(DOCKER_IMAGE)-dev .

run: ## Démarrer l'application localement
	streamlit run main.py

run-dev: ## Démarrer l'application en mode développement
	streamlit run main.py --server.runOnSave=true

docker-run: ## Démarrer avec Docker Compose
	docker-compose up -d

docker-dev: ## Démarrer en mode développement avec Docker
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

docker-build: ## Construire et démarrer avec Docker Compose
	docker-compose up --build -d

stop: ## Arrêter les conteneurs Docker
	docker-compose down

logs: ## Voir les logs Docker
	docker-compose logs -f

shell: ## Ouvrir un shell dans le conteneur
	docker-compose exec pdf-converter /bin/bash

setup: ## Configuration initiale du projet
	cp .env.example .env
	mkdir -p logs temp output
	$(MAKE) install-dev

check: ## Vérifications complètes (lint, type-check, test)
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test

deploy: ## Déployer en production
	$(MAKE) check
	$(MAKE) build
	docker-compose -f docker-compose.yml --profile production up -d