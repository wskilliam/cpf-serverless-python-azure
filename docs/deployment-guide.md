# Guia de Deploy Automatizado

Este documento descreve o processo de deploy automatizado (CI/CD) para a aplicação de validação de CPF no Azure Functions.

## Visão Geral

O processo de deploy é gerenciado pelo GitHub Actions. Um workflow foi configurado para automatizar a verificação, o teste e a publicação da aplicação sempre que novas alterações forem enviadas para a branch `main`.

O pipeline está definido no arquivo `.github/workflows/deploy.yml`.

## Funcionamento do Pipeline

O pipeline é acionado automaticamente em qualquer `push` para a branch `main`. Ele consiste em dois jobs sequenciais:

### 1. `build-and-test`

Este job é responsável por garantir a qualidade e a integridade do código antes do deploy. Ele executa os seguintes passos:
- **Checkout do Código**: Baixa a versão mais recente do código do repositório.
- **Configuração do Ambiente**: Instala e configura a versão correta do Python (3.12.11).
- **Instalação de Dependências**: Utiliza o Poetry para instalar todas as dependências do projeto.
- **Execução dos Testes**: Roda a suíte completa de testes automatizados com `pytest`.

Se qualquer um desses passos falhar, o pipeline é interrompido, e o deploy não é realizado, prevenindo que código com problemas chegue ao ambiente de produção.

### 2. `deploy`

Este job só é executado se o job `build-and-test` for concluído com sucesso. Ele é responsável por publicar a aplicação no Azure.
- **Checkout do Código**: Baixa novamente o código para garantir um ambiente limpo.
- **Deploy no Azure Functions**: Utiliza a action `Azure/functions-action@v1` para enviar o pacote da aplicação para o Azure.

## Configuração Necessária

Para que o deploy funcione, é necessário configurar um secret no repositório do GitHub.

### 1. Obter o Publish Profile do Azure

O "Publish Profile" é um arquivo XML que contém as credenciais de deploy para a sua Function App.

1.  Acesse o [Portal da Azure](https://portal.azure.com/).
2.  Navegue até a sua **Function App**.
3.  No menu lateral, encontre a seção "Publicar" e clique em **Baixar perfil de publicação**.
4.  Isso fará o download de um arquivo com a extensão `.publishsettings`. Abra este arquivo em um editor de texto.

### 2. Configurar o Secret no GitHub

O conteúdo completo do arquivo `.publishsettings` deve ser adicionado como um secret no seu repositório GitHub.

1.  No seu repositório no GitHub, vá para **Settings** > **Secrets and variables** > **Actions**.
2.  Clique em **New repository secret**.
3.  No campo **Name**, insira `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`.
4.  No campo **Secret**, cole o conteúdo completo do arquivo `.publishsettings` que você baixou.
5.  Clique em **Add secret**.

### 3. Substituir o Nome da Aplicação no Workflow

No arquivo `.github/workflows/deploy.yml`, você precisa substituir o placeholder `<YOUR_FUNCTION_APP_NAME>` pelo nome real da sua Function App no Azure.

## Variáveis de Ambiente

Qualquer variável de ambiente necessária para a aplicação em produção (como chaves de API, strings de conexão, etc.) **não** deve ser armazenada no código. Em vez disso, elas devem ser configuradas diretamente no Azure:

1.  No Portal da Azure, acesse sua **Function App**.
2.  No menu lateral, vá para **Configuração** > **Configurações do aplicativo**.
3.  Adicione as variáveis de ambiente como "Novas configurações de aplicativo".
