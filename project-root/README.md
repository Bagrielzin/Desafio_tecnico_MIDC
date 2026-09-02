# Desafio Técnico - Painel de Indicadores

Ecossistema completo para registro e visualização de indicadores de funcionários, construído com arquitetura de microsserviços.

O sistema é composto por uma API central em Python, um banco de dados relacional e duas aplicações frontend independentes (Angular para entrada de dados e React para o painel gerencial).

## 🚀 Como iniciar o ambiente

O projeto está totalmente conteinerizado, garantindo que rode de forma consistente em qualquer máquina, sem a necessidade de instalar dependências locais de Node.js ou Python.

**Pré-requisitos:** Docker e Docker Compose instalados e rodando.

1. Clone o repositório.
2. Abra o terminal na raiz do projeto (`project-root`).
3. Execute o comando abaixo para construir e iniciar todos os serviços:

```bash
docker compose up --build -d

🔗 Acessos e Portas
Após o ambiente iniciar completamente, acesse as aplicações nos seguintes endereços:

Entrada de Dados (Angular): http://localhost:4200

Painel Gerencial (React): http://localhost:3000

Documentação da API (Swagger): http://localhost:8080/docs

Health Check da API: http://localhost:8080/health

Nota: A porta do backend foi configurada para 8080 (internamente mapeando para a 8000) visando evitar conflitos comuns com outros serviços no Windows/Linux.

🏗️ Estrutura do Projeto

project-root/ 
 ├── backend/             # FastAPI + SQLAlchemy + Pydantic + Pytest
 ├── frontend-angular/    # Angular 17+ (Formulário Reativo + Serviços)
 ├── frontend-react/      # React + Vite + Tailwind + Recharts (Dashboard)
 ├── docker-compose.yml   # Orquestração dos 4 containers
 ├── .gitignore           # Ignora node_modules, pycache, venv, etc.
 └── README.md

 🧠 Arquitetura e Diferenciais Implementados
Foquei em entregar o escopo principal com estabilidade, aplicando os seguintes diferenciais técnicos exigidos:

Backend e Dados (Consulta Agregada e Exceções):

O endpoint /summary utiliza o próprio banco de dados (func.sum e group_by do SQLAlchemy) para processar os totais de entregas, enviando uma carga leve e formatada para o frontend.

Tratamento de exceções com HTTPException e SQLAlchemyError para evitar quedas em falhas de transação.

Testes unitários (Pytest) configurados com banco de dados SQLite em memória (StaticPool), garantindo testes rápidos sem afetar o banco real.

Health Check: Configurado no endpoint /health e no docker-compose.yml (pg_isready), garantindo que a API só processe requisições quando o banco estiver pronto.

Frontend Angular (Validação Estrita):

Utilização do ReactiveFormsModule para validação síncrona. O formulário barra o envio de valores não numéricos ou negativos, habilitando o botão de submissão apenas quando o formulário está estritamente válido.

Frontend React (Responsividade e UI):

Uso de Tailwind CSS com breakpoints (md:grid-cols-2) e tabelas com overflow-x-auto para responsividade nativa.

Componentização inteligente e tratamento de estados para UI (Loading, Error e Sucesso).

Gráficos dinâmicos renderizados com a biblioteca Recharts.

⚖️ Trade-offs e Decisões de Engenharia
Separação de Tabelas vs. Tabela Única: Optei por normalizar o banco de dados separando as entidades em employees e records. Embora isso exija a utilização de JOIN na API, evita anomalias de atualização (ex: se o departamento de um funcionário mudar, não precisamos atualizar centenas de registros passados) e reflete um modelo relacional realístico.

Duplicidade de Frontends: A exigência do desafio em usar Angular (inserção) e React (leitura) gerou o overhead de gerenciar dois pacotes Node. O trade-off aceito foi focar em estilização nativa/simples (Tailwind no React e CSS puro no Angular) evitando importar bibliotecas pesadas de UI (como Material Design ou AntDesign) para manter o build do Docker mais enxuto.

Migrações de Banco (Alembic): Decidi utilizar a criação nativa das tabelas pelo próprio SQLAlchemy (Base.metadata.create_all) no momento de inicialização da API. O uso do Alembic seria ideal para produção, porém, para o escopo e tempo deste desafio, essa abordagem "automática" garante que a aplicação rode out-of-the-box e sem erros para o avaliador.