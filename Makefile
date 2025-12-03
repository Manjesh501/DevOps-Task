.PHONY: help dev build test clean test-backend test-frontend deploy scan

help:
	@echo "DevOps Sample Project Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  dev        - Start development environment"
	@echo "  build      - Build Docker images"
	@echo "  test       - Run backend + frontend tests"
	@echo "  deploy     - Run deployment script"
	@echo "  scan       - Run Trivy security scans"
	@echo "  clean      - Remove all containers and volumes"
	@echo ""

dev:
	docker-compose -f docker-compose.dev.yml up --build

build:
	docker-compose -f docker-compose.dev.yml build

test: test-backend test-frontend

test-backend:
	cd backend && pip install -r requirements.txt && pip install pytest && pytest tests/

test-frontend:
	@if [ -f frontend/index.html ]; then \
		echo "Frontend test passed: index.html exists"; \
	else \
		echo "Frontend test failed: index.html not found"; exit 1; \
	fi

deploy:
	cd infra && ./deploy.sh

scan:
	trivy image 815539056618.dkr.ecr.eu-north-1.amazonaws.com/sample-backend:latest
	trivy image 815539056618.dkr.ecr.eu-north-1.amazonaws.com/sample-frontend:latest

clean:
	docker-compose -f docker-compose.dev.yml down -v || true
	docker-compose down -v || true
	cd monitoring && docker-compose down -v || true
