import pandas as pd
from extract import extract

RENAME_MAP = {
    "Entity": "entity",
    "Year": "year",
    "Access to electricity (% of population)": "access_to_electricity_pct",
    "Access to clean fuels for cooking": "access_to_clean_fuels_cooking",
    "Renewable-electricity-generating-capacity-per-capita": "renewable_electricity_capacity_per_capita",
    "Financial flows to developing countries (US $)": "financial_flows_developing_usd",
    "Renewable energy share in the total final energy consumption (%)": "renewable_energy_share_pct",
    "Electricity from fossil fuels (TWh)": "electricity_fossil_twh",
    "Electricity from nuclear (TWh)": "electricity_nuclear_twh",
    "Electricity from renewables (TWh)": "electricity_renewables_twh",
    "Low-carbon electricity (% electricity)": "low_carbon_electricity_pct",
    "Primary energy consumption per capita (kWh/person)": "primary_energy_consumption_per_capita_kwh",
    "Energy intensity level of primary energy (MJ/$2017 PPP GDP)": "energy_intensity_mj_per_gdp",
    "Value_co2_emissions_kt_by_country": "co2_emissions_kt",
    "Renewables (% equivalent primary energy)": "renewables_pct_equivalent_primary_energy",
    "gdp_growth": "gdp_growth",
    "gdp_per_capita": "gdp_per_capita",
    "Density\\n(P/Km2)": "density_per_km2",
    "Land Area(Km2)": "land_area_km2",
    "Latitude": "latitude",
    "Longitude": "longitude",
}


def clean_density(value):
    """Buang koma pemisah ribuan, lalu ubah ke angka. Kosong tetap kosong."""
    if pd.isna(value):
        return None
    return float(str(value).replace(",", ""))

def clip_percentage(value):
    """Batasi nilai persentase maksimal 100, minimal 0. Mengoreksi pembulatan floating-point."""
    if pd.isna(value):
        return value
    return max(0, min(100, value))

def transform(df: pd.DataFrame):
    df = df.rename(columns=RENAME_MAP)

    # perbaiki kolom density yang kebaca sebagai teks
    df["density_per_km2"] = df["density_per_km2"].apply(clean_density)

    df["low_carbon_electricity_pct"] = df["low_carbon_electricity_pct"].apply(clip_percentage)
    
    # pisahkan data yang tetap per negara -> dim_country
    dim_country = (
        df[["entity", "density_per_km2", "land_area_km2", "latitude", "longitude"]]
        .drop_duplicates(subset="entity")
        .reset_index(drop=True)
    )

    # sisanya (yang berubah tiap tahun) -> fact_energy_yearly
    kolom_geografis = ["density_per_km2", "land_area_km2", "latitude", "longitude"]
    fact_cols = [c for c in df.columns if c not in kolom_geografis]
    fact_energy_yearly = df[fact_cols].reset_index(drop=True)

    print(f"[TRANSFORM] dim_country: {len(dim_country)} baris")
    print(f"[TRANSFORM] fact_energy_yearly: {len(fact_energy_yearly)} baris")

    return dim_country, fact_energy_yearly


if __name__ == "__main__":
    raw_df = extract()
    dim_country, fact_energy_yearly = transform(raw_df)
    print("\ndim_country:")
    print(dim_country.head())
    print("\nfact_energy_yearly:")
    print(fact_energy_yearly.head())