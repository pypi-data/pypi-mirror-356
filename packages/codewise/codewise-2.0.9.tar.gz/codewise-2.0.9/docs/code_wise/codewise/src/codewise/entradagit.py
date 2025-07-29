from git import Repo, GitCommandError
import os
import sys

def gerar_entrada_automatica(caminho_repo, caminho_saida, nome_branch):
    try:
        repo = Repo(caminho_repo, search_parent_directories=True)
        branch_local = repo.heads[nome_branch]

        if 'origin' not in repo.remotes:
            print("AVISO: Remote 'origin' não configurado. Análise não pode prosseguir.", file=sys.stderr)
            return False

        print("Buscando atualizações do repositório remoto...", file=sys.stderr)
        repo.remotes.origin.fetch(prune=True)

        base_ref_str = ''
        branch_remota_str = f'origin/{branch_local.name}'

        # Verifica se a branch já existe no repositório remoto
        remote_branch_exists = any(ref.name == branch_remota_str for ref in repo.remotes.origin.refs)

        if remote_branch_exists:
            # Se a branch já existe, a base para o diff é a própria branch no remote.
            # Isso garante que estamos pegando apenas as novas atualizações.
            base_ref_str = branch_remota_str
            print(f"✅ Branch '{nome_branch}' já existe no remote. Analisando novos commits desde o último push.", file=sys.stderr)
        else:
            # Se a branch é nova, a base para o diff é a branch principal do remote.
            default_branch_name = "main" # Assume 'main' como padrão
            # Tenta encontrar a branch padrão do repo remoto
            for ref in repo.remotes.origin.refs:
                if ref.name in ['origin/main', 'origin/master']:
                    default_branch_name = ref.name.split('/')[-1]
                    break
            base_ref_str = f'origin/{default_branch_name}'
            print(f"✅ Branch '{nome_branch}' é nova. Comparando com a branch principal remota ('{default_branch_name}').", file=sys.stderr)

        commits_pendentes = list(repo.iter_commits(f"{base_ref_str}..{branch_local.name}"))
        if not commits_pendentes:
            print("Nenhum commit novo para analisar foi encontrado.", file=sys.stderr)
            return False

        # O diff agora é sempre entre a base correta e a ponta da branch local
        diff_completo = repo.git.diff(f'{base_ref_str}..{branch_local.name}')
        
        entrada = [f"Analisando {len(commits_pendentes)} novo(s) commit(s).\n\nMensagens de commit:\n"]
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