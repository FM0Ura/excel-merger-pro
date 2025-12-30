import logging
from pathlib import Path

def setup_logger() -> None:
    # Garante que a pasta logs existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(module)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app_execution.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )