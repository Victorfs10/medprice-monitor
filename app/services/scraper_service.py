from app.scrapers.drogaria_sp_scraper import DrogariaSaoPauloScraper
from app.repositories.price_repository import find_produto_by_ean, insert_produto, insert_preco

SCRAPERS = {
    "drogaria_sao_paulo": DrogariaSaoPauloScraper,
}


def run_scraper(farmacia: str, query: str) -> dict:
    scraper_class = SCRAPERS.get(farmacia)
    if not scraper_class:
        raise ValueError(f"Scraper não encontrado para: {farmacia}")

    scraper = scraper_class()
    products = scraper.scrape(query)

    saved = 0
    for product in products:
        ean = product.get("ean")
        if not ean:
            continue

        row = find_produto_by_ean(ean)
        produto_id = row["id"] if row else insert_produto(product["nome"], ean)

        insert_preco(
            produto_id=produto_id,
            preco=product["preco"],
            farmacia=product["farmacia"],
            url=product["url"],
        )
        saved += 1

    return {"scraped": len(products), "saved": saved}
