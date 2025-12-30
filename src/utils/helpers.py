import sys
import os
import re # <--- Importante

def resource_path(relative_path: str) -> str:
    """ (Código existente mantido...) """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def sanitize_filename(filename: str) -> str:
    """
    Remove caracteres proibidos em nomes de arquivos no Windows/Linux.
    Substitui: < > : " / \ | ? * por nada.
    """
    # Regex para remover caracteres ilegais
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove espaços extras no inicio/fim
    return cleaned.strip()