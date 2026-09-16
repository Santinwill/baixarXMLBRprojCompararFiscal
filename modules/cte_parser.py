from pathlib import Path
import xml.etree.ElementTree as ET


def remover_namespace(tag):
    """Remove o namespace de uma tag XML."""
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def obter_texto(elemento):
    """Retorna o texto limpo de um elemento ou string vazia."""
    if elemento is None:
        return ""
    return (elemento.text or "").strip()


def buscar_filho(elemento, nome_tag):
    """Localiza um filho direto ignorando o namespace."""
    if elemento is None:
        return None

    for filho in elemento:
        if remover_namespace(filho.tag) == nome_tag:
            return filho

    return None


def buscar_filhos(elemento, nome_tag):
    """Localiza todos os filhos diretos com a tag informada."""
    if elemento is None:
        return []

    return [
        filho
        for filho in elemento
        if remover_namespace(filho.tag) == nome_tag
    ]


def buscar_descendente(elemento, nome_tag):
    """Localiza o primeiro descendente ignorando o namespace."""
    if elemento is None:
        return None

    for descendente in elemento.iter():
        if remover_namespace(descendente.tag) == nome_tag:
            return descendente

    return None


def buscar_descendentes(elemento, nome_tag):
    """Localiza todos os descendentes com a tag informada."""
    if elemento is None:
        return []

    return [
        descendente
        for descendente in elemento.iter()
        if remover_namespace(descendente.tag) == nome_tag
    ]


def buscar_texto_filho(elemento, nome_tag):
    """Retorna o texto de um filho direto."""
    return obter_texto(buscar_filho(elemento, nome_tag))


def buscar_texto_descendente(elemento, nome_tag):
    """Retorna o texto do primeiro descendente encontrado."""
    return obter_texto(buscar_descendente(elemento, nome_tag))


def identificar_tipo_documento(root):
    """Identifica CT-e, NF-e ou documento desconhecido."""
    nome_root = remover_namespace(root.tag).lower()

    if nome_root in ("cteproc", "cte"):
        return "CTe"

    if nome_root in ("nfeproc", "nfe"):
        return "NFe"

    return "DESCONHECIDO"


def obter_chave_cte(root):
    """Obtém a chave pela propriedade Id de infCte."""
    inf_cte = buscar_descendente(root, "infCte")

    if inf_cte is None:
        return ""

    identificador = inf_cte.attrib.get("Id", "").strip()

    if identificador.startswith("CTe"):
        return identificador[3:]

    return identificador


def obter_identificacao_pessoa(elemento):
    """Obtém CNPJ ou CPF de uma pessoa do CT-e."""
    cnpj = buscar_texto_filho(elemento, "CNPJ")
    if cnpj:
        return cnpj

    return buscar_texto_filho(elemento, "CPF")


def obter_dados_pessoa(elemento, tag_endereco, prefixo):
    """Extrai identificação e endereço de uma pessoa do CT-e."""
    endereco = buscar_filho(elemento, tag_endereco)

    return {
        f"cnpj_cpf_{prefixo}": obter_identificacao_pessoa(elemento),
        f"razao_{prefixo}": buscar_texto_filho(elemento, "xNome"),
        f"fantasia_{prefixo}": buscar_texto_filho(elemento, "xFant"),
        f"ie_{prefixo}": buscar_texto_filho(elemento, "IE"),
        f"cidade_{prefixo}": buscar_texto_filho(endereco, "xMun"),
        f"uf_{prefixo}": buscar_texto_filho(endereco, "UF"),
        f"codigo_municipio_{prefixo}": buscar_texto_filho(endereco, "cMun"),
    }


def obter_tomador(inf_cte, ide):
    """
    Obtém o código do tomador e, quando existir toma4, os dados cadastrais informados diretamente no XML.
    """
    toma3 = buscar_filho(ide, "toma3")
    toma4 = buscar_filho(ide, "toma4")

    codigo = buscar_texto_filho(toma3, "toma")
    if not codigo:
        codigo = buscar_texto_filho(toma4, "toma")

    dados = {
        "codigo_tomador": codigo,
        "cnpj_cpf_tomador": "",
        "razao_tomador": "",
        "ie_tomador": "",
        "cidade_tomador": "",
        "uf_tomador": "",
    }

    if toma4 is not None:
        endereco = buscar_filho(toma4, "enderToma")
        dados.update(
            {
                "cnpj_cpf_tomador": obter_identificacao_pessoa(toma4),
                "razao_tomador": buscar_texto_filho(toma4, "xNome"),
                "ie_tomador": buscar_texto_filho(toma4, "IE"),
                "cidade_tomador": buscar_texto_filho(endereco, "xMun"),
                "uf_tomador": buscar_texto_filho(endereco, "UF"),
            }
        )

    return dados


def encontrar_grupo_icms(imposto):
    """Localiza o grupo tributário efetivo dentro de imp/ICMS."""
    icms = buscar_filho(imposto, "ICMS")

    if icms is None:
        return None

    for filho in icms:
        nome_tag = remover_namespace(filho.tag)
        if nome_tag.startswith("ICMS"):
            return filho

    return None


def primeiro_texto(elemento, nomes_tags):
    """Retorna o primeiro campo preenchido entre várias tags possíveis."""
    for nome_tag in nomes_tags:
        valor = buscar_texto_descendente(elemento, nome_tag)
        if valor:
            return valor

    return ""


def obter_dados_impostos(inf_cte):
    """Extrai ICMS, DIFAL e IBS/CBS do CT-e."""
    imposto = buscar_filho(inf_cte, "imp")
    grupo_icms = encontrar_grupo_icms(imposto)
    icms_uf_fim = buscar_filho(imposto, "ICMSUFFim")
    ibscbs = buscar_filho(imposto, "IBSCBS")

    return {
        "cst_icms": buscar_texto_descendente(grupo_icms, "CST"),
        "base_icms": primeiro_texto(
            grupo_icms,
            ("vBC", "vBCOutraUF"),
        ),
        "aliquota_icms": primeiro_texto(
            grupo_icms,
            ("pICMS", "pICMSOutraUF"),
        ),
        "valor_icms": primeiro_texto(
            grupo_icms,
            ("vICMS", "vICMSOutraUF"),
        ),
        "percentual_reducao_bc": buscar_texto_descendente(
            grupo_icms,
            "pRedBC",
        ),
        "valor_credito_outorgado": buscar_texto_descendente(
            grupo_icms,
            "vCred",
        ),
        "valor_total_tributos": buscar_texto_filho(
            imposto,
            "vTotTrib",
        ),
        "base_icms_uf_fim": buscar_texto_filho(
            icms_uf_fim,
            "vBCUFFim",
        ),
        "aliquota_fcp_uf_fim": buscar_texto_filho(
            icms_uf_fim,
            "pFCPUFFim",
        ),
        "aliquota_icms_uf_fim": buscar_texto_filho(
            icms_uf_fim,
            "pICMSUFFim",
        ),
        "aliquota_icms_interestadual": buscar_texto_filho(
            icms_uf_fim,
            "pICMSInter",
        ),
        "valor_fcp_uf_fim": buscar_texto_filho(
            icms_uf_fim,
            "vFCPUFFim",
        ),
        "valor_icms_uf_fim": buscar_texto_filho(
            icms_uf_fim,
            "vICMSUFFim",
        ),
        "valor_icms_uf_inicio": buscar_texto_filho(
            icms_uf_fim,
            "vICMSUFIni",
        ),
        "cst_ibscbs": buscar_texto_filho(ibscbs, "CST"),
        "classificacao_tributaria_ibscbs": buscar_texto_filho(
            ibscbs,
            "cClassTrib",
        ),
        "base_ibscbs": buscar_texto_descendente(ibscbs, "vBC"),
        "aliquota_ibs_uf": buscar_texto_descendente(ibscbs, "pIBSUF"),
        "valor_ibs_uf": buscar_texto_descendente(ibscbs, "vIBSUF"),
        "aliquota_ibs_municipio": buscar_texto_descendente(
            ibscbs,
            "pIBSMun",
        ),
        "valor_ibs_municipio": buscar_texto_descendente(
            ibscbs,
            "vIBSMun",
        ),
        "valor_ibs": buscar_texto_descendente(ibscbs, "vIBS"),
        "aliquota_cbs": buscar_texto_descendente(ibscbs, "pCBS"),
        "valor_cbs": buscar_texto_descendente(ibscbs, "vCBS"),
        "valor_total_dfe": buscar_texto_filho(imposto, "vTotDFe"),
    }


def obter_componentes_prestacao(inf_cte):
    """Extrai os componentes que formam o valor da prestação."""
    prestacao = buscar_filho(inf_cte, "vPrest")
    componentes = []

    for componente in buscar_filhos(prestacao, "Comp"):
        componentes.append(
            {
                "nome": buscar_texto_filho(componente, "xNome"),
                "valor": buscar_texto_filho(componente, "vComp"),
            }
        )

    return {
        "valor_total_prestacao": buscar_texto_filho(prestacao, "vTPrest"),
        "valor_a_receber": buscar_texto_filho(prestacao, "vRec"),
        "componentes_prestacao": componentes,
    }


def obter_informacoes_carga(inf_cte):
    """Extrai valores, produto predominante e medidas da carga."""
    info_carga = buscar_descendente(inf_cte, "infCarga")
    medidas = []

    for info_quantidade in buscar_filhos(info_carga, "infQ"):
        medidas.append(
            {
                "codigo_unidade": buscar_texto_filho(
                    info_quantidade,
                    "cUnid",
                ),
                "tipo_medida": buscar_texto_filho(
                    info_quantidade,
                    "tpMed",
                ),
                "quantidade": buscar_texto_filho(
                    info_quantidade,
                    "qCarga",
                ),
            }
        )

    return {
        "valor_carga": buscar_texto_filho(info_carga, "vCarga"),
        "produto_predominante": buscar_texto_filho(info_carga, "proPred"),
        "outra_caracteristica_carga": buscar_texto_filho(
            info_carga,
            "xOutCat",
        ),
        "valor_carga_averbada": buscar_texto_filho(
            info_carga,
            "vCargaAverb",
        ),
        "medidas_carga": medidas,
    }


def obter_chaves_nfe_referenciadas(inf_cte):
    """Retorna todas as chaves de NF-e vinculadas ao CT-e."""
    chaves = []

    for inf_nfe in buscar_descendentes(inf_cte, "infNFe"):
        chave = buscar_texto_filho(inf_nfe, "chave")
        if chave and chave not in chaves:
            chaves.append(chave)

    return chaves


def obter_observacoes(inf_cte):
    """Extrai xObs e observações de contribuinte e fisco."""
    complemento = buscar_filho(inf_cte, "compl")
    observacoes_contribuinte = []
    observacoes_fisco = []

    for observacao in buscar_filhos(complemento, "ObsCont"):
        observacoes_contribuinte.append(
            {
                "campo": observacao.attrib.get("xCampo", "").strip(),
                "texto": buscar_texto_filho(observacao, "xTexto"),
            }
        )

    for observacao in buscar_filhos(complemento, "ObsFisco"):
        observacoes_fisco.append(
            {
                "campo": observacao.attrib.get("xCampo", "").strip(),
                "texto": buscar_texto_filho(observacao, "xTexto"),
            }
        )

    return {
        "observacoes": buscar_texto_filho(complemento, "xObs"),
        "observacoes_contribuinte": observacoes_contribuinte,
        "observacoes_fisco": observacoes_fisco,
    }


def obter_dados_protocolo(root):
    """Extrai autorização e protocolo do CT-e processado."""
    protocolo = buscar_descendente(root, "infProt")

    return {
        "data_recebimento": buscar_texto_filho(protocolo, "dhRecbto"),
        "numero_protocolo": buscar_texto_filho(protocolo, "nProt"),
        "status": buscar_texto_filho(protocolo, "cStat"),
        "motivo_status": buscar_texto_filho(protocolo, "xMotivo"),
    }


def processar_cte(caminho_xml):
    """Processa um CT-e e retorna um dicionário fiscal estruturado."""
    caminho_xml = Path(caminho_xml)
    tree = ET.parse(caminho_xml)
    root = tree.getroot()

    if identificar_tipo_documento(root) != "CTe":
        raise ValueError(f"O arquivo {caminho_xml.name} não é um CT-e.")

    inf_cte = buscar_descendente(root, "infCte")
    ide = buscar_filho(inf_cte, "ide")
    emitente = buscar_filho(inf_cte, "emit")
    remetente = buscar_filho(inf_cte, "rem")
    expedidor = buscar_filho(inf_cte, "exped")
    recebedor = buscar_filho(inf_cte, "receb")
    destinatario = buscar_filho(inf_cte, "dest")

    documento = {
        "arquivo": caminho_xml.name,
        "tipo_documento": "CTe",
        "chave": obter_chave_cte(root),
        "versao": inf_cte.attrib.get("versao", "") if inf_cte is not None else "",
        "modelo": buscar_texto_filho(ide, "mod"),
        "numero_cte": buscar_texto_filho(ide, "nCT"),
        "serie": buscar_texto_filho(ide, "serie"),
        "data_emissao": buscar_texto_filho(ide, "dhEmi"),
        "cfop": buscar_texto_filho(ide, "CFOP"),
        "natureza_operacao": buscar_texto_filho(ide, "natOp"),
        "tipo_cte": buscar_texto_filho(ide, "tpCTe"),
        "tipo_servico": buscar_texto_filho(ide, "tpServ"),
        "modal": buscar_texto_filho(ide, "modal"),
        "codigo_municipio_envio": buscar_texto_filho(ide, "cMunEnv"),
        "municipio_envio": buscar_texto_filho(ide, "xMunEnv"),
        "uf_envio": buscar_texto_filho(ide, "UFEnv"),
        "codigo_municipio_inicio": buscar_texto_filho(ide, "cMunIni"),
        "municipio_inicio": buscar_texto_filho(ide, "xMunIni"),
        "uf_inicio": buscar_texto_filho(ide, "UFIni"),
        "codigo_municipio_fim": buscar_texto_filho(ide, "cMunFim"),
        "municipio_fim": buscar_texto_filho(ide, "xMunFim"),
        "uf_fim": buscar_texto_filho(ide, "UFFim"),
        "retira": buscar_texto_filho(ide, "retira"),
        "indicador_ie_tomador": buscar_texto_filho(ide, "indIEToma"),
        "rntrc": buscar_texto_descendente(inf_cte, "RNTRC"),
        "chaves_nfe_referenciadas": obter_chaves_nfe_referenciadas(inf_cte),
    }

    documento.update(obter_dados_pessoa(emitente, "enderEmit", "emitente"))
    documento.update(obter_dados_pessoa(remetente, "enderReme", "remetente"))
    documento.update(obter_dados_pessoa(expedidor, "enderExped", "expedidor"))
    documento.update(obter_dados_pessoa(recebedor, "enderReceb", "recebedor"))
    documento.update(obter_dados_pessoa(destinatario, "enderDest", "destinatario"))
    documento.update(obter_tomador(inf_cte, ide))
    documento.update(obter_componentes_prestacao(inf_cte))
    documento.update(obter_dados_impostos(inf_cte))
    documento.update(obter_informacoes_carga(inf_cte))
    documento.update(obter_observacoes(inf_cte))
    documento.update(obter_dados_protocolo(root))

    return documento


def processar_pasta_ctes(xml_dir):
    """Processa somente CT-es presentes na pasta informada."""
    resultados = []
    pasta = Path(xml_dir)

    if not pasta.exists():
        print(f"Pasta não encontrada: {pasta}")
        return resultados

    for arquivo_xml in sorted(pasta.glob("*.xml")):
        try:
            tree = ET.parse(arquivo_xml)
            root = tree.getroot()

            if identificar_tipo_documento(root) != "CTe":
                continue

            resultados.append(processar_cte(arquivo_xml))

        except ET.ParseError as erro:
            print(f"XML inválido: {arquivo_xml.name} | {erro}")

        except Exception as erro:
            print(f"Erro ao processar {arquivo_xml.name}: {erro}")

    return resultados
