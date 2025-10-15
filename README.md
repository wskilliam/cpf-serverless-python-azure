# Microsserviço Serverless para Validação de CPF – Azure Functions (Python)
Repositório para desenvolvimento de microsserviço serverless destinado à validação de CPF, utilizando **Azure Functions** e ambiente Python moderno.

---

## 🚀 Visão Geral

- Projeto desenvolvido em **Python 3.8+** (preferencialmente gerenciado com `pyenv`)
- Gerenciamento de dependências com **Poetry**
- Infraestrutura preparada para **Azure Functions Core Tools**
- Estrutura modular e escalável, seguindo boas práticas de separação de responsabilidades

---

## 🗂️ Estrutura do Projeto

```
├── src/
│   ├── functions/
│   │   └── cpf_validation/
│   │       ├── __init__.py
│   │       └── function_app.py
│   ├── core/
│   │   ├── validators/
│   │   ├── models/
│   │   └── utils/
│   └── config/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── .github/
│   └── workflows/
├── scripts/
└── requirements.txt
```

- **src/**: Código principal da aplicação
- **tests/**: Testes unitários e de integração
- **docs/**: Documentação técnica e de produto
- **.github/workflows/**: Automação CI/CD (actions, workflows)
- **scripts/**: Utilitários e ferramentas auxiliares
- **requirements.txt**: Alternativa para ambientes sem Poetry

---

## ⚙️ Como Rodar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Jcnok/cpf-serverless-python.git
   cd cpf-serverless-python
   ```

2. **Configure o ambiente Python:**
   - Recomenda-se usar `pyenv` para gerenciar versões do Python
   - Instale a versão recomendada do Python (3.8+)

3. **Instale as dependências com Poetry:**
   ```bash
   poetry install
   ```

4. **Ative o ambiente virtual:**
   ```bash
   poetry shell

   ```

---
## Exemplo de Função Inicial (src/functions/cpf_validation)

```
import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="ValidarCPF", auth_level=func.AuthLevel.FUNCTION)
def ValidarCPF(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

```
1. **Inicialização**
   ```bash
   func start

   ```
---

## 🔧 Setup das Ferramentas Azure para Desenvolvimento e Deploy (WSL2/Ubuntu)

Esta seção descreve o processo completo de configuração do ambiente de desenvolvimento para Azure Functions em ambiente **WSL2/Ubuntu**. Siga os passos abaixo para instalar, configurar e validar as ferramentas necessárias.

### 📋 Requisitos

- **Sistema Operacional:** WSL2 com Ubuntu 20.04+ ou distribuição compatível
- **Python:** 3.12.1 (gerenciado preferencialmente com `pyenv`)
- **Poetry:** Para gerenciamento de dependências
- **Acesso à Internet:** Necessário para download de pacotes e autenticação
- **Conta Azure:** Com permissões adequadas para criação e gerenciamento de recursos

### 🛠️ Instalação do Azure CLI

O Azure CLI é a ferramenta de linha de comando para gerenciar recursos do Azure.

```bash
# Atualizar repositórios do sistema
sudo apt-get update

# Instalar dependências necessárias
sudo curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verificar instalação
az --version
```

**Observações:**
- Em ambientes WSL2, certifique-se de que o serviço de rede está funcionando corretamente
- Caso encontre erros de conectividade, reinicie o WSL2: `wsl --shutdown` (executar no PowerShell/CMD)

### ⚡ Instalação do Azure Functions Core Tools

O Azure Functions Core Tools permite executar e depurar Azure Functions localmente.

```bash
# Adicionar repositório da Microsoft (se ainda não adicionado)
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg

# Adicionar o feed de pacotes do Azure Functions Core Tools
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'

# Atualizar repositórios
sudo apt-get update

# Instalar Azure Functions Core Tools (versão 4.x)
sudo apt-get install -y azure-functions-core-tools-4

# Verificar instalação
func --version
```
### 🔐 Autenticação no Azure

Após instalar as ferramentas, é necessário autenticar-se na sua conta Azure.

```bash
# Login interativo no Azure
az login

# Em ambientes WSL2, o comando acima abrirá o navegador padrão do Windows
# Siga as instruções na página de login para completar a autenticação

# Verificar a conta autenticada
az account show
```

**Dica:** Se o navegador não abrir automaticamente, use o login com código de dispositivo:

```bash
# Login alternativo usando código de dispositivo
az login --use-device-code

# Siga as instruções exibidas no terminal para completar a autenticação
```

### 📊 Configuração da Subscription

Configure a subscription padrão que será utilizada para o projeto.

```bash
# Listar todas as subscriptions disponíveis
az account list --output table

# Definir a subscription padrão (substitua SUBSCRIPTION_ID pelo ID desejado)
az account set --subscription <SUBSCRIPTION_ID>

# Ou usando o nome da subscription
az account set --subscription "Nome da Subscription"

# Confirmar a subscription ativa
az account show --output table
```

**Boas Práticas:**
- Sempre verifique qual subscription está ativa antes de criar recursos
- Documente o ID/nome da subscription utilizada no projeto
- Utilize tags para organizar recursos relacionados ao projeto

### ✅ Validação de Permissões

Verifique se sua conta possui as permissões necessárias para criar e gerenciar recursos.

```bash
# Listar resource groups disponíveis
az group list --output table

# Verificar permissões em um resource group específico
az role assignment list --resource-group <RESOURCE_GROUP_NAME> --output table

```

**Permissões mínimas recomendadas:**
- **Contributor** ou superior no Resource Group utilizado
- Permissões para criar e gerenciar Azure Functions
- Permissões para criar e gerenciar Storage Accounts (necessário para Azure Functions)

### 🧪 Teste de Configuração Local

Após configurar todas as ferramentas, teste o ambiente local.

```bash
# Criar um projeto de teste do Azure Functions
mkdir test-function && cd test-function

# Inicializar um novo projeto Azure Functions
func init --python

# Criar uma função HTTP de exemplo
func new --name HttpExample --template "HTTP trigger" --authlevel "anonymous"

# Executar a função localmente
func start

# Testar em outro terminal
curl http://localhost:7071/api/HttpExample?name=Azure

# Limpar após o teste
cd ..
rm -rf test-function
```
### 🚨 Troubleshooting - Problemas Comuns em WSL2

#### Problema: Erro de conectividade durante instalação
```bash
# Solução 1: Reiniciar WSL2
wsl --shutdown  # Executar no PowerShell/CMD do Windows

# Solução 2: Verificar DNS
cat /etc/resolv.conf
sudo nano /etc/resolv.conf  # Adicionar: nameserver 8.8.8.8
```

#### Problema: func command not found
```bash
# Verificar se o PATH está configurado corretamente
echo $PATH

# Reinstalar Azure Functions Core Tools
sudo apt-get remove azure-functions-core-tools-4
sudo apt-get install -y azure-functions-core-tools-4
```

#### Problema: Erro ao abrir navegador no az login
```bash
# Use o método alternativo com código de dispositivo
az login --use-device-code
```

#### Problema: Permissões insuficientes
```bash
# Verificar roles atribuídas
az role assignment list --assignee $(az account show --query user.name -o tsv)

# Solicitar permissões adequadas ao administrador da subscription
```
### 📚 Recursos Adicionais

- [Documentação Oficial do Azure CLI](https://docs.microsoft.com/cli/azure/)
- [Documentação do Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local)
- [Guia de Desenvolvimento Azure Functions com Python](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [WSL2 e Azure CLI - Boas Práticas](https://docs.microsoft.com/windows/wsl/)

---

## 🔧 Setup das Ferramentas Azure para Desenvolvimento e Deploy (WSL2/Ubuntu)

Esta seção descreve o processo completo de configuração do ambiente de desenvolvimento para Azure Functions em ambiente **WSL2/Ubuntu**. Siga os passos abaixo para instalar, configurar e validar as ferramentas necessárias.

### 📋 Requisitos

- **Sistema Operacional:** WSL2 com Ubuntu 20.04+ ou distribuição compatível
- **Python:** 3.8 ou superior (gerenciado preferencialmente com `pyenv`)
- **Poetry:** Para gerenciamento de dependências
- **Acesso à Internet:** Necessário para download de pacotes e autenticação
- **Conta Azure:** Com permissões adequadas para criação e gerenciamento de recursos

### 🛠️ Instalação do Azure CLI

O Azure CLI é a ferramenta de linha de comando para gerenciar recursos do Azure.

```bash
# Atualizar repositórios do sistema
sudo apt-get update

# Instalar dependências necessárias
sudo apt-get install -y ca-certificates curl apt-transport-https lsb-release gnupg

# Baixar e instalar a chave de assinatura da Microsoft
sudo mkdir -p /etc/apt/keyrings
curl -sLS https://packages.microsoft.com/keys/microsoft.asc | \
  gpg --dearmor | sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null
sudo chmod go+r /etc/apt/keyrings/microsoft.gpg

# Adicionar o repositório do Azure CLI
AZ_DIST=$(lsb_release -cs)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ ${AZ_DIST} main" | \
  sudo tee /etc/apt/sources.list.d/azure-cli.list

# Atualizar repositórios e instalar Azure CLI
sudo apt-get update
sudo apt-get install -y azure-cli

# Verificar instalação
az --version
```

**Observações:**
- Em ambientes WSL2, certifique-se de que o serviço de rede está funcionando corretamente
- Caso encontre erros de conectividade, reinicie o WSL2: `wsl --shutdown` (executar no PowerShell/CMD)

### ⚡ Instalação do Azure Functions Core Tools

O Azure Functions Core Tools permite executar e depurar Azure Functions localmente.

```bash
# Adicionar repositório da Microsoft (se ainda não adicionado)
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg

# Adicionar o feed de pacotes do Azure Functions Core Tools
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'

# Atualizar repositórios
sudo apt-get update

# Instalar Azure Functions Core Tools (versão 4.x)
sudo apt-get install -y azure-functions-core-tools-4

# Verificar instalação
func --version
```

**Observações específicas para WSL2:**
- O Azure Functions Core Tools requer o .NET runtime, que será instalado automaticamente como dependência
- Caso encontre problemas com a instalação, verifique se os repositórios da Microsoft estão configurados corretamente
- Para ambientes com proxy, configure as variáveis de ambiente `http_proxy` e `https_proxy` antes da instalação

### 🔐 Autenticação no Azure

Após instalar as ferramentas, é necessário autenticar-se na sua conta Azure.

```bash
# Login interativo no Azure
az login

# Em ambientes WSL2, o comando acima abrirá o navegador padrão do Windows
# Siga as instruções na página de login para completar a autenticação

# Verificar a conta autenticada
az account show
```

**Dica:** Se o navegador não abrir automaticamente, use o login com código de dispositivo:

```bash
# Login alternativo usando código de dispositivo
az login --use-device-code

# Siga as instruções exibidas no terminal para completar a autenticação
```

### 📊 Configuração da Subscription

Configure a subscription padrão que será utilizada para o projeto.

```bash
# Listar todas as subscriptions disponíveis
az account list --output table

# Definir a subscription padrão (substitua SUBSCRIPTION_ID pelo ID desejado)
az account set --subscription <SUBSCRIPTION_ID>

# Ou usando o nome da subscription
az account set --subscription "Nome da Subscription"

# Confirmar a subscription ativa
az account show --output table
```

**Boas Práticas:**
- Sempre verifique qual subscription está ativa antes de criar recursos
- Documente o ID/nome da subscription utilizada no projeto
- Utilize tags para organizar recursos relacionados ao projeto

### ✅ Validação de Permissões

Verifique se sua conta possui as permissões necessárias para criar e gerenciar recursos.

```bash
# Listar resource groups disponíveis
az group list --output table

# Verificar permissões em um resource group específico
az role assignment list --resource-group <RESOURCE_GROUP_NAME> --output table

# Listar todas as permissões da conta atual
az role assignment list --assignee $(az account show --query user.name -o tsv) --output table
```

**Permissões mínimas recomendadas:**
- **Contributor** ou superior no Resource Group utilizado
- Permissões para criar e gerenciar Azure Functions
- Permissões para criar e gerenciar Storage Accounts (necessário para Azure Functions)

### 🧪 Teste de Configuração Local

Após configurar todas as ferramentas, teste o ambiente local.

```bash
# Criar um projeto de teste do Azure Functions
mkdir test-function && cd test-function

# Inicializar um novo projeto Azure Functions
func init --python

# Criar uma função HTTP de exemplo
func new --name HttpExample --template "HTTP trigger" --authlevel "anonymous"

# Executar a função localmente
func start

# Testar em outro terminal
curl http://localhost:7071/api/HttpExample?name=Azure

# Limpar após o teste
cd ..
rm -rf test-function
```

### 🚨 Troubleshooting - Problemas Comuns em WSL2

#### Problema: Erro de conectividade durante instalação
```bash
# Solução 1: Reiniciar WSL2
wsl --shutdown  # Executar no PowerShell/CMD do Windows

# Solução 2: Verificar DNS
cat /etc/resolv.conf
sudo nano /etc/resolv.conf  # Adicionar: nameserver 8.8.8.8
```

#### Problema: func command not found
```bash
# Verificar se o PATH está configurado corretamente
echo $PATH

# Reinstalar Azure Functions Core Tools
sudo apt-get remove azure-functions-core-tools-4
sudo apt-get install -y azure-functions-core-tools-4
```

#### Problema: Erro ao abrir navegador no az login
```bash
# Use o método alternativo com código de dispositivo
az login --use-device-code
```

#### Problema: Permissões insuficientes
```bash
# Verificar roles atribuídas
az role assignment list --assignee $(az account show --query user.name -o tsv)

# Solicitar permissões adequadas ao administrador da subscription
```

### 📚 Recursos Adicionais

- [Documentação Oficial do Azure CLI](https://docs.microsoft.com/cli/azure/)
- [Documentação do Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local)
- [Guia de Desenvolvimento Azure Functions com Python](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [WSL2 e Azure CLI - Boas Práticas](https://docs.microsoft.com/windows/wsl/)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre o processo de contribuição, padrões de código e boas práticas.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

> Para dúvidas, contribuições ou sugestões, abra uma [Issue](https://github.com/Jcnok/cpf-serverless-python/issues) ou consulte o arquivo de contribuição!
```
