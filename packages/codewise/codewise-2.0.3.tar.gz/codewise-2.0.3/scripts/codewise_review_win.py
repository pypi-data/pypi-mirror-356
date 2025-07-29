
import subprocess
import os
import sys
import re
import json

# ===================================================================
# SEÇÃO DE FUNÇÕES AUXILIARES (COMPARTILHADAS)
# ===================================================================

def run_codewise_mode(mode, repo_path, branch_name):
    """Executa a IA como um MÓDULO e captura a saída, resolvendo o ImportError."""
    print(f"\n--- *! Executando IA [modo: {mode}] !* ---")
    
    # CORREÇÃO PRINCIPAL: Executamos a 'lib' como um módulo com 'py -m'.
    # Isso faz o Python reconhecer a estrutura do pacote e as importações relativas.
    # O nome do módulo é 'codewise_lib.main' porque no setup.py definimos que o pacote 'codewise_lib'
    # está no diretório '.../src/codewise', onde o main.py se encontra.
    command = [
        sys.executable, "-m", "codewise_lib.main",
        "--repo", repo_path,
        "--branch", branch_name,
        "--mode", mode
    ]
    try:
        # A pasta raiz do projeto precisa estar no path para o Python encontrar o módulo
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{os.path.dirname(os.path.dirname(__file__))}{os.pathsep}{env.get('PYTHONPATH', '')}"
        
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore', env=env)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ FALHA no modo '{mode}':\n--- Erro do Subprocesso ---\n{e.stderr}\n--------------------------", file=sys.stderr)
        return None

def obter_branch_padrao_remota(repo_path):
    try:
        remote_url_result = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], cwd=repo_path, text=True, encoding='utf-8').strip()
        match = re.search(r'github\.com/([^/]+/[^/]+?)(\.git)?$', remote_url_result)
        if not match: return "main"
        repo_slug = match.group(1)
        result = subprocess.check_output(
            ["gh", "repo", "view", repo_slug, "--json", "defaultBranchRef", "-q", ".defaultBranchRef.name"],
            text=True, encoding='utf-8', stderr=subprocess.DEVNULL
        ).strip()
        if not result: return "main"
        print(f"✅ Branch principal detectada no GitHub: '{result}'", file=sys.stderr)
        return result
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "main"

def extrair_titulo_valido(texto):
    match = re.search(r"(feat|fix|refactor|docs):\s.+", texto, re.IGNORECASE)
    if match: return match.group(0).strip()
    return None

def obter_pr_aberto_para_branch(branch, repo_dir):
    try:
        result = subprocess.run(["gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number"], check=True, capture_output=True, text=True, encoding='utf-8', cwd=repo_dir)
        return json.loads(result.stdout)[0]['number'] if json.loads(result.stdout) else None
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None

# ===================================================================
# LÓGICA DO COMANDO 'codewise-lint' (PARA PRE-COMMIT)
# ===================================================================
def main_lint():
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    repo_path = os.getcwd()
    try:
        current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], encoding='utf-8', cwd=repo_path).strip()
    except Exception:
        current_branch = ""
    print("--- 🔍 Executando análise rápida pré-commit do CodeWise ---", file=sys.stderr)
    sugestoes = run_codewise_mode("lint", repo_path, current_branch)
    if sugestoes is None:
        print("--- ❌ A análise rápida falhou. Verifique os erros acima. ---", file=sys.stderr)
        sys.exit(1)
    elif "Nenhum problema aparente detectado." in sugestoes:
        print("--- ✅ Nenhuma sugestão crítica. Bom trabalho! ---", file=sys.stderr)
    else:
        print("\n--- 💡 SUGESTÕES DE MELHORIA ---", file=sys.stderr)
        print(sugestoes, file=sys.stderr)
        print("---------------------------------", file=sys.stderr)

# ===================================================================
# LÓGICA DO COMANDO 'codewise-pr' (PARA PRE-PUSH)
# ===================================================================
def main_pr():

    if not shutil.which("gh"):
        print("❌ Erro: A GitHub CLI ('gh') não foi encontrada no seu sistema.", file=sys.stderr)
        print("   Por favor, instale-a a partir de: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)

    os.environ['PYTHONIOENCODING'] = 'utf-8'
    repo_path = os.getcwd()
    print(f"📍 Analisando o repositório em: {repo_path}", file=sys.stderr)
    
    try:
        current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], encoding='utf-8', cwd=repo_path).strip()
    except Exception as e:
        sys.exit(f"❌ Erro ao detectar branch Git: {e}")

    base_branch_target = obter_branch_padrao_remota(repo_path)
    if current_branch == base_branch_target:
        sys.exit(f"❌ A automação não pode ser executada na branch principal ('{base_branch_target}').")

    print("\n--- 🤖 Executando IA para documentação do PR ---", file=sys.stderr)
    titulo_bruto = run_codewise_mode("titulo", repo_path, current_branch)
    descricao = run_codewise_mode("descricao", repo_path, current_branch)
    analise_tecnica = run_codewise_mode("analise", repo_path, current_branch)

    if not all([titulo_bruto, descricao, analise_tecnica]):
        sys.exit("❌ Falha ao gerar todos os textos necessários da IA.")

    titulo_final = extrair_titulo_valido(titulo_bruto) or f"feat: Modificações da branch {current_branch}"
    print(f"✔️ Título definido para o PR: {titulo_final}", file=sys.stderr)

    temp_analise_path = os.path.join(repo_path, ".codewise_analise_temp.txt")
    with open(temp_analise_path, "w", encoding='utf-8') as f: f.write(analise_tecnica)

    pr_numero = obter_pr_aberto_para_branch(current_branch, repo_path)

    if pr_numero:
        print(f"⚠️ PR #{pr_numero} já existente. Acrescentando nova análise...", file=sys.stderr)
        try:
            # 1. Busca a descrição atual do PR
            print("   - Buscando descrição existente...", file=sys.stderr)
            descricao_antiga_raw = subprocess.check_output(
                ["gh", "pr", "view", str(pr_numero), "--json", "body"],
                cwd=repo_path, text=True, encoding='utf-8'
            )
            descricao_antiga = json.loads(descricao_antiga_raw).get("body", "")

            # 2. Prepara a nova entrada com data e hora
            from datetime import datetime
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            nova_entrada_descricao = (
                f"\n\n---\n\n"
                f"**🔄 Atualização em {timestamp}**\n\n"
                f"{descricao}"
            )

            # 3. Concatena a descrição antiga com a nova
            body_final = descricao_antiga + nova_entrada_descricao

            # 4. Edita o PR com o corpo completo
            subprocess.run(["gh", "pr", "edit", str(pr_numero), "--title", titulo_final, "--body", body_final], check=False, text=True, capture_output=True, encoding='utf-8', cwd=repo_path)
            print(f"✅ Descrição do PR #{pr_numero} atualizada com novas informações.")

        except Exception as e:
            # Se falhar ao buscar a descrição antiga, apenas substitui para não quebrar o fluxo
            print(f"⚠️ Não foi possível buscar a descrição antiga. Substituindo pela nova. Erro: {e}", file=sys.stderr)
            subprocess.run(["gh", "pr", "edit", str(pr_numero), "--title", titulo_final, "--body", descricao], check=False, text=True, capture_output=True, encoding='utf-8', cwd=repo_path)

    else:
        print("🆕 Nenhum PR aberto. Criando Pull Request...", file=sys.stderr)
        try:
            result = subprocess.run(["gh", "pr", "create", "--base", base_branch_target, "--head", current_branch, "--title", titulo_final, "--body", descricao], check=True, capture_output=True, text=True, encoding='utf-8', cwd=repo_path)
            pr_url = result.stdout.strip()
            match = re.search(r"/pull/(\d+)", pr_url)
            if match: pr_numero = match.group(1)
            else: raise Exception(f"Não foi possível extrair o número do PR da URL: {pr_url}")
            print(f"✅ PR #{pr_numero} criado: {pr_url}", file=sys.stderr)
        except Exception as e:
            os.remove(temp_analise_path); sys.exit(f"❌ Falha ao criar PR: {e}")

    if pr_numero:
        print(f"💬 Comentando análise técnica no PR #{pr_numero}...", file=sys.stderr)
        try:
            subprocess.run(["gh", "pr", "comment", str(pr_numero), "--body-file", temp_analise_path], check=True, capture_output=True, text=True, encoding='utf-8', cwd=repo_path)
            print("✅ Comentário postado com sucesso.", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"❌ Falha ao comentar no PR: {e.stderr}", file=sys.stderr)
        finally:
            print("🧹 Limpando arquivo temporário...", file=sys.stderr); os.remove(temp_analise_path)