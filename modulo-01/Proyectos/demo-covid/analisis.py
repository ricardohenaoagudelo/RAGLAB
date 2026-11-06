"""Analiza casos COVID-19 de Boyacá y genera un tablero agregado."""

from pathlib import Path
import html
import unicodedata

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
CSV = Path(__file__).resolve().parent / "casos_covid.csv"
OUT = ROOT / "docs" / "proyectos" / "demo-covid"
CHARTS = OUT / "graficos"
SOURCE = "https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia-/gt2j-8ykr/about_data"


def normalize(value):
    text = unicodedata.normalize("NFKD", str(value))
    return "".join(char for char in text if not unicodedata.combining(char)).strip().casefold()


def main():
    if not CSV.is_file():
        raise SystemExit(f"No se encontró el CSV: {CSV}")
    df = pd.read_csv(CSV, encoding="utf-8-sig", dtype=str)
    required = {"Fecha de diagnóstico", "Nombre departamento", "ID de caso", "Nombre municipio"}
    missing_columns = sorted(required - set(df.columns))
    if missing_columns:
        raise SystemExit(f"Faltan columnas necesarias: {', '.join(missing_columns)}")

    df["_date"] = pd.to_datetime(df["Fecha de diagnóstico"], errors="coerce", dayfirst=True)
    department = df["Nombre departamento"].fillna("").map(normalize)
    boyaca = df.loc[department.eq("boyaca")].copy()
    invalid_dates = int(boyaca["_date"].isna().sum())
    valid = boyaca.loc[boyaca["_date"].notna()].copy()
    case_ids = valid["ID de caso"].fillna("").str.strip()
    if case_ids.eq("").any() or case_ids.duplicated().any():
        raise SystemExit("ID de caso está vacío o repetido en Boyacá; se detuvo para no contar filas como casos.")
    valid["_month"] = valid["_date"].dt.to_period("M")
    monthly = valid.groupby("_month").size().sort_index()
    if monthly.empty:
        raise SystemExit("No hay fechas de diagnóstico válidas para Boyacá.")
    municipalities = valid.groupby("Nombre municipio").size().sort_values(ascending=False).head(10)
    changes = monthly.pct_change(fill_method=None) * 100
    period = f"{monthly.index.min()} a {monthly.index.max()}"

    CHARTS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly.index.astype(str), monthly.values, marker="o", color="#176b87")
    ax.set(title="Casos identificados por mes de diagnóstico — Boyacá", xlabel="Mes", ylabel="Casos (ID únicos)")
    ax.tick_params(axis="x", rotation=55)
    ax.grid(axis="y", alpha=.25)
    fig.tight_layout()
    fig.savefig(CHARTS / "casos_mensuales.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    municipalities.sort_values().plot.barh(ax=ax, color="#41a6a0")
    ax.set(title="Diez municipios con más casos identificados", xlabel="Casos (ID únicos)", ylabel="Municipio")
    fig.tight_layout()
    fig.savefig(CHARTS / "casos_por_municipio.png", dpi=150)
    plt.close(fig)

    change = "No calculable" if pd.isna(changes.iloc[-1]) else f"{changes.iloc[-1]:.1f}%"
    peak = monthly.idxmax()
    limitations = (
        f"Se excluyeron {invalid_dates:,} registros de Boyacá sin fecha de diagnóstico válida. "
        "Se cuentan ID de caso únicos; los resultados describen este CSV y no necesariamente todos los contagios. "
        "Fecha de diagnóstico no equivale a fecha de notificación o reporte."
    )
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>COVID-19 en Boyacá</title>
<style>body{{font:16px system-ui,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem;color:#18313b}}h1{{color:#176b87}}.cards{{display:flex;gap:1rem;flex-wrap:wrap}}.card{{background:#edf6f6;padding:1rem;border-radius:10px;flex:1;min-width:220px}}img{{max-width:100%;height:auto}}section{{margin:2rem 0}}</style></head><body>
<h1>Casos positivos de COVID-19 en Boyacá</h1><p><b>Departamento:</b> Boyacá · <b>Periodo de diagnóstico:</b> {html.escape(period)}</p>
<p>Pregunta: evolución mensual de casos identificados por ID de caso.</p><div class="cards"><p class="card"><b>Indicador 1</b><br>{int(monthly.sum()):,} casos identificados</p><p class="card"><b>Indicador 2</b><br>Cambio último mes frente al anterior: {change}</p></div>
<section><h2>Casos mensuales</h2><img src="graficos/casos_mensuales.png" alt="Casos identificados por mes"></section>
<section><h2>Distribución municipal</h2><img src="graficos/casos_por_municipio.png" alt="Casos por municipio"></section>
<section><h2>Hallazgo</h2><p>El máximo del periodo ocurrió en {html.escape(str(peak))}: {int(monthly.max()):,} casos identificados.</p></section>
<section><h2>Limitaciones</h2><p>{html.escape(limitations)}</p></section>
<p>Fuente: <a href="{SOURCE}">Portal Nacional de Datos Abiertos — Casos positivos de COVID-19 en Colombia</a>.</p>
<small>Reporte agregado; no se incluyen filas individuales.</small></body></html>'''
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print(f"Tablero generado: {OUT / 'index.html'}")
    print(f"Boyacá | Periodo {period} | Casos {int(monthly.sum())} | Cambio último mes {change} | Fechas inválidas excluidas {invalid_dates}")


if __name__ == "__main__":
    main()