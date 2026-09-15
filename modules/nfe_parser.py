from pathlib import Path
import xml.etree.ElementTree as ET


def remover_namespace(tag):
    """
    Remove o namespace de uma tag XML.

    Exemplo:
        {http://www.portalfiscal.inf.br/nfe}cUF

    Retorno:
        cUF
    """

    if "}" in tag:
        return tag.split("}", 1)[1]

    return tag


def obter_texto(elemento):
    """
    Retorna o texto de um elemento XML.

    Caso o elemento não exista ou esteja vazio,
    retorna uma string vazia.
    """

    if elemento is None:
        return ""

    return (elemento.text or "").strip()


def buscar_filho(elemento, nome_tag):
    """
    Localiza um filho direto pelo nome da tag,
    ignorando o namespace XML.
    """

    if elemento is None:
        return None

    for filho in elemento:

        if remover_namespace(filho.tag) == nome_tag:
            return filho

    return None


def buscar_texto_filho(elemento, nome_tag):
    """
    Retorna o texto de um filho direto.
    """

    filho = buscar_filho(
        elemento,
        nome_tag,
    )

    return obter_texto(filho)


def buscar_descendente(elemento, nome_tag):
    """
    Localiza o primeiro descendente pelo nome da tag,
    ignorando o namespace.
    """

    if elemento is None:
        return None

    for descendente in elemento.iter():

        if remover_namespace(descendente.tag) == nome_tag:
            return descendente

    return None


def buscar_texto_descendente(elemento, nome_tag):
    """
    Retorna o texto do primeiro descendente
    encontrado com a tag informada.
    """

    descendente = buscar_descendente(
        elemento,
        nome_tag,
    )

    return obter_texto(descendente)


def identificar_tipo_documento(root):
    """
    Identifica o tipo do documento fiscal.
    """

    nome_root = remover_namespace(root.tag).lower()

    if nome_root in (
        "nfeproc",
        "nfe",
    ):
        return "NFe"

    if nome_root in (
        "cteproc",
        "cte",
    ):
        return "CTe"

    return "DESCONHECIDO"


def obter_chave(root):
    """
    Obtém a chave de acesso pela propriedade Id
    da tag infNFe.
    """

    for elemento in root.iter():

        nome_tag = remover_namespace(
            elemento.tag
        )

        if nome_tag != "infNFe":
            continue

        identificador = elemento.attrib.get(
            "Id",
            "",
        ).strip()

        if identificador.startswith("NFe"):
            return identificador[3:]

        return identificador

    return ""


def obter_identificacao_pessoa(elemento):
    """
    Obtém CNPJ ou CPF de um emitente ou destinatário.
    """

    if elemento is None:
        return ""

    cnpj = buscar_texto_filho(
        elemento,
        "CNPJ",
    )

    if cnpj:
        return cnpj

    return buscar_texto_filho(
        elemento,
        "CPF",
    )


def obter_endereco_emitente(emitente):
    """
    Obtém cidade e UF do endereço do emitente.

    Para o layout de entradas, o fornecedor da NF-e
    recebida corresponde normalmente ao emitente.
    """

    endereco = buscar_filho(
        emitente,
        "enderEmit",
    )

    return {
        "cidade_emitente": buscar_texto_filho(
            endereco,
            "xMun",
        ),
        "uf_emitente": buscar_texto_filho(
            endereco,
            "UF",
        ),
    }


def obter_endereco_destinatario(destinatario):
    """
    Obtém cidade e UF do destinatário.
    """

    endereco = buscar_filho(
        destinatario,
        "enderDest",
    )

    return {
        "cidade_destinatario": buscar_texto_filho(
            endereco,
            "xMun",
        ),
        "uf_destinatario": buscar_texto_filho(
            endereco,
            "UF",
        ),
    }


def encontrar_grupo_imposto(imposto, prefixo):
    """
    Localiza um grupo tributário pelo prefixo.

    Exemplos de grupos localizados:

        ICMS00
        ICMS20
        ICMS40
        ICMS60
        ICMSSN102
        ICMSSN500

        PISAliq
        PISQtde
        PISNT
        PISOutr

        COFINSAliq
        COFINSQtde
        COFINSNT
        COFINSOutr

        IPITrib
        IPINT
    """

    if imposto is None:
        return None

    for elemento in imposto.iter():

        nome_tag = remover_namespace(
            elemento.tag
        )

        if nome_tag.startswith(prefixo):
            return elemento

    return None


def obter_cst_icms(grupo_icms):
    """
    Obtém o CST ou CSOSN do ICMS.

    Quando o XML usa CSOSN, o valor é mantido
    integralmente no campo cst_icms.
    """

    if grupo_icms is None:
        return ""

    cst = buscar_texto_descendente(
        grupo_icms,
        "CST",
    )

    if cst:
        return cst

    return buscar_texto_descendente(
        grupo_icms,
        "CSOSN",
    )


def obter_dados_icms(imposto):
    """
    Extrai os principais dados de ICMS do item.
    """

    grupo_icms = encontrar_grupo_imposto(
        imposto,
        "ICMS",
    )

    if grupo_icms is None:
        return {
            "origem_icms": "",
            "cst_icms": "",
            "modalidade_bc_icms": "",
            "base_icms": "",
            "aliquota_icms": "",
            "valor_icms": "",
            "base_icms_st": "",
            "valor_icms_st": "",
            "valor_icms_desonerado": "",
            "valor_fcp": "",
            "valor_fcp_st": "",
            "valor_icms_uf_destino": "",
            "valor_icms_uf_remetente": "",
            "valor_fcp_uf_destino": "",
        }

    return {
        "origem_icms": buscar_texto_descendente(
            grupo_icms,
            "orig",
        ),
        "cst_icms": obter_cst_icms(
            grupo_icms
        ),
        "modalidade_bc_icms": buscar_texto_descendente(
            grupo_icms,
            "modBC",
        ),
        "base_icms": buscar_texto_descendente(
            grupo_icms,
            "vBC",
        ),
        "aliquota_icms": buscar_texto_descendente(
            grupo_icms,
            "pICMS",
        ),
        "valor_icms": buscar_texto_descendente(
            grupo_icms,
            "vICMS",
        ),
        "base_icms_st": buscar_texto_descendente(
            grupo_icms,
            "vBCST",
        ),
        "valor_icms_st": buscar_texto_descendente(
            grupo_icms,
            "vICMSST",
        ),
        "valor_icms_desonerado": buscar_texto_descendente(
            grupo_icms,
            "vICMSDeson",
        ),
        "valor_fcp": buscar_texto_descendente(
            grupo_icms,
            "vFCP",
        ),
        "valor_fcp_st": buscar_texto_descendente(
            grupo_icms,
            "vFCPST",
        ),
        "valor_icms_uf_destino": buscar_texto_descendente(
            imposto,
            "vICMSUFDest",
        ),
        "valor_icms_uf_remetente": buscar_texto_descendente(
            imposto,
            "vICMSUFRemet",
        ),
        "valor_fcp_uf_destino": buscar_texto_descendente(
            imposto,
            "vFCPUFDest",
        ),
    }


def obter_dados_pis(imposto):
    """
    Extrai os dados de PIS do item.
    """

    grupo_pis = encontrar_grupo_imposto(
        imposto,
        "PIS",
    )

    if grupo_pis is None:
        return {
            "cst_pis": "",
            "base_pis": "",
            "aliquota_pis": "",
            "quantidade_bc_pis": "",
            "aliquota_pis_reais": "",
            "valor_pis": "",
        }

    return {
        "cst_pis": buscar_texto_descendente(
            grupo_pis,
            "CST",
        ),
        "base_pis": buscar_texto_descendente(
            grupo_pis,
            "vBC",
        ),
        "aliquota_pis": buscar_texto_descendente(
            grupo_pis,
            "pPIS",
        ),
        "quantidade_bc_pis": buscar_texto_descendente(
            grupo_pis,
            "qBCProd",
        ),
        "aliquota_pis_reais": buscar_texto_descendente(
            grupo_pis,
            "vAliqProd",
        ),
        "valor_pis": buscar_texto_descendente(
            grupo_pis,
            "vPIS",
        ),
    }


def obter_dados_cofins(imposto):
    """
    Extrai os dados de COFINS do item.
    """

    grupo_cofins = encontrar_grupo_imposto(
        imposto,
        "COFINS",
    )

    if grupo_cofins is None:
        return {
            "cst_cofins": "",
            "base_cofins": "",
            "aliquota_cofins": "",
            "quantidade_bc_cofins": "",
            "aliquota_cofins_reais": "",
            "valor_cofins": "",
        }

    return {
        "cst_cofins": buscar_texto_descendente(
            grupo_cofins,
            "CST",
        ),
        "base_cofins": buscar_texto_descendente(
            grupo_cofins,
            "vBC",
        ),
        "aliquota_cofins": buscar_texto_descendente(
            grupo_cofins,
            "pCOFINS",
        ),
        "quantidade_bc_cofins": buscar_texto_descendente(
            grupo_cofins,
            "qBCProd",
        ),
        "aliquota_cofins_reais": buscar_texto_descendente(
            grupo_cofins,
            "vAliqProd",
        ),
        "valor_cofins": buscar_texto_descendente(
            grupo_cofins,
            "vCOFINS",
        ),
    }


def obter_dados_ipi(imposto):
    """
    Extrai os dados de IPI do item.
    """

    grupo_ipi = encontrar_grupo_imposto(
        imposto,
        "IPI",
    )

    if grupo_ipi is None:
        return {
            "cst_ipi": "",
            "codigo_enquadramento_ipi": "",
            "base_ipi": "",
            "aliquota_ipi": "",
            "valor_ipi": "",
        }

    grupo_tributacao_ipi = None

    for elemento in grupo_ipi.iter():

        nome_tag = remover_namespace(
            elemento.tag
        )

        if nome_tag in (
            "IPITrib",
            "IPINT",
        ):
            grupo_tributacao_ipi = elemento
            break

    if grupo_tributacao_ipi is None:
        grupo_tributacao_ipi = grupo_ipi

    return {
        "cst_ipi": buscar_texto_descendente(
            grupo_tributacao_ipi,
            "CST",
        ),
        "codigo_enquadramento_ipi": buscar_texto_descendente(
            grupo_ipi,
            "cEnq",
        ),
        "base_ipi": buscar_texto_descendente(
            grupo_tributacao_ipi,
            "vBC",
        ),
        "aliquota_ipi": buscar_texto_descendente(
            grupo_tributacao_ipi,
            "pIPI",
        ),
        "valor_ipi": buscar_texto_descendente(
            grupo_tributacao_ipi,
            "vIPI",
        ),
    }


def obter_dados_issqn(imposto):
    """
    Extrai os dados de ISSQN quando o item representa serviço.
    """

    grupo_issqn = buscar_descendente(
        imposto,
        "ISSQN",
    )

    if grupo_issqn is None:
        return {
            "base_issqn": "",
            "aliquota_issqn": "",
            "valor_issqn": "",
            "codigo_municipio_issqn": "",
            "item_lista_servico": "",
        }

    return {
        "base_issqn": buscar_texto_filho(
            grupo_issqn,
            "vBC",
        ),
        "aliquota_issqn": buscar_texto_filho(
            grupo_issqn,
            "vAliq",
        ),
        "valor_issqn": buscar_texto_filho(
            grupo_issqn,
            "vISSQN",
        ),
        "codigo_municipio_issqn": buscar_texto_filho(
            grupo_issqn,
            "cMunFG",
        ),
        "item_lista_servico": buscar_texto_filho(
            grupo_issqn,
            "cListServ",
        ),
    }


def obter_totais_documento(root):
    """
    Extrai os totais da NF-e e retenções.
    """

    total = buscar_descendente(
        root,
        "total",
    )

    icms_total = buscar_descendente(
        total,
        "ICMSTot",
    )

    issqn_total = buscar_descendente(
        total,
        "ISSQNtot",
    )

    ret_tributos = buscar_descendente(
        total,
        "retTrib",
    )

    return {
        "base_icms_total": buscar_texto_filho(
            icms_total,
            "vBC",
        ),
        "valor_icms_total": buscar_texto_filho(
            icms_total,
            "vICMS",
        ),
        "valor_icms_desonerado_total": buscar_texto_filho(
            icms_total,
            "vICMSDeson",
        ),
        "base_icms_st_total": buscar_texto_filho(
            icms_total,
            "vBCST",
        ),
        "valor_icms_st_total": buscar_texto_filho(
            icms_total,
            "vST",
        ),
        "valor_produtos_total": buscar_texto_filho(
            icms_total,
            "vProd",
        ),
        "valor_frete_total": buscar_texto_filho(
            icms_total,
            "vFrete",
        ),
        "valor_seguro_total": buscar_texto_filho(
            icms_total,
            "vSeg",
        ),
        "valor_desconto_total": buscar_texto_filho(
            icms_total,
            "vDesc",
        ),
        "valor_ii_total": buscar_texto_filho(
            icms_total,
            "vII",
        ),
        "valor_ipi_total": buscar_texto_filho(
            icms_total,
            "vIPI",
        ),
        "valor_pis_total": buscar_texto_filho(
            icms_total,
            "vPIS",
        ),
        "valor_cofins_total": buscar_texto_filho(
            icms_total,
            "vCOFINS",
        ),
        "valor_outros_total": buscar_texto_filho(
            icms_total,
            "vOutro",
        ),
        "valor_total_nf": buscar_texto_filho(
            icms_total,
            "vNF",
        ),
        "base_issqn_total": buscar_texto_filho(
            issqn_total,
            "vBC",
        ),
        "valor_issqn_total": buscar_texto_filho(
            issqn_total,
            "vISS",
        ),
        "valor_pis_servicos": buscar_texto_filho(
            issqn_total,
            "vPIS",
        ),
        "valor_cofins_servicos": buscar_texto_filho(
            issqn_total,
            "vCOFINS",
        ),
        "valor_pis_retido": buscar_texto_filho(
            ret_tributos,
            "vRetPIS",
        ),
        "valor_cofins_retido": buscar_texto_filho(
            ret_tributos,
            "vRetCOFINS",
        ),
        "valor_csll_retido": buscar_texto_filho(
            ret_tributos,
            "vRetCSLL",
        ),
        "base_irrf": buscar_texto_filho(
            ret_tributos,
            "vBCIRRF",
        ),
        "valor_irrf_retido": buscar_texto_filho(
            ret_tributos,
            "vIRRF",
        ),
        "base_inss": buscar_texto_filho(
            ret_tributos,
            "vBCRetPrev",
        ),
        "valor_inss_retido": buscar_texto_filho(
            ret_tributos,
            "vRetPrev",
        ),
    }


def processar_item(det):
    """
    Processa um item da NF-e.

    Cada tag det será transformada em um dicionário
    que posteriormente corresponderá a uma linha
    da planilha de entradas.
    """

    produto = buscar_filho(
        det,
        "prod",
    )

    imposto = buscar_filho(
        det,
        "imposto",
    )

    dados_icms = obter_dados_icms(
        imposto
    )

    dados_pis = obter_dados_pis(
        imposto
    )

    dados_cofins = obter_dados_cofins(
        imposto
    )

    dados_ipi = obter_dados_ipi(
        imposto
    )

    dados_issqn = obter_dados_issqn(
        imposto
    )

    item = {
        "n_item": det.attrib.get(
            "nItem",
            "",
        ),
        "codigo_produto": buscar_texto_filho(
            produto,
            "cProd",
        ),
        "ean": buscar_texto_filho(
            produto,
            "cEAN",
        ),
        "descricao_produto": buscar_texto_filho(
            produto,
            "xProd",
        ),
        "ncm": buscar_texto_filho(
            produto,
            "NCM",
        ),
        "cest": buscar_texto_filho(
            produto,
            "CEST",
        ),
        "cfop": buscar_texto_filho(
            produto,
            "CFOP",
        ),
        "unidade": buscar_texto_filho(
            produto,
            "uCom",
        ),
        "quantidade": buscar_texto_filho(
            produto,
            "qCom",
        ),
        "valor_unitario": buscar_texto_filho(
            produto,
            "vUnCom",
        ),
        "valor_total": buscar_texto_filho(
            produto,
            "vProd",
        ),
        "ean_tributavel": buscar_texto_filho(
            produto,
            "cEANTrib",
        ),
        "unidade_tributavel": buscar_texto_filho(
            produto,
            "uTrib",
        ),
        "quantidade_tributavel": buscar_texto_filho(
            produto,
            "qTrib",
        ),
        "valor_unitario_tributavel": buscar_texto_filho(
            produto,
            "vUnTrib",
        ),
        "valor_frete": buscar_texto_filho(
            produto,
            "vFrete",
        ),
        "valor_seguro": buscar_texto_filho(
            produto,
            "vSeg",
        ),
        "valor_desconto": buscar_texto_filho(
            produto,
            "vDesc",
        ),
        "valor_outros": buscar_texto_filho(
            produto,
            "vOutro",
        ),
        "indicador_total": buscar_texto_filho(
            produto,
            "indTot",
        ),
        "pedido_compra": buscar_texto_filho(
            produto,
            "xPed",
        ),
        "item_pedido_compra": buscar_texto_filho(
            produto,
            "nItemPed",
        ),
        "informacao_adicional_item": buscar_texto_filho(
            det,
            "infAdProd",
        ),
    }

    item.update(dados_icms)
    item.update(dados_pis)
    item.update(dados_cofins)
    item.update(dados_ipi)
    item.update(dados_issqn)

    return item


def processar_nfe(caminho_xml):
    """
    Processa uma NF-e e retorna:

        dados do documento;
        emitente;
        destinatário;
        endereço;
        totais;
        retenções;
        itens;
        impostos de cada item.
    """

    caminho_xml = Path(caminho_xml)

    tree = ET.parse(caminho_xml)
    root = tree.getroot()

    tipo_documento = identificar_tipo_documento(
        root
    )

    if tipo_documento != "NFe":
        raise ValueError(
            f"O arquivo {caminho_xml.name} "
            f"não é uma NF-e."
        )

    inf_nfe = buscar_descendente(
        root,
        "infNFe",
    )

    ide = buscar_filho(
        inf_nfe,
        "ide",
    )

    emitente = buscar_filho(
        inf_nfe,
        "emit",
    )

    destinatario = buscar_filho(
        inf_nfe,
        "dest",
    )

    endereco_emitente = obter_endereco_emitente(
        emitente
    )

    endereco_destinatario = obter_endereco_destinatario(
        destinatario
    )

    totais = obter_totais_documento(
        inf_nfe
    )

    documento = {
        "arquivo": caminho_xml.name,
        "tipo_documento": tipo_documento,
        "chave": obter_chave(root),
        "versao": (
            inf_nfe.attrib.get("versao", "")
            if inf_nfe is not None
            else ""
        ),
        "modelo": buscar_texto_filho(
            ide,
            "mod",
        ),
        "numero_nf": buscar_texto_filho(
            ide,
            "nNF",
        ),
        "serie": buscar_texto_filho(
            ide,
            "serie",
        ),
        "data_emissao": (
            buscar_texto_filho(ide, "dhEmi")
            or buscar_texto_filho(ide, "dEmi")
        ),
        "data_saida_entrada": (
            buscar_texto_filho(ide, "dhSaiEnt")
            or buscar_texto_filho(ide, "dSaiEnt")
        ),
        "tipo_operacao": buscar_texto_filho(
            ide,
            "tpNF",
        ),
        "finalidade_emissao": buscar_texto_filho(
            ide,
            "finNFe",
        ),
        "natureza_operacao": buscar_texto_filho(
            ide,
            "natOp",
        ),
        "codigo_municipio_fato_gerador": buscar_texto_filho(
            ide,
            "cMunFG",
        ),
        "cnpj_emitente": obter_identificacao_pessoa(
            emitente
        ),
        "razao_emitente": buscar_texto_filho(
            emitente,
            "xNome",
        ),
        "fantasia_emitente": buscar_texto_filho(
            emitente,
            "xFant",
        ),
        "inscricao_estadual_emitente": buscar_texto_filho(
            emitente,
            "IE",
        ),
        "cnpj_destinatario": obter_identificacao_pessoa(
            destinatario
        ),
        "razao_destinatario": buscar_texto_filho(
            destinatario,
            "xNome",
        ),
        "inscricao_estadual_destinatario": buscar_texto_filho(
            destinatario,
            "IE",
        ),
        "informacoes_complementares": buscar_texto_descendente(
            inf_nfe,
            "infCpl",
        ),
        "informacoes_fisco": buscar_texto_descendente(
            inf_nfe,
            "infAdFisco",
        ),
        "itens": [],
    }

    documento.update(
        endereco_emitente
    )

    documento.update(
        endereco_destinatario
    )

    documento.update(
        totais
    )

    for elemento in inf_nfe:

        if remover_namespace(elemento.tag) != "det":
            continue

        item = processar_item(
            elemento
        )

        documento["itens"].append(
            item
        )

    return documento


def processar_pasta_xmls(xml_dir):
    """
    Processa somente as NF-es da pasta informada.

    CT-es e documentos desconhecidos são ignorados,
    pois terão parser próprio em outra fase.
    """

    resultados = []

    pasta = Path(xml_dir)

    if not pasta.exists():
        print(
            f"Pasta não encontrada: {pasta}"
        )

        return resultados

    for arquivo_xml in sorted(
        pasta.glob("*.xml")
    ):
        try:
            tree = ET.parse(
                arquivo_xml
            )

            root = tree.getroot()

            tipo_documento = identificar_tipo_documento(
                root
            )

            if tipo_documento != "NFe":
                continue

            dados = processar_nfe(
                arquivo_xml
            )

            resultados.append(
                dados
            )

        except ET.ParseError as erro:
            print(
                f"XML inválido: "
                f"{arquivo_xml.name} | "
                f"{erro}"
            )

        except Exception as erro:
            print(
                f"Erro ao processar "
                f"{arquivo_xml.name}: "
                f"{erro}"
            )

    return resultados


if __name__ == "__main__":
    documentos = processar_pasta_xmls(
        "xmls"
    )

    print(
        f"NF-es processadas: "
        f"{len(documentos)}"
    )

    total_itens = sum(
        len(documento["itens"])
        for documento in documentos
    )

    print(
        f"Itens encontrados: "
        f"{total_itens}"
    )

    if documentos:
        primeira_nfe = documentos[0]

        print(
            "\nDados da primeira NF-e:"
        )

        print(
            {
                "arquivo": primeira_nfe["arquivo"],
                "chave": primeira_nfe["chave"],
                "modelo": primeira_nfe["modelo"],
                "numero_nf": primeira_nfe["numero_nf"],
                "serie": primeira_nfe["serie"],
                "data_emissao": primeira_nfe["data_emissao"],
                "cnpj_emitente": primeira_nfe[
                    "cnpj_emitente"
                ],
                "razao_emitente": primeira_nfe[
                    "razao_emitente"
                ],
                "uf_emitente": primeira_nfe[
                    "uf_emitente"
                ],
                "cidade_emitente": primeira_nfe[
                    "cidade_emitente"
                ],
                "valor_total_nf": primeira_nfe[
                    "valor_total_nf"
                ],
                "valor_pis_retido": primeira_nfe[
                    "valor_pis_retido"
                ],
                "valor_cofins_retido": primeira_nfe[
                    "valor_cofins_retido"
                ],
                "valor_csll_retido": primeira_nfe[
                    "valor_csll_retido"
                ],
                "valor_irrf_retido": primeira_nfe[
                    "valor_irrf_retido"
                ],
                "valor_inss_retido": primeira_nfe[
                    "valor_inss_retido"
                ],
            }
        )

        if primeira_nfe["itens"]:
            print(
                "\nPrimeiro item:"
            )

            print(
                primeira_nfe["itens"][0]
            )