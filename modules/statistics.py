class Statistics:

    def __init__(self):
        self.paginas_processadas = 0
        self.downloads_realizados = 0
        self.xmls_novos = 0
        self.xmls_duplicados = 0
        self.erros = 0
        self.tempo_execucao = "00:00:00"

    def resumo(self):
        return f"""
=====================================
RESUMO DA EXECUÇÃO
=====================================
Páginas processadas: {self.paginas_processadas}
Downloads realizados: {self.downloads_realizados}
XMLs novos: {self.xmls_novos}
XMLs duplicados: {self.xmls_duplicados}
Erros encontrados: {self.erros}
Tempo execução: {self.tempo_execucao}
=====================================
"""