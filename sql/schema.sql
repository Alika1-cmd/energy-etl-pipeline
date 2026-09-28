CREATE TABLE IF NOT EXISTS dim_country (
    entity TEXT PRIMARY KEY,
    density_per_km2 NUMERIC,
    land_area_km2 NUMERIC,
    latitude NUMERIC,
    longitude NUMERIC
);

CREATE TABLE IF NOT EXISTS fact_energy_yearly (
    id SERIAL PRIMARY KEY,
    entity TEXT NOT NULL REFERENCES dim_country(entity),
    year INTEGER NOT NULL,
    access_to_electricity_pct NUMERIC,
    access_to_clean_fuels_cooking NUMERIC,
    renewable_electricity_capacity_per_capita NUMERIC,
    financial_flows_developing_usd NUMERIC,
    renewable_energy_share_pct NUMERIC,
    electricity_fossil_twh NUMERIC,
    electricity_nuclear_twh NUMERIC,
    electricity_renewables_twh NUMERIC,
    low_carbon_electricity_pct NUMERIC,
    primary_energy_consumption_per_capita_kwh NUMERIC,
    energy_intensity_mj_per_gdp NUMERIC,
    co2_emissions_kt NUMERIC,
    renewables_pct_equivalent_primary_energy NUMERIC,
    gdp_growth NUMERIC,
    gdp_per_capita NUMERIC,
    UNIQUE (entity, year)
);