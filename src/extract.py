import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/global-data-on-sustainable-energy (1).csv")

def extract(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Baca data mentah dari CSV, tanpa diubah sama sekali."""
    df = pd.read_csv(path)
    print(f"[EXTRACT] Berhasil baca {len(df)} baris dari {path.name}")
    return df

if __name__ == "__main__":
    df = extract()
    print(df.head())