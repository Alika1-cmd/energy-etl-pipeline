import pandas as pd

df = pd.read_csv("data/raw/global-data-on-sustainable-energy (1).csv")

print("Ukuran data:", df.shape)
print("\nNama kolom:")
for col in df.columns:
    print(repr(col))
print("\n5 baris pertama:")
print(df.head())

print("\nTipe data tiap kolom:")
print(df.dtypes)

print("\nJumlah missing value per kolom:")
print(df.isnull().sum())

print("\nJumlah baris duplikat:")
print(df.duplicated().sum())

print("\nJumlah kombinasi Entity-Year yang duplikat:")
print(df.duplicated(subset=["Entity", "Year"]).sum())

print("\nRentang tahun:", df["Year"].min(), "-", df["Year"].max())
print("Jumlah negara unik:", df["Entity"].nunique())

print("\nContoh isi kolom Density:")
print(df["Density\\n(P/Km2)"].dropna().unique()[:10])

density_col = "Density\\n(P/Km2)"

mengandung_koma = df[density_col].dropna().str.contains(",")
print("Jumlah nilai yang mengandung koma:", mengandung_koma.sum())
print("Contoh nilainya:", df[density_col].dropna()[mengandung_koma].unique()[:10])

# cek juga kalau ada karakter aneh selain angka dan koma
bukan_angka_murni = df[density_col].dropna().str.replace(",", "", regex=False).str.isnumeric()
print("\nJumlah nilai yang TIDAK murni angka (setelah koma dibuang):", (~bukan_angka_murni).sum())
print("Contoh nilai bermasalah:", df[density_col].dropna()[~bukan_angka_murni].unique()[:10])

kolom_geografis = ["Density\\n(P/Km2)", "Land Area(Km2)", "Latitude", "Longitude"]

for kolom in kolom_geografis:
    jumlah_nilai_unik = df.groupby("Entity")[kolom].nunique()
    print(f"\n{kolom}:")
    print(jumlah_nilai_unik.value_counts())

kolom_geografis = ["Density\\n(P/Km2)", "Land Area(Km2)", "Latitude", "Longitude"]
negara_data_kosong = df[df[kolom_geografis].isnull().any(axis=1)]["Entity"].unique()
print("Negara dengan data geografis kosong:", negara_data_kosong)