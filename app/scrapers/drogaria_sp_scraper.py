import requests
from app.scrapers.base_scraper import BaseScraper

BASE_URL = "https://www.drogariasaopaulo.com.br"
SEARCH_URL = f"{BASE_URL}/api/io/_v/api/intelligent-search/product_search/trade-policy/1"
FARMACIA = "drogaria_sao_paulo"


class DrogariaSaoPauloScraper(BaseScraper):
    def scrape(self, query: str) -> list[dict]:
        results = []
        page = 1
        count = 48

        while True:
            response = requests.get(
                SEARCH_URL,
                params={"query": query, "count": count, "page": page},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            products = data.get("products", [])
            if not products:
                break

            for product in products:
                item = product.get("items", [{}])[0]
                seller = item.get("sellers", [{}])[0]
                offer = seller.get("commertialOffer", {})

                results.append({
                    "nome": product.get("productName"),
                    "ean": item.get("ean"),
                    "preco": offer.get("Price"),
                    "preco_lista": offer.get("ListPrice"),
                    "farmacia": FARMACIA,
                    "url": BASE_URL + product.get("link", ""),
                    "disponivel": offer.get("AvailableQuantity", 0) > 0,
                })

            records_filtered = data.get("recordsFiltered", 0)
            if page * count >= records_filtered:
                break
            page += 1

        return results
