from app.db.connection import get_connection


def find_produto_by_ean(ean: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM produtos WHERE ean = %s", (ean,))
            return cur.fetchone()
    finally:
        conn.close()


def insert_produto(nome: str, ean: str) -> int:
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO produtos (nome, ean) VALUES (%s, %s) RETURNING id",
                    (nome, ean),
                )
                return cur.fetchone()["id"]
    finally:
        conn.close()


def insert_preco(produto_id: int, preco: float, farmacia: str, url: str):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO precos (produto_id, preco, farmacia, url) VALUES (%s, %s, %s, %s)",
                    (produto_id, preco, farmacia, url),
                )
    finally:
        conn.close()


def find_all_precos() -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, pr.nome, pr.ean, p.preco, p.farmacia, p.url, p.collected_at
                FROM precos p
                JOIN produtos pr ON pr.id = p.produto_id
                ORDER BY p.collected_at DESC
                LIMIT 100
            """)
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def find_preco_by_id(id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, pr.nome, pr.ean, p.preco, p.farmacia, p.url, p.collected_at
                FROM precos p
                JOIN produtos pr ON pr.id = p.produto_id
                WHERE p.id = %s
            """, (id,))
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()
