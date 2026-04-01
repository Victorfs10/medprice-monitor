class BaseScraper:
    def scrape(self, query: str) -> list[dict]:
        """
        Busca produtos por nome e retorna lista de dicts com:
        - nome: str
        - ean: str
        - preco: float
        - preco_lista: float
        - farmacia: str
        - url: str
        - disponivel: bool
        """
        raise NotImplementedError
