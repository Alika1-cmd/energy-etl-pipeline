-- 1. 10 negara dengan porsi energi terbarukan tertinggi di tahun 2019
SELECT entity, renewable_energy_share_pct
FROM fact_energy_yearly
WHERE year = 2019 AND renewable_energy_share_pct IS NOT NULL
ORDER BY renewable_energy_share_pct DESC
LIMIT 10;

-- 2. Tren rata-rata akses listrik dunia dari tahun ke tahun
SELECT year, ROUND(AVG(access_to_electricity_pct), 2) AS rata_rata_akses_listrik
FROM fact_energy_yearly
WHERE access_to_electricity_pct IS NOT NULL
GROUP BY year
ORDER BY year;

-- 3. 10 negara dengan akses listrik TERENDAH di tahun 2019 (isu ketimpangan)
SELECT entity, access_to_electricity_pct
FROM fact_energy_yearly
WHERE year = 2019 AND access_to_electricity_pct IS NOT NULL
ORDER BY access_to_electricity_pct ASC
LIMIT 10;

-- 4. Negara dengan kenaikan porsi energi terbarukan terbesar, 2000 vs 2019
SELECT
    a.entity,
    a.renewable_energy_share_pct AS share_2000,
    b.renewable_energy_share_pct AS share_2019,
    ROUND(b.renewable_energy_share_pct - a.renewable_energy_share_pct, 2) AS kenaikan
FROM fact_energy_yearly a
JOIN fact_energy_yearly b ON a.entity = b.entity
WHERE a.year = 2000 AND b.year = 2019
    AND a.renewable_energy_share_pct IS NOT NULL
    AND b.renewable_energy_share_pct IS NOT NULL
ORDER BY kenaikan DESC
LIMIT 10;