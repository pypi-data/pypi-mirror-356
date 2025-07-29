import os
import sys
import stat
import argparse

PRE_PUSH_CONTENT = """#!/bin/sh
set -e
echo "--- [HOOK PRE-PUSH CodeWise ATIVADO] ---"
codewise-pr
echo "--- [HOOK PRE-PUSH CodeWise CONCLUÍDO] ---"
exit 0
"""

PRE_COMMIT_CONTENT = """#!/bin/sh
set -e
echo "--- [HOOK PRE-COMMIT CodeWise ATIVADO] ---"
codewise-lint
echo "--- [HOOK PRE-COMMIT CodeWise CONCLUÍDO] ---"
exit 0
"""

def install_hook(hook_name, hook_content, repo_root):
    hooks_dir = os.path.join(repo_root, '.git', 'hooks')
    if not os.path.isdir(hooks_dir):
        print(f"❌ Erro: Diretório de hooks do Git não encontrado em '{hooks_dir}'.", file=sys.stderr)
        return False
    
    hook_path = os.path.join(hooks_dir, hook_name)
    try:
        with open(hook_path, 'w', newline='\n') as f:
            f.write(hook_content)
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
        print(f"✅ Hook '{hook_name}' instalado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao instalar o hook '{hook_name}': {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Instalador de hooks do CodeWise.")
    parser.add_argument('--commit', action='store_true', help='Instala o hook pre-commit.')
    parser.add_argument('--push', action='store_true', help='Instala o hook pre-push.')
    parser.add_argument('--all', action='store_true', help='Instala ambos os hooks.')
    args = parser.parse_args()

    print("🚀 Iniciando configuração de hooks do CodeWise...")
    repo_root = os.getcwd()
    
    if not any([args.commit, args.push, args.all]):
        print("Nenhum hook especificado. Use --commit, --push, ou --all.", file=sys.stderr)
        sys.exit(1)

    if args.commit or args.all:
        install_hook('pre-commit', PRE_COMMIT_CONTENT, repo_root)

    if args.push or args.all:
        install_hook('pre-push', PRE_PUSH_CONTENT, repo_root)

    print("\n🎉 Configuração concluída!")

if __name__ == "__main__":
    main()