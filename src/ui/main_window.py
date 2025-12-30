import customtkinter as ctk
import threading
import os
from tkinter import filedialog, messagebox
from typing import List
from src.services.excel_handler import ExcelHandler
from src.utils.helpers import resource_path, sanitize_filename

class MainWindow(ctk.CTk):
    # --- Paleta de Cores (Mantida) ---
    COLOR_BG = "#1a1a1a"
    COLOR_FRAME = "#2b2b2b"
    COLOR_ACCENT = "#3B8ED0"
    COLOR_SUCCESS = "#2CC985"
    COLOR_TEXT = "#E0E0E0"
    COLOR_INPUT_BG = "#343638"
    
    def __init__(self):
        super().__init__()
        self._configure_window()
        self._init_variables()
        self._build_layout()

    def _configure_window(self):
        self.title("Excel Merger Enterprise")
        self.geometry("700x650")
        
        try:
            icon_path = resource_path("assets/app.ico")
            self.iconbitmap(icon_path)
        except Exception:
            pass

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue") 
        self.configure(fg_color=self.COLOR_BG)

    def _init_variables(self):
        self.selected_files: List[str] = []
        self.output_folder: str = ""

    def _build_layout(self):
        self.card = ctk.CTkFrame(
            self, 
            fg_color=self.COLOR_FRAME, 
            corner_radius=15,
            border_width=1,
            border_color="#404040"
        )
        self.card.pack(fill="both", expand=True, padx=30, pady=30)

        self._build_header()
        self._build_selection_area()
        self._build_config_area()
        self._build_action_area()

    def _build_header(self):
        title_lbl = ctk.CTkLabel(
            self.card, 
            text="MERGER PRO", 
            font=("Segoe UI", 28, "bold"),
            text_color=self.COLOR_TEXT
        )
        title_lbl.pack(pady=(30, 5))

        subtitle_lbl = ctk.CTkLabel(
            self.card, 
            text="Ferramenta Unificada de Processamento de Dados", 
            font=("Segoe UI", 12),
            text_color="gray"
        )
        subtitle_lbl.pack(pady=(0, 10))
        
        ctk.CTkProgressBar(self.card, height=2, progress_color=self.COLOR_ACCENT).pack(fill="x", padx=100)

    def _build_selection_area(self):
        self.files_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.files_frame.pack(pady=(20, 10), fill="x", padx=40)

        ctk.CTkLabel(self.files_frame, text="1. Entrada de Dados", font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x")

        self.btn_select = ctk.CTkButton(
            self.files_frame,
            text="📂 SELECIONAR ARQUIVOS (Múltiplos)", # Texto atualizado
            command=self._select_files,
            height=45,
            corner_radius=8,
            fg_color="transparent",
            border_width=2,
            border_color=self.COLOR_ACCENT,
            text_color=self.COLOR_ACCENT,
            hover_color=("#3B8ED0", "#1f538d")
        )
        self.btn_select.pack(fill="x", pady=5)

        self.lbl_file_count = ctk.CTkLabel(
            self.files_frame, 
            text="Nenhum arquivo selecionado",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.lbl_file_count.pack()

    def _build_config_area(self):
        self.config_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.config_frame.pack(pady=10, fill="x", padx=40)
        
        ctk.CTkLabel(self.config_frame, text="2. Configuração de Saída", font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", pady=(0, 5))

        self.config_frame.columnconfigure(0, weight=1)
        self.config_frame.columnconfigure(1, weight=2)

        self.btn_folder = ctk.CTkButton(
            self.config_frame,
            text="Selecionar Pasta Destino",
            command=self._select_output_folder,
            height=35,
            fg_color="#404040",
            hover_color="#505050"
        )
        self.btn_folder.pack(fill="x", pady=5)
        
        self.lbl_folder_path = ctk.CTkLabel(
            self.config_frame,
            text="Nenhuma pasta selecionada",
            text_color="gray",
            font=("Segoe UI", 11),
            anchor="w"
        )
        self.lbl_folder_path.pack(fill="x")

        ctk.CTkLabel(self.config_frame, text="Nome do Arquivo Final:", font=("Segoe UI", 12), anchor="w").pack(fill="x", pady=(10, 0))
        
        self.entry_filename = ctk.CTkEntry(
            self.config_frame,
            placeholder_text="Ex: relatorio_consolidado",
            height=35,
            fg_color=self.COLOR_INPUT_BG,
            border_color="#555"
        )
        self.entry_filename.pack(fill="x", pady=5)

    def _build_action_area(self):
        self.action_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.action_frame.pack(side="bottom", fill="x", padx=40, pady=30)

        self.btn_run = ctk.CTkButton(
            self.action_frame,
            text="PROCESSAR E SALVAR",
            command=self._start_thread,
            state="disabled",
            height=55,
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            fg_color=self.COLOR_FRAME,
            border_width=1,
            border_color="#555"
        )
        self.btn_run.pack(fill="x", pady=(0, 15))

        self.progress = ctk.CTkProgressBar(self.action_frame, height=8, progress_color=self.COLOR_SUCCESS)
        self.progress.pack(fill="x")
        self.progress.set(0)
        
        self.lbl_status = ctk.CTkLabel(self.action_frame, text="Aguardando configuração...", font=("Segoe UI", 11))
        self.lbl_status.pack(pady=(5, 0))

    # --- Lógica Atualizada ---

    def _select_files(self):
        paths = filedialog.askopenfilenames(
            title="Selecione os arquivos Excel",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if paths:
            self.selected_files = list(paths)
            self._validate_ready_state()

    def _select_output_folder(self):
        folder = filedialog.askdirectory(title="Selecione onde salvar")
        if folder:
            self.output_folder = folder
            display_path = folder if len(folder) < 40 else ".../" + os.path.basename(folder)
            self.lbl_folder_path.configure(text=display_path, text_color=self.COLOR_ACCENT)
            self._validate_ready_state()

    def _validate_ready_state(self):
        count = len(self.selected_files)
        has_folder = bool(self.output_folder)
        
        # Lógica flexível: Apenas requer mais que 0 arquivos
        if count > 0:
            self.lbl_file_count.configure(text=f"✔ {count} arquivos carregados", text_color=self.COLOR_SUCCESS)
        else:
            self.lbl_file_count.configure(text="Nenhum arquivo selecionado", text_color="gray")

        # Libera botão Run se houver arquivos e pasta de saída
        if count > 0 and has_folder:
            self.btn_run.configure(state="normal", fg_color=self.COLOR_ACCENT, text_color="white", border_width=0)
            self.lbl_status.configure(text="Pronto para processar")
        else:
            self.btn_run.configure(state="disabled", fg_color=self.COLOR_FRAME, border_width=1)
            
            if count == 0:
                self.lbl_status.configure(text="Selecione os arquivos de entrada")
            elif not has_folder:
                self.lbl_status.configure(text="Selecione a pasta de destino")

    def _start_thread(self):
        raw_name = self.entry_filename.get()
        safe_name = sanitize_filename(raw_name)

        if not safe_name:
            messagebox.showwarning("Atenção", "Digite um nome válido para o arquivo.")
            return

        if raw_name != safe_name:
            self.entry_filename.delete(0, "end")
            self.entry_filename.insert(0, safe_name)

        if not safe_name.lower().endswith(".xlsx"):
            safe_name += ".xlsx"

        full_path = os.path.join(self.output_folder, safe_name)

        self._lock_ui(True)
        threading.Thread(target=self._run_logic, args=(full_path,), daemon=True).start()

    def _run_logic(self, output_file):
        try:
            def update_ui(val, msg):
                self.progress.set(val)
                self.lbl_status.configure(text=msg)
            
            duration = ExcelHandler.process_merge(self.selected_files, output_file, on_progress=update_ui)
            
            self.after(0, lambda: messagebox.showinfo("Sucesso", f"Merge de {len(self.selected_files)} arquivos concluído!\nSalvo em: {output_file}"))
            self.after(0, lambda: self.lbl_status.configure(text="Concluído com sucesso"))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Erro Crítico", str(e)))
            self.after(0, lambda: self.lbl_status.configure(text="Falha na operação"))
        finally:
            self.after(0, lambda: self._lock_ui(False))

    def _lock_ui(self, lock: bool):
        state = "disabled" if lock else "normal"
        self.btn_select.configure(state=state)
        self.btn_folder.configure(state=state)
        self.entry_filename.configure(state=state)
        self.btn_run.configure(state=state)