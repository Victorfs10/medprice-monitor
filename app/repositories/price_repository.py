from datetime import timezone, timedelta
from app.db.connection import get_connection

BRT = timezone(timedelta(hours=-3))


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
                SELECT p.id, pr.nome, pr.ean, p.preco, p.farmacia, p.url, p.created_at
                FROM precos p
                JOIN produtos pr ON pr.id = p.produto_id
                ORDER BY p.created_at DESC
                LIMIT 100
            """)
            rows = cur.fetchall()
            result = []
            for row in rows:
                r = dict(row)
                if r.get("created_at"):
                    r["created_at"] = r["created_at"].replace(tzinfo=timezone.utc).astimezone(BRT).strftime("%d/%m/%Y")
                result.append(r)
            return result
    finally:
        conn.close()


def find_preco_by_id(id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.id, pr.nome, pr.ean, p.preco, p.farmacia, p.url, p.created_at
                FROM precos p
                JOIN produtos pr ON pr.id = p.produto_id
                WHERE p.id = %s
            """, (id,))
            row = cur.fetchone()
            if not row:
                return None
            r = dict(row)
            if r.get("created_at"):
                r["created_at"] = r["created_at"].replace(tzinfo=timezone.utc).astimezone(BRT).strftime("%d/%m/%Y")
            return r
    finally:
        conn.close()
