import polars as pl
import logging
import time
from pathlib import Path
from typing import List, Callable, Optional

class ExcelHandler:
    """
    Gerencia operações de I/O e transformação de dados Excel.
    """
    
    @staticmethod
    def validate_paths(file_paths: List[str]) -> None:
        # Tech Lead Note: Removemos a restrição de "exatamente 3".
        # Apenas garantimos que há pelo menos 1 arquivo e que são .xlsx
        if not file_paths:
            raise ValueError("Nenhum arquivo foi selecionado.")
        
        for path in file_paths:
            if Path(path).suffix.lower() != '.xlsx':
                raise ValueError(f"Arquivo inválido: {Path(path).name}. Apenas .xlsx é permitido.")

    @classmethod
    def process_merge(cls, file_paths: List[str], output_path: str, on_progress: Optional[Callable[[float, str], None]] = None) -> float:
        start_time = time.time()
        dfs: List[pl.DataFrame] = []

        logging.info(f"--- Iniciando Job de Merge com {len(file_paths)} arquivos ---")

        # Etapa 1: Leitura
        total_files = len(file_paths)
        
        for idx, file_path in enumerate(file_paths):
            p_name = Path(file_path).name
            logging.info(f"Lendo: {p_name}")
            
            if on_progress:
                # Progresso proporcional à quantidade de arquivos
                progress_step = 0.7 / total_files 
                current_prog = (idx * progress_step)
                on_progress(current_prog, f"Lendo ({idx+1}/{total_files}): {p_name}...")

            try:
                # Lê o Excel
                df = pl.read_excel(file_path)
                
                # --- REQUISITO: Converter TUDO para Texto ---
                # Isso padroniza os dados e evita erros de conflito de tipos (Int vs String)
                df = df.select(pl.all().cast(pl.String))
                
                # --- REQUISITO: Log das Colunas ---
                logging.info(f"[{p_name}] Colunas detectadas: {df.columns}")
                
                dfs.append(df)
            except Exception as e:
                logging.error(f"Falha ao processar {p_name}: {e}")
                raise e

        # Etapa 2: Processamento
        if on_progress: on_progress(0.75, "Unificando DataFrames...")
        
        try:
            # Concatenação vertical relaxada (agora que tudo é texto, é mais seguro)
            final_df = pl.concat(dfs, how="vertical")
        except Exception as e:
            logging.error(f"Erro de Concatenação: {e}")
            raise ValueError("Erro ao unir arquivos. Verifique os logs para ver divergência de colunas.") from e

        # Etapa 3: Escrita
        if on_progress: on_progress(0.90, "Escrevendo arquivo final...")
        logging.info(f"Salvando em: {output_path}")
        
        final_df.write_excel(output_path)

        total_time = time.time() - start_time
        logging.info(f"Job finalizado com sucesso em {total_time:.2f}s")
        
        if on_progress: on_progress(1.0, "Pronto!")
        
        return total_time