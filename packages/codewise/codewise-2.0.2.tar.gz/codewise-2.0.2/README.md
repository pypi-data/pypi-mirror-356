
CodeWise- é uma ferramenta de linha de comando que utiliza o poder de modelos de linguagem (via CrewAI) para automatizar a criação e o enriquecimento de Pull Requests no GitHub.

## Funcionalidades Principais
- **Geração de Título:** Cria títulos de PR claros e concisos seguindo o padrão *Conventional Commits*.
- **Geração de Descrição:** Escreve descrições detalhadas baseadas nas alterações do código.
- **Análise Técnica:** Posta um comentário no PR com um resumo executivo das melhorias de arquitetura, aderência a princípios S.O.L.I.D. e outros pontos de qualidade.
- **Automação Completa:** Integra-se ao seu fluxo de trabalho Git para rodar automaticamente a cada `git push`.

## Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em seu sistema:
1.  **Python** (versão 3.11 ou superior)
2.  **Git**
3.  **GitHub CLI (`gh`)**: Após instalar, autentique-se com o GitHub executando `gh auth login` no seu terminal.

####################### Instalação (Apenas uma vez) #########################################

Para instalar a ferramenta CodeWise-PR e suas dependências no seu computador, siga estes passos:

1.  Clone este repositório:
    ```
    git clone [https://github.com/bs20242/cwb.git](https://github.com/bs20242/cwb.git) CodeWise
    ```
2.  Navegue até a pasta do projeto:
    ```
    win: cd C:\Users\SeuUsuario\CodeWise
    linux: cd /c/Users/SeuUsuario/CodeWise (use: git config --global core.autocrlf true <caso o git no Linux/WSL esteja pegando arquivos demais no git status>)

Passo 2.1: Crie e Utilize um Ambiente Virtual (Recomendado)
Para evitar conflitos com outros projetos Python, é altamente recomendado usar um ambiente virtual. Pense nisso apenas para este projeto, mantendo seu sistema principal limpo.

 2.1.1. Para Criar o Ambiente:
Execute este comando uma única vez. Ele cria uma pasta chamada .venv com uma instalação limpa do Python dentro.

py -m venv .venv / python3 -m venv .venv (Linux)

 2.1.2. Para Ativar o Ambiente:
Sempre que for trabalhar no projeto, você precisa ativar o ambiente.

.\.venv\Scripts\activate ou  source venv/bin/activate

Você saberá que funcionou porque o início da linha do seu terminal mudará, mostrando (.venv) antes do caminho.

 2.1.3. Para Desativar o Ambiente :
Quando terminar de trabalhar, você pode desativar o ambiente simplesmente digitando:

deactivate

O (.venv) desaparecerá do seu terminal, indicando que você voltou ao seu sistema normal.

# No Windows (PowerShell/CMD) ou WSL/Git bash:

3.  Instale as dependências e a ferramenta:
    ```

    # Instala a ferramenta e os comandos 'codewise-pr' e 'codewise-init', ao final também instala os requirements.txt

    py -m pip install -e . / python3 -m pip install -e .

    ```
## se quiser criar um novo repositorio na máquina pelo prompt:

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
#############################################################################################################################################
Após estes passos, a ferramenta estará instalada e pronta para ser configurada em qualquer um dos seus projetos.

######################## Como Usar #######################################

Para cada repositório Git em que você desejar usar a automação, basta fazer uma configuração inicial de 10 segundos.

#### **Passo 1: Navegue até o seu Repositório**

```
# Exemplo: configurando para o projeto C_lib
cd /caminho/para/seu/C_lib
```

#### **Passo 2: Ative a Automação**

# Para ativar AMBAS as automações (Recomendado)
codewise-init --all
```
Você verá uma mensagem de sucesso confirmando que a automação está ativa.
*(**Opcional:** use `--commit` para ativar apenas a análise rápida ou `--push` para ativar apenas a automação de PR).*

Antes de usar a ferramenta, você precisa configurar sua chave de API do Google Gemini. Este processo é feito localmente e de forma segura, sem expor sua chave no código.

 Crie o Arquivo de Ambiente (.env)

A chave de API é lida de um arquivo chamado `.env` localizado na pasta principal da biblioteca. Primeiro, navegue até o diretório correto. A partir da raiz do projeto, o caminho é:

"cd docs/code_wise/codewise/src/codewise" há um exemplo de .env em formato txt que você pode copiar o conteúdo dentro.

abra o terminal no local onde se encontra o crew.py, após ter copiado o conteúdo do exemplo use: "notepad .env"/"touch .env" (Linux) 
 aceite criar um novo arquivo e cole o conteúdo dentro, e adicione sua API key do gemini.


## Fluxo de Trabalho do Dia a Dia
Com a configuração concluída, seu fluxo de trabalho se torna mais inteligente:

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
    Agora, o **hook `pre-push` será ativado**. O `codewise-pr` irá criar ou atualizar seu Pull Request no GitHub com título, descrição e um comentário de análise técnica, tudo gerado por IA.

---
*Este projeto foi desenvolvido como uma ferramenta para otimizar o processo de code review e documentação de software.*