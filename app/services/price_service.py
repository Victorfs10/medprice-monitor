from app.repositories.price_repository import find_all_precos, find_preco_by_id


def get_precos() -> list[dict]:
    return find_all_precos()


def get_preco_by_id(id: int):
    return find_preco_by_id(id)
