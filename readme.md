# BRprojXML

Automação em Python para consulta e download de arquivos XML e ZIP de documentos fiscais através do portal BR Proj.

## Objetivo

Este projeto automatiza o processo diário de consulta e download de documentos fiscais no BR Proj, eliminando atividades manuais e permitindo futura execução agendada.

### Funcionalidades

- Login automático no portal BR Proj
- Configuração automática dos filtros de pesquisa
- Navegação por múltiplas páginas de resultados
- Download automático dos arquivos XML/ZIP
- Organização dos arquivos baixados
- Estrutura preparada para execução agendada
- Estrutura modular para manutenção futura

---

# Estrutura do Projeto

```text
BRprojXML/
│
├── database/
│
├── downloads/
│
├── logs/
│
├── xmls/
│
├── modulos/
│   ├── login.py
│   ├── filtros.py
│   ├── pagination.py
│   ├── download.py
│   ├── extractor.py
│   └── utils.py
│
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

# Fluxo da Automação

1. Abre o portal BR Proj
2. Realiza autenticação
3. Seleciona:
   - Recebidas
   - NFe
   - CTe
   - Listar Transferências
4. Limpa o campo CNPJ
5. Define a data desejada
6. Executa a consulta
7. Identifica a quantidade total de páginas
8. Percorre todas as páginas disponíveis
9. Realiza o download dos arquivos
10. Armazena os arquivos localmente

---

# Tecnologias Utilizadas

- Python 3.12+
- Playwright
- Microsoft Edge / Google Chrome
- dotenv

---

# Instalação

## 1. Clonar o Repositório

```bash
git clone https://github.com/SEU-USUARIO/BRprojXML.git
```

```bash
cd BRprojXML
```

---

## 2. Criar Ambiente Virtual

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## 4. Instalar Navegadores do Playwright

```bash
playwright install
```

---

# Configuração

Criar um arquivo `.env` na raiz do projeto:

```env
BRPROJ_USUARIO=seu_usuario
BRPROJ_SENHA=sua_senha
```

Nunca enviar o arquivo `.env` para o Git.

---

# Arquivo .env.example

Criar um arquivo chamado:

```text
.env.example
```

Conteúdo:

```env
BRPROJ_USUARIO=
BRPROJ_SENHA=
```

Esse arquivo serve apenas como modelo para novos ambientes.

---

# Execução

Executar a automação:

```bash
python main.py
```

---

# Estrutura dos Diretórios

## downloads

Armazena os arquivos baixados pelo navegador durante a execução.

```text
downloads/
```

---

## xmls

Armazena os XMLs processados ou extraídos.

```text
xmls/
```

---

## logs

Armazena os logs de execução.

```text
logs/
```

---

## database

Diretório reservado para futuras funcionalidades:

- Controle de processamentos
- Histórico de documentos
- Banco SQLite
- Controle de duplicidades

```text
database/
```

---

# Logs

Os logs devem registrar:

- Início da execução
- Login realizado
- Quantidade de páginas encontradas
- Downloads realizados
- Arquivos processados
- Erros encontrados
- Encerramento do processo

---

# Melhorias Futuras

- Execução automática via Agendador de Tarefas do Windows
- Execução em servidor Linux
- Execução em Docker
- Validação de documentos duplicados
- Integração com ERP CIGAM
- Integração com SharePoint
- Envio de alertas por e-mail
- Dashboard de monitoramento
- Download automático de PDFs de NFS-e

---

# Git Ignore Recomendado

```gitignore
# Python
__pycache__/
*.pyc
*.pyo

# Ambientes virtuais
venv/
.venv/

# Arquivos sensíveis
.env

# Logs
logs/
*.log

# Downloads
downloads/

# XMLs
xmls/

# Banco de dados
database/
*.db
*.sqlite3

# VS Code
.vscode/

# Sistema operacional
.DS_Store
Thumbs.db
```

---

# Autor

Willian Pedro Santin

Projeto desenvolvido para automatizar a consulta e o download de documentos fiscais através do portal BR Proj, com foco em integração futura aos processos internos da Life Agro.