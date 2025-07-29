
CodeWise- é uma ferramenta de linha de comando que utiliza o poder de modelos de linguagem (via CrewAI) para automatizar a criação e o enriquecimento de Pull Requests no GitHub.

## Funcionalidades Principais
- **Geração de Título:** Cria títulos de PR claros e concisos seguindo o padrão *Conventional Commits*.
- **Geração de Descrição:** Escreve descrições detalhadas baseadas nas alterações do código.
- **Análise Técnica:** Posta um comentário no PR com um resumo executivo das melhorias de arquitetura, aderência a princípios S.O.L.I.D. e outros pontos de qualidade.
- **Automação Completa:** Integra-se ao seu fluxo de trabalho Git para rodar automaticamente a cada `git push`.

## Pré-requisitos para serem instalados antes de tudo

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em seu sistema:
1.  **Python** (versão 3.11 ou superior)
2.  **Git**
3.  **GitHub CLI (`gh`)**: Após instalar, logue com sua conta do GitHub executando "gh auth login" no seu terminal. (só precisa uma vez no pc)

========================================================COMO INSTALAR======================================================================================================================
#Após instalar os pré requisitos, aqui está como funciona a criação do ambiente virtual no repositório que for usar, para evitar conflitos das dependências de lib.

1) - Você fará isso apenas uma vez no repositório novo --> Escolha um repositório git já configurado, abra o terminal na raiz e comece:

# Crie e Utilize um Ambiente Virtual 
Para evitar conflitos com outros projetos Python, é altamente recomendado usar um ambiente virtual. Pense nisso apenas para este projeto, mantendo seu sistema principal limpo.

1.1. Para Criar o Ambiente:
Execute este comando uma única vez. Ele cria uma pasta chamada .venv com uma instalação limpa do Python dentro.

py -m venv .venv / python3 -m venv .venv (Linux)

1.2. Para Ativar o Ambiente:
Sempre que for trabalhar no projeto, você precisa ativar o ambiente.

.\.venv\Scripts\activate ou  source venv/bin/activate

Você saberá que funcionou porque o início da linha do seu terminal mudará, mostrando (.venv) antes do caminho ou o nome que foi escolhido.

1.3. Para Desativar o Ambiente :

Quando terminar de usar, você pode desativar o ambiente simplesmente digitando:

deactivate

O (.venv) desaparecerá do seu terminal, indicando que você voltou ao seu sistema normal sem a lib.

=========================================================================================================================================================================================
================================================================Como USAR================================================================================================================

Para cada repositório Git em que você desejar usar a automação, basta fazer uma configuração inicial.

**Passo 1: vá até o seu Repositório**

# Exemplo: configurando para o projeto C_lib
cd /caminho/para/seu/C_lib

**Instale a lib com o comando "pip install codewise" ou "py -m pip install codewise" (pode demorar um pouco aqui)**

após instalar a lib, você pode confirmar se está tudo certo com o comando codewise-help!

depois disso basta apenas ativar os pré-hooks automatizados com o comando codewise-init --all e pronto

**Passo 2: Ative a Automação**

# Para ativar AMBAS as automações 
codewise-init --all

Você verá uma mensagem de sucesso confirmando que a automação está ativa.
*(**Opcional:** use o comando com `--commit` para ativar apenas a análise rápida ou `--push` para ativar apenas a automação de PR).*

Após estes passos, a ferramenta estará instalada e pronta para ser configurada em qualquer um dos seus projetos 
(idealmente sempre crie o ambiente virtual na pasta raiz toda vez que for criar um repositório novo para usar a ferramenta e evitar conflitos).
=========================================================================================================================================================================================
# CONFIG DO .ENV no repositório

 Configuração obrigatória

Antes de usar o CodeWise, você precisa configurar sua chave da API do Google Gemini.

1. No repositório que você está desenvolvendo, crie um arquivo chamado `.env`
2. Copie e cole e de um CTRL+S para salvar:

GEMINI_API_KEY=sua-chave do gemini
MODEL_NAME=gemini/gemini-2.0-flash

Você pode criar esse arquivo com:

- Windows:

  notepad .env

-Linux/macOS:

touch .env && nano .env

3. Após salvar, está tudo pronto. Considerando que seu novo repositório já está corretamente configurado com as branchs para PR sem conter apenas a default (main/master)
=========================================================================================================================================================================================

## DICAS : se quiser criar um novo repositório na máquina pelo prompt o gh ajuda com alguns comandos também :

( mkdir MeuNovoProjeto 
cd MeuNovoProjeto
git init
gh repo create MeuNovoProjeto --public --source=. --remote=origin
# (Crie seu primeiro arquivo, ex: README.md) echo > README.md
git add .
git commit -m "Primeiro commit"
git push --set-upstream origin main (ou master, dependendo do seu Git)
nova branch: git checkout -b nome-da-branch enviar para remoto: git push -u origin nome-da-branch
)
=========================================================================================================================================================================================

## Fluxo de Trabalho do Dia a Dia

1.  Trabalhe normalmente em uma branch separada (ex: `minha-feature`).
2.  Adicione suas alterações para o próximo commit:
    ```
    git add .
    ```
3.  Faça o commit:
    ```
    git commit -m "feat: implementa novo recurso X"
    ```
    Neste momento, o **hook `pre-commit` será ativado**. Você verá a análise rápida do `codewise-lint` aparecer no seu terminal com sugestões de melhoria antes mesmo de o commit ser finalizado.

4.  Envie suas alterações para o GitHub:
    ```
    git push
    ```
 se for a primeira vez use com --no-verify para não usar o programa ainda! (git push origin master --no-verify) (git push --set-upstream origin teste )
    Agora, o **hook `pre-push` será ativado**. O `codewise-pr` irá criar ou atualizar seu Pull Request no GitHub com título, descrição e um comentário de análise técnica com sugestões e melhorias, tudo gerado por IA.

---
*Este projeto foi desenvolvido como uma ferramenta para otimizar o processo de code review e documentação de software.*