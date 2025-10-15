# Guia de Contribuição – cpf-serverless-python

Bem-vindo! Este documento orienta sobre como configurar o ambiente, adotar convenções e contribuir com qualidade para este projeto.

---

## 🛠️ Setup do Ambiente

### Pré-requisitos

Antes de iniciar o desenvolvimento, certifique-se de ter as seguintes ferramentas instaladas:

- **Python 3.8+** (preferencialmente gerenciado com `pyenv`)
- **Poetry** (gerenciamento de dependências)
- **Azure CLI** (para deploy e gerenciamento de recursos Azure)
- **Azure Functions Core Tools** (para execução local de Azure Functions)

> 📘 **Importante:** Para instalação completa das ferramentas Azure (Azure CLI e Azure Functions Core Tools), incluindo configuração de autenticação, subscription e permissões, consulte a seção **[🔧 Setup das Ferramentas Azure para Desenvolvimento e Deploy (WSL2/Ubuntu)](README.md#-setup-das-ferramentas-azure-para-desenvolvimento-e-deploy-wsl2ubuntu)** no README.md.

### Instalação das Dependências do Projeto

- **Instale as dependências:**
  ```bash
  poetry install --no-root
  ```

- **Ative o ambiente virtual Poetry:**
  ```bash
  poetry shell
  ```

- **Verifique a versão do Python:**
  ```bash
  python --version
  ```

### Validação do Ambiente Azure

Após configurar as ferramentas Azure (conforme guia no README.md), valide a instalação:

```bash
# Verificar Azure CLI
az --version

# Verificar Azure Functions Core Tools
func --version

# Verificar autenticação
az account show
```
---

### Estrutura de Funções Azure

- Todas as Azure Functions devem ser criadas e organizadas em subpastas dentro de `src/functions/<nome_da_funcao>`.
- Siga sempre os padrões de nomeação e estrutura do projeto principal descritos no README.md.

---

## ⚙️ Ferramentas e Dependências

- **Dependências base:**
  - `azure-functions`
  - `azure-functions-worker`
  - `pydantic`
  - `cpf-cnpj-validator`

- **Dependências de desenvolvimento:**
  - `pytest` (testes)
  - `black` (formatação de código)
  - `flake8` (linter)
  - `mypy` (type checking)
  - `pytest-cov` (cobertura de testes)

---

## 📝 Checks de Qualidade

Execute antes de abrir PR:

- **Testes:**
  ```bash
  poetry run pytest
  ```

- **Formatação Black:**
  ```bash
  poetry run black --check .
  ```

- **Lint:**
  ```bash
  poetry run flake8 .
  ```

- **Type Check:**
  ```bash
  poetry run mypy .
  ```

### Executar Todos os Checks de Uma Vez

```bash
# Script sugerido para executar todos os checks
poetry run black --check . && \
poetry run flake8 . && \
poetry run mypy . && \
poetry run pytest
```

---

## 🧙 Observações Importantes

- O projeto possui `.flake8` configurado para ignorar pastas ocultas/ambiente virtual.
- Use sempre `poetry install --no-root` caso não deseje instalar o projeto como pacote Python.
- Mantenha o código na pasta principal do projeto (ex: `src/` ou `cpf_serverless_python/`, conforme padrão).
- **Para contribuidores em WSL2/Ubuntu:** Consulte a seção de troubleshooting no README.md caso encontre problemas com Azure CLI ou Azure Functions Core Tools.

---

## 🚀 Fluxo para Pull Requests

1. Crie uma branch referente à issue (ex: `hotfix/22-complementa-dependencias`)
2. Faça commits claros e objetivos (ex: `"feat: validação de CPF"`)
3. Execute todos os checks de qualidade antes de abrir o PR
4. Relacione o PR à Issue correspondente e documente comandos/evidências no PR
5. Aguarde a revisão e responda aos comentários, se houver

### Convenções de Commit

Utilize o formato [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Alterações na documentação
- `test:` - Adição ou modificação de testes
- `refactor:` - Refatoração de código
- `chore:` - Tarefas de manutenção
- `ci:` - Alterações em CI/CD

---

## 📚 Recursos para Contribuidores

- [Documentação do Azure Functions (Python)](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black Code Style](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)

---

## 💡 Dúvidas ou Sugestões?

Contribua ou peça mentoria!
  
Contate o responsável pelo repositório ou abra uma discussão na aba "Issues".

---

**Bons commits e bons PRs!**
