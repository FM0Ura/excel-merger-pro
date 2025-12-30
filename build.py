import PyInstaller.__main__
import shutil
import os
import re
from pathlib import Path

# --- Configurações do Projeto ---
APP_NAME = "ExcelMergerPro"
ENTRY_POINT = "src/main.py"
ICON_PATH = "assets/app.ico"
REQ_FILE = "requirements.txt"

def get_hidden_imports_from_requirements():
    """
    Lê o requirements.txt tentando diferentes codificações (UTF-8, UTF-16)
    para evitar erros comuns de arquivos gerados no Windows/PowerShell.
    """
    imports = []
    
    if not os.path.exists(REQ_FILE):
        print(f"⚠️ Aviso: {REQ_FILE} não encontrado. Nenhuma dependência externa será forçada.")
        return []

    print(f"--- Lendo dependências de {REQ_FILE} ---")
    
    content = ""
    # Estratégia de Fallback de Codificação
    encodings_to_try = ['utf-8', 'utf-16', 'cp1252']
    
    for enc in encodings_to_try:
        try:
            with open(REQ_FILE, 'r', encoding=enc) as f:
                content = f.read()
            print(f"   (Arquivo lido com sucesso usando codificação: {enc})")
            break # Sucesso, sai do loop
        except UnicodeError:
            continue # Tenta o próximo
    
    if not content:
        print("❌ Erro Crítico: Não foi possível ler o requirements.txt com nenhuma codificação padrão.")
        return []

    # Processa as linhas lidas
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Remove versionamento (ex: 'pandas>=1.0' vira 'pandas')
        package_name = re.split(r'[=<>]|~', line)[0].strip()
        
        if package_name:
            imports.append(package_name)

    # Overrides manuais (Pacotes com nome de import diferente do pip)
    manual_overrides = ['PIL'] 
    
    # Remove duplicatas e retorna
    detected = list(set(imports + manual_overrides))
    for lib in detected:
        print(f"   -> Detectado: {lib}")
        
    return detected

def build():
    print(f"\n🚀 Iniciando Build Automático: {APP_NAME}\n")
    
    # 1. Limpeza
    if os.path.exists("dist"): shutil.rmtree("dist")
    if os.path.exists("build"): shutil.rmtree("build")
    if os.path.exists(f"{APP_NAME}.spec"): os.remove(f"{APP_NAME}.spec")

    # 2. Ícone
    icon_option = []
    if os.path.exists(ICON_PATH):
        icon_option = [f'--icon={ICON_PATH}']
    else:
        print(f"⚠️ Ícone não encontrado em {ICON_PATH}. Usando padrão.")

    # 3. Assets do CustomTkinter
    import customtkinter
    ctk_path = os.path.dirname(customtkinter.__file__)
    
    # 4. Imports Dinâmicos
    dynamic_imports = get_hidden_imports_from_requirements()
    hidden_import_args = [f'--hidden-import={lib}' for lib in dynamic_imports]

    # 5. Argumentos PyInstaller
    args = [
        ENTRY_POINT,
        f'--name={APP_NAME}',
        '--noconsole',
        '--onefile',
        '--clean',
        f'--add-data={ICON_PATH}{os.pathsep}assets',
        f'--add-data={ctk_path}{os.pathsep}customtkinter', 
    ] + icon_option + hidden_import_args

    # 6. Execução
    print("\n--- Executando PyInstaller ---")
    PyInstaller.__main__.run(args)
    
    print(f"\n✅ SUCESSO! O executável está pronto em: dist/{APP_NAME}.exe")

if __name__ == "__main__":
    build()