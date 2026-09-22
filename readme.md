# BRprojXML

Automação desenvolvida para consulta, download, processamento e consolidação de documentos fiscais eletrônicos obtidos através do portal BR Proj.

---

# Objetivo

Automatizar o processo diário de obtenção de documentos fiscais eletrônicos, eliminando atividades manuais e consolidando as informações em uma única base Excel para conferência fiscal.

---

# Escopo Atual (v0.4.0)

O projeto atualmente realiza:

- Login automático no portal BR Proj
- Consulta automática de documentos recebidos
- Download automático dos arquivos disponibilizados
- Navegação entre múltiplas páginas de resultado
- Extração automática de arquivos ZIP
- Organização dos XMLs baixados
- Leitura de documentos NF-e
- Leitura de documentos CT-e
- Leitura de documentos NFS-e
- Conversão para estrutura fiscal padronizada
- Consolidação dos documentos em Base_Fiscal.xlsx
- Controle de duplicidade através da coluna CHAVE_ITEM
- Atualização incremental da base histórica
- Geração de logs de execução

---

# Estrutura Atual do Projeto

```text
BRprojXML/
│
├── downloads/
├── logs/
├── outputs/
├── xmls/
│
├── modules/
│   ├── config.py
│   ├── login.py
│   ├── filtros.py
│   ├── pagination.py
│   ├── download.py
│   ├── extractor.py
│   ├── nfe_parser.py
│   ├── cte_parser.py
│   ├── nfse_parser.py
│   ├── fiscal_mapper.py
│   ├── excel_exporter.py
│   ├── logger.py
│   └── statistics.py
│
├── main.py
├── requirements.txt
├── executar_brprojTI.bat
├── executar_brprojW.bat
├── .env
├── .env.example
└── README.md
```

---

# Fluxo Atual da Automação

## Etapa 1 - Consulta no Portal

1. Acessa o portal BR Proj
2. Realiza autenticação
3. Configura filtros automaticamente
4. Consulta documentos recebidos
5. Navega por todas as páginas disponíveis

## Etapa 2 - Download

6. Seleciona todos os documentos da página
7. Realiza exportação automática
8. Salva os arquivos na pasta downloads

## Etapa 3 - Processamento

9. Extrai arquivos ZIP
10. Move XMLs para a pasta xmls
11. Ignora XMLs já existentes

## Etapa 4 - Leitura Fiscal

12. Processa NF-es
13. Processa CT-es
14. Processa NFS-es

## Etapa 5 - Consolidação

15. Mapeia os documentos para o layout fiscal
16. Gera registros fiscais padronizados
17. Valida duplicidades por CHAVE_ITEM
18. Atualiza a Base_Fiscal.xlsx

---

# Documentos Suportados

## NF-e

Suporte para:

- Dados do emitente
- Dados do destinatário
- Produtos
- CFOP
- NCM
- ICMS
- PIS
- COFINS
- IPI
- Retenções
- Informações complementares

## CT-e

Suporte para:

- Emitente
- Remetente
- Destinatário
- Tomador
- Prestação de transporte
- Valores fiscais
- ICMS
- Chaves NF-e relacionadas

## NFS-e

Suporte para:

- Prestador
- Tomador
- Dados do serviço
- Valor do serviço
- Informações complementares

---

# Base Fiscal

O sistema gera o arquivo:

```text
outputs\Base_Fiscal.xlsx
```

A base é cumulativa.

Registros já existentes não são importados novamente.

---

# Controle de Duplicidade

O controle é realizado através da coluna:

```text
CHAVE_ITEM
```

Formato:

```text
CHAVE_ACESSO_ITEM
```

Exemplo:

```text
43240612345678000123550010000012341000012345_1
```

Cada item fiscal pode existir apenas uma vez dentro da Base_Fiscal.xlsx.

---

# Campos Adicionados ao Projeto

Campos implementados especificamente para controle interno:

- TIPO_DOCUMENTO
- CHAVE
- CHAVE_ITEM
- CD_UNI_NEG

O campo CD_UNI_NEG é obtido a partir dos 3 últimos dígitos do estabelecimento presente no CNPJ do destinatário/tomador.

---

# Logs

Os logs são gravados em:

```text
logs/brproj.log
```

São registrados:

- Início da execução
- Login realizado
- Downloads efetuados
- XMLs processados
- Erros encontrados
- Resumo da execução

---

# Configuração

Criar arquivo:

```env
.env
```

Conteúdo:

```env
BRPROJ_USUARIO=
BRPROJ_SENHA=
BRPROJ_URL=
```

---

# Instalação

## Criar ambiente virtual

Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Instalar Playwright

```bash
playwright install
```

---

# Execução

```bash
python main.py
```

---

# Execução Agendada

O projeto pode ser executado através:

- Arquivo BAT
- Agendador de Tarefas do Windows

Atualmente é utilizado para execução automática diária.

---

# Tecnologias Utilizadas

- Python
- Playwright
- OpenPyXL
- python-dotenv

---

# Histórico de Versão

## v0.4.0

Implementado até esta versão:

- Download automatizado BR Proj
- Extração de ZIPs
- Parser NF-e
- Parser CT-e
- Parser NFS-e
- Fiscal Mapper unificado
- Exportação Base_Fiscal.xlsx
- Campo TIPO_DOCUMENTO
- Campo CHAVE
- Campo CHAVE_ITEM
- Campo CD_UNI_NEG
- Deduplicação por CHAVE_ITEM
- Atualização incremental da base

---

# Autor

Willian Pedro Santin

Projeto interno para automação da obtenção e consolidação de documentos fiscais eletrônicos através do portal BR Proj.
``