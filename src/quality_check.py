import pandas as pd
from extract import extract
from transform import transform


def check_missing(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Hitung persentase data hilang per kolom, urutkan dari yang paling parah."""
    total = len(df)
    missing = df.isnull().sum()
    pct = (missing / total * 100).round(2)
    report = pd.DataFrame({"missing_count": missing, "missing_pct": pct})
    report = report[report["missing_count"] > 0].sort_values("missing_pct", ascending=False)
    print(f"\n[QUALITY] Missing value report - {name}")
    print(report)
    return report


def check_percentage_range(df: pd.DataFrame, kolom_persen: list):
    """Cek kolom yang seharusnya persentase (0-100), tapi nilainya di luar itu."""
    print(f"\n[QUALITY] Cek kolom persentase di luar rentang 0-100")
    for kolom in kolom_persen:
        di_luar_rentang = df[(df[kolom] < 0) | (df[kolom] > 100)]
        if len(di_luar_rentang) > 0:
            print(f"  {kolom}: {len(di_luar_rentang)} baris di luar rentang")
        else:
            print(f"  {kolom}: aman")


if __name__ == "__main__":
    raw_df = extract()
    dim_country, fact_energy_yearly = transform(raw_df)

    check_missing(dim_country, "dim_country")
    check_missing(fact_energy_yearly, "fact_energy_yearly")

    kolom_persen = [
        "access_to_electricity_pct",
        "access_to_clean_fuels_cooking",
        "renewable_energy_share_pct",
        "low_carbon_electricity_pct",
        "renewables_pct_equivalent_primary_energy",
    ]
    check_percentage_range(fact_energy_yearly, kolom_persen)

    baris_aneh = fact_energy_yearly[
        (fact_energy_yearly["low_carbon_electricity_pct"] < 0)
        | (fact_energy_yearly["low_carbon_electricity_pct"] > 100)
    ]
    print("\n[QUALITY] Detail baris dengan nilai low_carbon_electricity_pct aneh:")
    print(baris_aneh[["entity", "year", "low_carbon_electricity_pct"]])