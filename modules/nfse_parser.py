from pathlib import Path
import xml.etree.ElementTree as ET


def remover_namespace(tag):
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def obter_texto(elemento):
    if elemento is None:
        return ""

    return (elemento.text or "").strip()


def buscar_descendente(elemento, nome_tag):
    if elemento is None:
        return None

    for item in elemento.iter():
        if remover_namespace(item.tag) == nome_tag:
            return item

    return None


def buscar_texto(elemento, nome_tag):
    return obter_texto(
        buscar_descendente(
            elemento,
            nome_tag
        )
    )


def identificar_tipo_documento(root):
    nome_root = remover_namespace(
        root.tag
    ).lower()

    if nome_root == "nfse":
        return "NFSe"

    return "DESCONHECIDO"


def obter_chave_nfse(root):

    inf_nfse = buscar_descendente(
        root,
        "infNFSe"
    )

    if inf_nfse is None:
        return ""

    identificador = (
        inf_nfse.attrib.get(
            "Id",
            ""
        )
        .strip()
    )

    if identificador.startswith("NFS"):
        return identificador[3:]

    return identificador


def processar_nfse(caminho_xml):

    caminho_xml = Path(caminho_xml)

    tree = ET.parse(caminho_xml)

    root = tree.getroot()

    if identificar_tipo_documento(root) != "NFSe":
        raise ValueError(
            f"{caminho_xml.name} não é NFSe"
        )

    inf_nfse = buscar_descendente(
        root,
        "infNFSe"
    )

    emit = buscar_descendente(
        inf_nfse,
        "emit"
    )

    toma = buscar_descendente(
        inf_nfse,
        "toma"
    )

    dps = buscar_descendente(
        inf_nfse,
        "infDPS"
    )

    serv = buscar_descendente(
        inf_nfse,
        "serv"
    )

    valores = buscar_descendente(
        dps,
        "valores"
    )

    serv_prest = buscar_descendente(
        valores,
        "vServPrest"
    )

    documento = {

        "arquivo":
            caminho_xml.name,

        "tipo_documento":
            "NFSe",

        "chave":
            obter_chave_nfse(
                root
            ),

        "modelo":
            "NFSe",

        "numero_nf":
            buscar_texto(
                inf_nfse,
                "nNFSe"
            ),

        "serie":
            buscar_texto(
                dps,
                "serie"
            ),

        "data_emissao":
            buscar_texto(
                dps,
                "dhEmi"
            ),

        "data_competencia":
            buscar_texto(
                dps,
                "dCompet"
            ),

        "cnpj_emitente":
            buscar_texto(
                emit,
                "CNPJ"
            ),

        "razao_emitente":
            buscar_texto(
                emit,
                "xNome"
            ),

        "cidade_emitente":
            buscar_texto(
                emit,
                "cMun"
            ),

        "uf_emitente":
            buscar_texto(
                emit,
                "UF"
            ),

        "cnpj_destinatario":
            buscar_texto(
                toma,
                "CNPJ"
            ),

        "razao_destinatario":
            buscar_texto(
                toma,
                "xNome"
            ),

        "cidade_destinatario":
            buscar_texto(
                toma,
                "cMun"
            ),

        "uf_destinatario":
            "",

        "valor_servico":
            buscar_texto(
                serv_prest,
                "vServ"
            ),

        "valor_total_nf":
            buscar_texto(
                inf_nfse,
                "vLiq"
            ),

        "codigo_servico":
            buscar_texto(
                serv,
                "cTribNac"
            ),

        "descricao_servico":
            buscar_texto(
                serv,
                "xDescServ"
            ),

        "observacoes":
            buscar_texto(
                serv,
                "xInfComp"
            ),
    }

    return documento


def processar_pasta_nfses(xml_dir):

    resultados = []

    pasta = Path(xml_dir)

    if not pasta.exists():
        return resultados

    for arquivo_xml in sorted(
        pasta.glob("*.xml")
    ):

        try:

            tree = ET.parse(
                arquivo_xml
            )

            root = tree.getroot()

            if (
                identificar_tipo_documento(root)
                != "NFSe"
            ):
                continue

            resultados.append(
                processar_nfse(
                    arquivo_xml
                )
            )

        except ET.ParseError:
            continue

        except Exception as erro:
            print(
                f"Erro ao processar "
                f"{arquivo_xml.name}: "
                f"{erro}"
            )

    return resultados


if __name__ == "__main__":

    documentos = processar_pasta_nfses(
        "xmls"
    )

    print(
        f"NFSe encontradas: "
        f"{len(documentos)}"
    )

    if documentos:

        print(
            "\nPrimeira NFSe:"
        )

        print(
            documentos[0]
        )