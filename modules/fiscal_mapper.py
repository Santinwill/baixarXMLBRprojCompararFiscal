def obter_cd_uni_neg(cnpj):
    if not cnpj:
        return ""
    numeros = "".join(
        c for c in str(cnpj)
        if c.isdigit()
    )
    if len(numeros) != 14:
        return ""
    estabelecimento = numeros[8:12]
    return estabelecimento[-3:]

def mapear_nfe(documento):
    registros = []
    for item in documento["itens"]:
        registro = {
            "cd_uni_neg":
                obter_cd_uni_neg(documento["cnpj_destinatario"]),

            "arquivo": documento["arquivo"],
            "tipo_documento": documento["tipo_documento"],

            "chave": documento["chave"],
            "modelo": documento["modelo"],

            "numero_nf": documento["numero_nf"],
            "serie": documento["serie"],

            "data_emissao": documento["data_emissao"],
            "data_saida_entrada": documento["data_saida_entrada"],

            "natureza_operacao": documento["natureza_operacao"],
            "tipo_operacao": documento["tipo_operacao"],
            "finalidade_emissao": documento["finalidade_emissao"],

            "cnpj_emitente": documento["cnpj_emitente"],
            "razao_emitente": documento["razao_emitente"],

            "cidade_emitente": documento["cidade_emitente"],
            "uf_emitente": documento["uf_emitente"],

            "ie_emitente":
                documento["inscricao_estadual_emitente"],

            "cnpj_destinatario":
                documento["cnpj_destinatario"],

            "razao_destinatario":
                documento["razao_destinatario"],

            "cidade_destinatario":
                documento["cidade_destinatario"],

            "uf_destinatario":
                documento["uf_destinatario"],

            "ie_destinatario":
                documento["inscricao_estadual_destinatario"],

            "base_icms_total":
                documento["base_icms_total"],

            "valor_icms_total":
                documento["valor_icms_total"],

            "valor_produtos_total":
                documento["valor_produtos_total"],

            "valor_frete_total":
                documento["valor_frete_total"],

            "valor_seguro_total":
                documento["valor_seguro_total"],

            "valor_desconto_total":
                documento["valor_desconto_total"],

            "valor_ipi_total":
                documento["valor_ipi_total"],

            "valor_pis_total":
                documento["valor_pis_total"],

            "valor_cofins_total":
                documento["valor_cofins_total"],

            "valor_total_nf":
                documento["valor_total_nf"],

            "valor_pis_retido":
                documento["valor_pis_retido"],

            "valor_cofins_retido":
                documento["valor_cofins_retido"],

            "valor_csll_retido":
                documento["valor_csll_retido"],

            "valor_irrf_retido":
                documento["valor_irrf_retido"],

            "valor_inss_retido":
                documento["valor_inss_retido"],

            "informacoes_complementares":
                documento["informacoes_complementares"],

            "informacoes_fisco":
                documento["informacoes_fisco"],

            "n_item": item["n_item"],

            "codigo_produto":
                item["codigo_produto"],

            "descricao_produto":
                item["descricao_produto"],

            "ean":
                item["ean"],

            "ean_tributavel":
                item["ean_tributavel"],

            "ncm":
                item["ncm"],

            "cest":
                item["cest"],

            "cfop":
                item["cfop"],

            "unidade":
                item["unidade"],

            "quantidade":
                item["quantidade"],

            "valor_unitario":
                item["valor_unitario"],

            "valor_item":
                item["valor_total"],

            "valor_frete_item":
                item["valor_frete"],

            "valor_seguro_item":
                item["valor_seguro"],

            "valor_desconto_item":
                item["valor_desconto"],

            "valor_outros_item":
                item["valor_outros"],

            "origem_icms":
                item["origem_icms"],

            "cst_icms":
                item["cst_icms"],

            "modalidade_bc_icms":
                item["modalidade_bc_icms"],

            "base_icms":
                item["base_icms"],

            "aliquota_icms":
                item["aliquota_icms"],

            "valor_icms":
                item["valor_icms"],

            "base_icms_st":
                item["base_icms_st"],

            "valor_icms_st":
                item["valor_icms_st"],

            "valor_icms_desonerado":
                item["valor_icms_desonerado"],

            "valor_fcp":
                item["valor_fcp"],

            "valor_fcp_st":
                item["valor_fcp_st"],

            "valor_icms_uf_destino":
                item["valor_icms_uf_destino"],

            "valor_icms_uf_remetente":
                item["valor_icms_uf_remetente"],

            "cst_pis":
                item["cst_pis"],

            "base_pis":
                item["base_pis"],

            "aliquota_pis":
                item["aliquota_pis"],

            "valor_pis":
                item["valor_pis"],

            "cst_cofins":
                item["cst_cofins"],

            "base_cofins":
                item["base_cofins"],

            "aliquota_cofins":
                item["aliquota_cofins"],

            "valor_cofins":
                item["valor_cofins"],

            "cst_ipi":
                item["cst_ipi"],

            "base_ipi":
                item["base_ipi"],

            "aliquota_ipi":
                item["aliquota_ipi"],

            "valor_ipi":
                item["valor_ipi"],

            "base_issqn":
                item["base_issqn"],

            "aliquota_issqn":
                item["aliquota_issqn"],

            "valor_issqn":
                item["valor_issqn"],

            "indicador_total":
                item["indicador_total"],

            "pedido_compra":
                item["pedido_compra"],

            "item_pedido_compra":
                item["item_pedido_compra"],

            "informacao_adicional_item":
                item["informacao_adicional_item"],
        }
        registros.append(registro)
    return registros

def mapear_nfse(documento):
    registro = {
        "cd_uni_neg":
            obter_cd_uni_neg(documento["cnpj_destinatario"]),

        "arquivo":
            documento["arquivo"],

        "tipo_documento":
            "NFSe",

        "chave":
            documento["chave"],

        "modelo":
            documento["modelo"],

        "numero_nf":
            documento["numero_nf"],

        "serie":
            documento["serie"],

        "data_emissao":
            documento["data_emissao"],

        "data_saida_entrada":
            documento["data_competencia"],

        "natureza_operacao":
            "SERVICO",

        "tipo_operacao":
            "SERVICO",

        "finalidade_emissao":
            "",

        "cnpj_emitente":
            documento["cnpj_emitente"],

        "razao_emitente":
            documento["razao_emitente"],

        "cidade_emitente":
            documento["cidade_emitente"],

        "uf_emitente":
            documento["uf_emitente"],

        "ie_emitente":
            "",

        "cnpj_destinatario":
            documento["cnpj_destinatario"],

        "razao_destinatario":
            documento["razao_destinatario"],

        "cidade_destinatario":
            documento["cidade_destinatario"],

        "uf_destinatario":
            documento.get(
                "uf_destinatario",
                ""
            ),

        "ie_destinatario":
            "",

        "base_icms_total":
            "",

        "valor_icms_total":
            "",

        "valor_produtos_total":
            documento["valor_servico"],

        "valor_frete_total":
            "",

        "valor_seguro_total":
            "",

        "valor_desconto_total":
            "",

        "valor_ipi_total":
            "",

        "valor_pis_total":
            "",

        "valor_cofins_total":
            "",

        "valor_total_nf":
            documento["valor_total_nf"],

        "valor_pis_retido":
            "",

        "valor_cofins_retido":
            "",

        "valor_csll_retido":
            "",

        "valor_irrf_retido":
            "",

        "valor_inss_retido":
            "",

        "informacoes_complementares":
            documento["observacoes"],

        "informacoes_fisco":
            "",

        "n_item":
            "1",

        "codigo_produto":
            documento["codigo_servico"],

        "descricao_produto":
            documento["descricao_servico"],

        "ean":
            "",

        "ean_tributavel":
            "",

        "ncm":
            "",

        "cest":
            "",

        "cfop":
            "",

        "unidade":
            "UN",

        "quantidade":
            "1",

        "valor_unitario":
            documento["valor_servico"],

        "valor_item":
            documento["valor_servico"],

        "valor_frete_item":
            "",

        "valor_seguro_item":
            "",

        "valor_desconto_item":
            "",

        "valor_outros_item":
            "",

        "origem_icms":
            "",

        "cst_icms":
            "",

        "modalidade_bc_icms":
            "",

        "base_icms":
            "",

        "aliquota_icms":
            "",

        "valor_icms":
            "",

        "base_icms_st":
            "",

        "valor_icms_st":
            "",

        "valor_icms_desonerado":
            "",

        "valor_fcp":
            "",

        "valor_fcp_st":
            "",

        "valor_icms_uf_destino":
            "",

        "valor_icms_uf_remetente":
            "",

        "cst_pis":
            "",

        "base_pis":
            "",

        "aliquota_pis":
            "",

        "valor_pis":
            "",

        "cst_cofins":
            "",

        "base_cofins":
            "",

        "aliquota_cofins":
            "",

        "valor_cofins":
            "",

        "cst_ipi":
            "",

        "base_ipi":
            "",

        "aliquota_ipi":
            "",

        "valor_ipi":
            "",

        "base_issqn":
            documento["valor_servico"],

        "aliquota_issqn":
            "",

        "valor_issqn":
            "",

        "indicador_total":
            "1",

        "pedido_compra":
            "",

        "item_pedido_compra":
            "",

        "informacao_adicional_item":
            documento["descricao_servico"],
    }
    return [registro]

def mapear_documentos(documentos):
    registros = []
    for documento in documentos:
        tipo = documento.get("tipo_documento","")
        if tipo == "NFe":
            registros.extend(mapear_nfe(documento))
        elif tipo == "CTe":
            registros.extend(mapear_cte(documento))
        elif tipo == "NFSe":
            registros.extend(mapear_nfse(documento))
    return registros


def mapear_cte(documento):
    registro = {
        "cd_uni_neg":
            obter_cd_uni_neg(documento["cnpj_cpf_destinatario"]),

        "arquivo": documento["arquivo"],
        "tipo_documento": "CTe",

        "chave": documento["chave"],
        "modelo": documento["modelo"],

        "numero_nf": documento["numero_cte"],
        "serie": documento["serie"],

        "data_emissao": documento["data_emissao"],
        "data_saida_entrada": "",

        "natureza_operacao":
            documento["natureza_operacao"],

        "tipo_operacao":
            documento["tipo_servico"],

        "finalidade_emissao":
            documento["tipo_cte"],

        "cnpj_emitente":
            documento["cnpj_cpf_emitente"],

        "razao_emitente":
            documento["razao_emitente"],

        "cidade_emitente":
            documento["cidade_emitente"],

        "uf_emitente":
            documento["uf_emitente"],

        "ie_emitente":
            documento["ie_emitente"],

        "cnpj_destinatario":
            documento["cnpj_cpf_destinatario"],

        "razao_destinatario":
            documento["razao_destinatario"],

        "cidade_destinatario":
            documento["cidade_destinatario"],

        "uf_destinatario":
            documento["uf_destinatario"],

        "ie_destinatario":
            documento["ie_destinatario"],

        "base_icms_total":
            documento["base_icms"],

        "valor_icms_total":
            documento["valor_icms"],

        "valor_produtos_total":
            documento["valor_total_prestacao"],

        "valor_frete_total":
            documento["valor_total_prestacao"],

        "valor_seguro_total": "",
        "valor_desconto_total": "",

        "valor_ipi_total": "",
        "valor_pis_total": "",
        "valor_cofins_total": "",

        "valor_total_nf":
            documento["valor_total_prestacao"],

        "valor_pis_retido": "",
        "valor_cofins_retido": "",
        "valor_csll_retido": "",
        "valor_irrf_retido": "",
        "valor_inss_retido": "",

        "informacoes_complementares":
            documento["observacoes"],

        "informacoes_fisco": "",

        "n_item": "1",

        "codigo_produto": "",

        "descricao_produto":
            "SERVICO DE TRANSPORTE",

        "ean": "",
        "ean_tributavel": "",

        "ncm": "",
        "cest": "",

        "cfop":
            documento["cfop"],

        "unidade": "UN",

        "quantidade": "1",

        "valor_unitario":
            documento["valor_total_prestacao"],

        "valor_item":
            documento["valor_total_prestacao"],

        "valor_frete_item": "",
        "valor_seguro_item": "",
        "valor_desconto_item": "",
        "valor_outros_item": "",

        "origem_icms": "",

        "cst_icms":
            documento["cst_icms"],

        "modalidade_bc_icms": "",

        "base_icms":
            documento["base_icms"],

        "aliquota_icms":
            documento["aliquota_icms"],

        "valor_icms":
            documento["valor_icms"],

        "base_icms_st": "",
        "valor_icms_st": "",
        "valor_icms_desonerado": "",

        "valor_fcp":
            documento["valor_fcp_uf_fim"],

        "valor_fcp_st": "",

        "valor_icms_uf_destino":
            documento["valor_icms_uf_fim"],

        "valor_icms_uf_remetente":
            documento["valor_icms_uf_inicio"],

        "cst_pis":
            documento["cst_ibscbs"],

        "base_pis":
            documento["base_ibscbs"],

        "aliquota_pis":
            documento["aliquota_cbs"],

        "valor_pis":
            documento["valor_cbs"],

        "cst_cofins":
            documento["cst_ibscbs"],

        "base_cofins":
            documento["base_ibscbs"],

        "aliquota_cofins":
            documento["aliquota_cbs"],

        "valor_cofins":
            documento["valor_cbs"],

        "cst_ipi": "",
        "base_ipi": "",
        "aliquota_ipi": "",
        "valor_ipi": "",

        "base_issqn": "",
        "aliquota_issqn": "",
        "valor_issqn": "",

        "indicador_total": "1",

        "pedido_compra": "",
        "item_pedido_compra": "",

        "informacao_adicional_item":
            documento["produto_predominante"],
    }
    return [registro]      