import sys
from pathlib import Path

# Adiciona o diretório raiz ao path do Python para resolver imports corretamente
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from src.utils.logger_config import setup_logger
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    setup_logger()
    app = MainWindow()
    app.mainloop()