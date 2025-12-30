# 🛡️ Excel Merger Pro

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-Fast_Data-CD792C?logo=rust)
![UI](https://img.shields.io/badge/CustomTkinter-Dark_Mode-1a1a1a)
![Status](https://img.shields.io/badge/Build-Passing-2CC985)

> **Ferramenta Enterprise para Unificação de Dados em Alta Performance.**

O **Excel Merger Pro** é uma aplicação desktop desenvolvida para consolidar múltiplos arquivos Excel (`.xlsx`) em um único dataset unificado. Diferente de scripts simples, ele utiliza **Polars** (Rust-based engine) para garantir performance superior e baixo consumo de memória, envolvido em uma interface moderna e responsiva.

---

## 🚀 Principais Funcionalidades

### ⚙️ Core & Performance
- **Engine Polars:** Processamento multithreaded otimizado em Rust.
- **Merge Ilimitado:** Aceita qualquer quantidade de arquivos de entrada (1 ou 100+).
- **Schema Enforcement:** Converte automaticamente todas as colunas para `Text/String` durante a leitura, prevenindo erros de tipagem (`Int64` vs `Utf8`) e garantindo a integridade da fusão.
- **Sanitização de Input:** Proteção automática contra caracteres inválidos em nomes de arquivos (Regex).

### 🎨 UI & UX (User Experience)
- **Interface Dark Minimalista:** Design system baseado na cor `#1a1a1a` para conforto visual.
- **Feedback em Tempo Real:** Barra de progresso assíncrona (não trava a janela) e status detalhado.
- **Validação de Estado:** Botões de ação só são liberados quando os requisitos (arquivos + pasta de saída) são atendidos.

### 🔍 Observabilidade
- **Logging Detalhado:** Registra o nome das colunas de cada arquivo processado em `logs/app_execution.log` para facilitar auditoria e debug de divergências.

---

## 📂 Arquitetura do Projeto

O projeto segue princípios **SOLID** e **Clean Architecture**, separando responsabilidades:

```text
ExcelMergerPro/
│
├── assets/                 # Recursos estáticos (Ícones)
├── dist/                   # Executável compilado (após build)
├── logs/                   # Arquivos de log de execução
│
├── src/
│   ├── services/           # Regra de Negócio (Polars, I/O)
│   │   └── excel_handler.py
│   │
│   ├── ui/                 # Interface Gráfica (View/Controller)
│   │   └── main_window.py
│   │
│   └── utils/              # Helpers e Configurações
│       ├── helpers.py
│       └── logger_config.py
│
├── build.py                # Script de automação do PyInstaller
├── main.py                 # Ponto de entrada (Entry Point)
└── requirements.txt        # Dependências

## ⚙️ Instalação e Uso

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/excel-merger-pro.git](https://github.com/seu-usuario/excel-merger-pro.git)
   cd excel-merger-pro
   ```

2. **Instale as dependências:**
   Recomenda-se usar um ambiente virtual (`venv`).
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```bash
   python src/main.py
   ```

4. **Compilação para uso (opcional):**
   ```bash
   python build.py
   ```

## 📝 Como Usar

1. Clique em **"Selecionar Arquivos"** e escolha exatamente 3 arquivos `.xlsx`.
2. O sistema validará se os arquivos são compatíveis.
3. Clique em **"INICIAR MERGE"**.
4. Escolha onde salvar o arquivo final.
5. Acompanhe o progresso na barra inferior.

## 🤝 Contribuição

O projeto segue princípios **SOLID**.
- Ao criar novas features de processamento, adicione ao `services/`.
- Ao alterar a interface, modifique apenas `ui/`.