from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


OUTPUT_DIR = Path("outputs")
SHEET_NAME = "Export"

# Ordem e nomes reproduzem o layout de Entradas 14-09.xlsx.
# TIPO_ESPECIE aparece duas vezes no arquivo de referencia e foi preservado.
COLUNAS = [
    ("CD_UNI_NEG", None),
    ("NF", "numero_nf"),
    ("MODELO_FORMULARIO", "modelo"),
    ("DATA_EMISSAO", "data_emissao"),
    ("DATA_ENTRADA", None),
    ("CNPJ_CPF", "cnpj_emitente"),
    ("RAZAO_SOCIAL", "razao_emitente"),
    ("UF", "uf_emitente"),
    ("CIDADE", "cidade_emitente"),
    ("CD_DESC_CFOP", "cfop"),
    ("CD_DESC_TIPO_OPERACAO", None),
    ("TIPO_ESPECIE", None),
    ("CD_CONTA_FIN", None),
    ("DESC_CONTA", None),
    ("CD_MATERIAL", "codigo_produto"),
    ("DESC_MATERIAL", "descricao_produto"),
    ("DESC_GRUPO", None),
    ("TIPO_ESPECIE", None),
    ("CD_CLASS_FISCAL", "ncm"),
    ("UN_MEDIDA", "unidade"),
    ("CTS_ICMS", "cst_icms"),
    ("CTS_PIS", "cst_pis"),
    ("CTS_COFINS", "cst_cofins"),
    ("CTS_IPI", "cst_ipi"),
    ("QTD_ENTRADA", "quantidade"),
    ("VLR_ENTRADA", "valor_item"),
    ("VLR_FRETE", "valor_frete_item"),
    ("VLR_DESCONTO", "valor_desconto_item"),
    ("COMPLEMENTO", "informacoes_complementares"),
    ("BASE_ICMS", "base_icms"),
    ("VLR_ICMS", "valor_icms"),
    ("ICMS_NAO_TRI", None),
    ("ICMS_OUTROS", None),
    ("ICMS_NAO_DEST", None),
    ("PIS_NAO_DEST", None),
    ("COFINS_NAO_DEST", None),
    ("BASE_PIS_COFINS", "base_pis_cofins"),
    ("VLR_PIS", "valor_pis"),
    ("VLR_COFINS", "valor_cofins"),
    ("VLR_IPI", "valor_ipi"),
    ("IPI_NAO_TRI", None),
    ("IPI_OUTROS", None),
    ("VLR_PIS_RET", "valor_pis_retido"),
    ("VLR_COFINS_RET", "valor_cofins_retido"),
    ("VLR_CSLL_RET", "valor_csll_retido"),
    ("VLR_IRRF_RET", "valor_irrf_retido"),
    ("VLR_ISS_RET", None),
    ("VLR_INSS_RET", "valor_inss_retido"),
    ("VLR_DIF_ALIQUOTA", "valor_icms_uf_destino"),
    ("MOVIMENTO", None),
]

CAMPOS_TEXTO = {
    "numero_nf",
    "modelo",
    "cnpj_emitente",
    "razao_emitente",
    "uf_emitente",
    "cidade_emitente",
    "cfop",
    "codigo_produto",
    "descricao_produto",
    "ncm",
    "unidade",
    "cst_icms",
    "cst_pis",
    "cst_cofins",
    "cst_ipi",
    "informacoes_complementares",
}

CAMPOS_NUMERICOS = {
    "quantidade",
    "valor_item",
    "valor_frete_item",
    "valor_desconto_item",
    "base_icms",
    "valor_icms",
    "base_pis_cofins",
    "valor_pis",
    "valor_cofins",
    "valor_ipi",
    "valor_pis_retido",
    "valor_cofins_retido",
    "valor_csll_retido",
    "valor_irrf_retido",
    "valor_inss_retido",
    "valor_icms_uf_destino",
}

CAMPOS_MONETARIOS = CAMPOS_NUMERICOS - {"quantidade"}

LARGURAS = {
    "CD_UNI_NEG": 13,
    "NF": 13,
    "MODELO_FORMULARIO": 18,
    "DATA_EMISSAO": 20,
    "DATA_ENTRADA": 16,
    "CNPJ_CPF": 20,
    "RAZAO_SOCIAL": 46,
    "UF": 8,
    "CIDADE": 25,
    "CD_DESC_CFOP": 18,
    "CD_DESC_TIPO_OPERACAO": 34,
    "TIPO_ESPECIE": 14,
    "CD_CONTA_FIN": 15,
    "DESC_CONTA": 30,
    "CD_MATERIAL": 18,
    "DESC_MATERIAL": 48,
    "DESC_GRUPO": 30,
    "CD_CLASS_FISCAL": 18,
    "UN_MEDIDA": 12,
    "COMPLEMENTO": 55,
    "MOVIMENTO": 16,
}


def para_decimal(valor):
    """Converte texto numerico do XML em Decimal, sem inventar zero."""
    if valor is None:
        return None

    texto = str(valor).strip()
    if not texto:
        return None

    try:
        return Decimal(texto)
    except InvalidOperation:
        return None


def para_data(valor):
    """Converte data ISO da NF-e em datetime sem fuso para o Excel."""
    if valor is None:
        return None

    texto = str(valor).strip()
    if not texto:
        return None

    try:
        data = datetime.fromisoformat(texto)
        return data.replace(tzinfo=None)
    except ValueError:
        return texto


def primeira_base_pis_cofins(registro):
    """Usa a base de PIS; se ausente, usa a base de COFINS."""
    base_pis = registro.get("base_pis", "")
    if str(base_pis or "").strip():
        return base_pis

    return registro.get("base_cofins", "")


def preparar_registro(registro):
    """Acrescenta somente campos derivados de origem conhecida."""
    preparado = dict(registro)
    preparado["base_pis_cofins"] = primeira_base_pis_cofins(registro)
    return preparado


def preparar_valor(registro, campo):
    """Prepara texto, numero ou data para escrita no Excel."""
    if campo is None:
        return ""

    valor = registro.get(campo, "")

    if campo == "data_emissao":
        return para_data(valor)

    if campo in CAMPOS_NUMERICOS:
        return para_decimal(valor)

    if valor is None:
        return ""

    return str(valor).strip()


def criar_cabecalho(planilha):
    """Cria o cabecalho na mesma ordem da planilha de referencia."""
    for coluna, (titulo, _) in enumerate(COLUNAS, start=1):
        celula = planilha.cell(row=1, column=coluna, value=titulo)
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill(fill_type="solid", fgColor="1F4E78")
        celula.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True,
        )

    planilha.row_dimensions[1].height = 32


def preencher_planilha(planilha, registros):
    """Grava uma linha para cada item fiscal mapeado."""
    for linha, registro_original in enumerate(registros, start=2):
        registro = preparar_registro(registro_original)

        for coluna, (_, campo) in enumerate(COLUNAS, start=1):
            valor = preparar_valor(registro, campo)
            celula = planilha.cell(row=linha, column=coluna, value=valor)
            celula.alignment = Alignment(vertical="top")

            if campo in CAMPOS_TEXTO:
                celula.number_format = "@"
            elif campo == "data_emissao" and isinstance(valor, datetime):
                celula.number_format = "dd/mm/yyyy"
            elif campo == "quantidade":
                celula.number_format = '#,##0.0000;[Red](#,##0.0000);-'
            elif campo in CAMPOS_MONETARIOS:
                celula.number_format = '#,##0.00;[Red](#,##0.00);-'


def ajustar_colunas(planilha):
    """Aplica larguras adequadas ao layout fiscal."""
    for coluna, (titulo, _) in enumerate(COLUNAS, start=1):
        letra = get_column_letter(coluna)
        planilha.column_dimensions[letra].width = LARGURAS.get(titulo, 16)


def gerar_excel(registros, output_dir=OUTPUT_DIR):
    """
    Gera um novo arquivo Excel por execucao.

    Os campos exclusivos do CIGAM permanecem vazios quando nao ha
    origem no XML ou no registro fiscal. O arquivo nao inventa codigos.
    """
    if not registros:
        raise ValueError("Nenhum registro fiscal informado para exportacao.")

    pasta_saida = Path(output_dir)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    agora = datetime.now()
    nome_arquivo = f"Entradas_XML_{agora.strftime('%Y%m%d_%H%M%S')}.xlsx"
    caminho_arquivo = pasta_saida / nome_arquivo

    workbook = Workbook()
    planilha = workbook.active
    planilha.title = SHEET_NAME
    planilha.freeze_panes = "A2"
    planilha.sheet_view.showGridLines = False

    criar_cabecalho(planilha)
    preencher_planilha(planilha, registros)
    ajustar_colunas(planilha)

    ultima_coluna = get_column_letter(len(COLUNAS))
    ultima_linha = len(registros) + 1
    planilha.auto_filter.ref = f"A1:{ultima_coluna}{ultima_linha}"

    workbook.save(caminho_arquivo)
    return caminho_arquivo


if __name__ == "__main__":
    from nfe_parser import processar_pasta_xmls
    from fiscal_mapper import mapear_documentos

    documentos = processar_pasta_xmls("xmls")
    registros = mapear_documentos(documentos)

    print(f"Documentos: {len(documentos)}")
    print(f"Registros: {len(registros)}")

    if registros:
        arquivo = gerar_excel(registros)
        print(f"Excel gerado: {arquivo}")
    else:
        print("Nenhum registro fiscal encontrado. Excel nao gerado.")
