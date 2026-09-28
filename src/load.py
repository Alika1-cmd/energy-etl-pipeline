import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from extract import extract
from transform import transform

# tunjuk langsung ke file .env di root project (satu tingkat di atas folder src)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
SCHEMA_PATH = Path("sql/schema.sql")


def get_engine():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL tidak ditemukan. Cek file .env kamu.")
    # paksa pakai driver psycopg2, biar tidak bentrok sama psycopg (v3)
    url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    return create_engine(url)


def create_schema(engine):
    """Jalankan schema.sql untuk membuat tabel, kalau belum ada."""
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    with engine.connect() as conn:
        for statement in schema_sql.split(";"):
            statement = statement.strip()
            if statement:
                conn.execute(text(statement))
        conn.commit()
    print("[LOAD] Skema tabel siap.")


def load(dim_country, fact_energy_yearly, engine):
    dim_country.to_sql("dim_country", engine, if_exists="append", index=False)
    print(f"[LOAD] {len(dim_country)} baris masuk ke dim_country")

    fact_energy_yearly.to_sql("fact_energy_yearly", engine, if_exists="append", index=False)
    print(f"[LOAD] {len(fact_energy_yearly)} baris masuk ke fact_energy_yearly")


if __name__ == "__main__":
    raw_df = extract()
    dim_country, fact_energy_yearly = transform(raw_df)

    engine = get_engine()
    create_schema(engine)
    load(dim_country, fact_energy_yearly, engine)