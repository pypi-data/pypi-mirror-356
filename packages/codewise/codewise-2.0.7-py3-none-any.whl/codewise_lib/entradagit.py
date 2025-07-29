from git import Repo, GitCommandError
import os
import sys

def gerar_entrada_automatica(caminho_repo, caminho_saida, nome_branch):
    try:
        repo = Repo(caminho_repo, search_parent_directories=True)
        if nome_branch not in repo.heads:
            print(f"Branch local '{nome_branch}' não encontrada.", file=sys.stderr)
            return False
        branch_local = repo.heads[nome_branch]
        commits_pendentes = []

        if 'origin' in repo.remotes:
            try:
                repo.remotes.origin.fetch(prune=True)
                branch_remota_ref = f'origin/{branch_local.name}'
                commits_pendentes = list(repo.iter_commits(f"{branch_remota_ref}..{branch_local.name}"))
            except GitCommandError:
                default_branch_name = "main" if 'main' in repo.heads else 'master'
                print(f"AVISO: Branch '{branch_local.name}' não encontrada no remote. Comparando com a branch '{default_branch_name}'.", file=sys.stderr)
                commits_pendentes = list(repo.iter_commits(f"{default_branch_name}..{branch_local.name}"))
        else:
            print("AVISO: Remote 'origin' não configurado. Analisando os 2 últimos commits locais.", file=sys.stderr)
            commits_pendentes = list(repo.iter_commits(branch_local, max_count=2))

        if not commits_pendentes:
            print("Nenhum commit novo para analisar foi encontrado.", file=sys.stderr)
            return False

        commit_base = commits_pendentes[-1].parents[0] if commits_pendentes[-1].parents else None
        diff_completo = repo.git.diff(commit_base, commits_pendentes[0])
        
        entrada = [f"Analisando {len(commits_pendentes)} commit(s).\n\nMensagens de commit:\n"]
        for commit in reversed(commits_pendentes):
            entrada.append(f"- {commit.message.strip()}")
        entrada.append(f"\n{'='*80}\nDiferenças de código consolidadas a serem analisadas:\n{diff_completo}")

        with open(caminho_saida, "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write("\n".join(entrada))
        return True
    except Exception as e:
        print(f"Ocorreu um erro inesperado em 'entradagit.py': {e}", file=sys.stderr)
        return False

def obter_mudancas_staged(repo_path="."):
    """
    Verifica o estado do repositório para o modo lint.
    Retorna:
    - O 'diff' do código se houver mudanças no stage.
    - Uma string de AVISO se o stage estiver limpo mas o working dir tiver mudanças.
    - None se o repositório estiver totalmente limpo.
    """
    try:
        repo = Repo(repo_path, search_parent_directories=True)
        
        diff_staged = repo.git.diff('--cached')
        if diff_staged:
            return diff_staged

        diff_working_dir = repo.git.diff()
        if diff_working_dir:
            return "AVISO: Nenhuma mudança na 'staging area', mas existem modificações não adicionadas.\nUse 'git add <arquivo>' para prepará-las para a análise."

        return None
    except Exception as e:
        print(f"Erro em 'entradagit.py' ao obter staged changes: {e}", file=sys.stderr)
        return "FALHA: Erro ao interagir com o repositório Git."