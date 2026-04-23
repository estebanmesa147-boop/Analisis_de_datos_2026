# =============================================================
# PROYECTO: Análisis Papa Superior Corabastos (2019-2025)
# FASE 3B: IPC alimentos y precio real deflactado
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats

sns.set_theme(style='whitegrid')
plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.family'] = 'sans-serif'

# --- RUTAS ---
RAW       = r"C:\Users\user\Desktop\Analisis de Datos 2026\proyecto_papa_superior_corabastos\data\raw"
PROCESSED = r"C:\Users\user\Desktop\Analisis de Datos 2026\proyecto_papa_superior_corabastos\data\processed"

meses_orden = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
               'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
mes_num = {m: str(i+1).zfill(2) for i, m in enumerate(meses_orden)}

# =============================================================
# PASO 1: Cargar y construir índice IPC
# =============================================================
df_ipc = pd.read_excel(f"{RAW}\\graficador_seriesf.xlsx", sheet_name='Datos', skiprows=2)
df_ipc.columns = ['fecha', 'ipc_alimentos']
df_ipc = df_ipc[df_ipc['fecha'].notna() & (df_ipc['fecha'] != '')]
df_ipc = df_ipc[~df_ipc['fecha'].astype(str).str.contains('Descargado')]
df_ipc['fecha'] = pd.to_datetime(df_ipc['fecha'], format='%d/%m/%Y')
df_ipc['ipc_alimentos'] = df_ipc['ipc_alimentos'].astype(str).str.replace(',', '.').astype(float)
df_ipc = df_ipc[df_ipc['fecha'].dt.year.between(2019, 2025)].reset_index(drop=True)

# Construir índice acumulado base 100 = enero 2019
df_ipc['factor_mensual'] = (1 + df_ipc['ipc_alimentos'] / 100) ** (1/12)
df_ipc['indice'] = 100.0
for i in range(1, len(df_ipc)):
    df_ipc.loc[i, 'indice'] = df_ipc.loc[i-1, 'indice'] * df_ipc.loc[i, 'factor_mensual']

print("IPC construido correctamente")
print(f"Índice enero 2019:     100.0")
print(f"Índice diciembre 2025: {df_ipc.iloc[-1]['indice']:.2f}")
print("Interpretación: los alimentos costaban 88.65% más en dic-2025 que en ene-2019")

# =============================================================
# PASO 2: Unir IPC con dataset maestro
# =============================================================
df = pd.read_parquet(f"{PROCESSED}\\papa_superior_corabastos_2019_2025.parquet")
df['mes'] = pd.Categorical(df['mes'], categories=meses_orden, ordered=True)
df = df.sort_values(['Año','mes']).reset_index(drop=True)

df['fecha'] = pd.to_datetime(
    df['Año'].astype(str) + '-' + df['mes'].astype(str).map(mes_num) + '-01'
)

df_ipc['fecha_merge'] = df_ipc['fecha'].values.astype('datetime64[M]').astype('datetime64[D]')
df['fecha_merge']     = df['fecha'].values.astype('datetime64[M]').astype('datetime64[D]')

df = pd.merge(df, df_ipc[['fecha_merge','ipc_alimentos','indice']], on='fecha_merge', how='left')

# Calcular precio real (base enero 2019 = 100)
df['precio_real'] = (df['precio_promedio'] / df['indice']) * 100

print("Merge exitoso. Shape:", df.shape)
print()
print(df[['Año','mes','precio_promedio','indice','precio_real']].head(12).to_string())

# =============================================================
# GRÁFICA 1: Precio nominal vs precio real
# =============================================================
df_anual = df.groupby('Año').agg(
    precio_nominal = ('precio_promedio', 'mean'),
    precio_real    = ('precio_real', 'mean')
).reset_index()

fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(df_anual['Año'], df_anual['precio_nominal'],
        marker='o', linewidth=2.5, color='#E07B39',
        label='Precio nominal ($/kg)')
ax.plot(df_anual['Año'], df_anual['precio_real'],
        marker='s', linewidth=2.5, color='#4C9BE8',
        linestyle='--', label='Precio real (base ene-2019)')

for _, row in df_anual.iterrows():
    ax.annotate(f"${row['precio_nominal']:,.0f}",
                xy=(row['Año'], row['precio_nominal']),
                xytext=(0, 12), textcoords='offset points',
                ha='center', fontsize=8, color='#E07B39')
    ax.annotate(f"${row['precio_real']:,.0f}",
                xy=(row['Año'], row['precio_real']),
                xytext=(0, -18), textcoords='offset points',
                ha='center', fontsize=8, color='#4C9BE8')

ax.set_title('Precio nominal vs precio real — Papa Superior Corabastos (2019–2025)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Año')
ax.set_ylabel('$/kg')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_xticks(df_anual['Año'])
ax.legend()
plt.tight_layout()
plt.savefig(f"{PROCESSED}\\grafico_precio_nominal_vs_real.png", bbox_inches='tight')
plt.show()

# =============================================================
# CORRELACIONES: nominal vs real vs abastecimiento vs IPC
# =============================================================
pearson_nom,  p_nom   = stats.pearsonr(df['Toneladas'], df['precio_promedio'])
pearson_real, p_real  = stats.pearsonr(df['Toneladas'], df['precio_real'])
spearman_nom, _       = stats.spearmanr(df['Toneladas'], df['precio_promedio'])
spearman_real, _      = stats.spearmanr(df['Toneladas'], df['precio_real'])

# Precio nominal vs IPC
pearson_ipc_nom,  _ = stats.pearsonr(df['ipc_alimentos'], df['precio_promedio'])
pearson_ipc_real, _ = stats.pearsonr(df['ipc_alimentos'], df['precio_real'])

resumen = pd.DataFrame({
    'Correlación'  : ['Toneladas vs precio nominal',
                      'Toneladas vs precio real',
                      'IPC alimentos vs precio nominal',
                      'IPC alimentos vs precio real'],
    'Pearson r'    : [round(pearson_nom,4),     round(pearson_real,4),
                      round(pearson_ipc_nom,4), round(pearson_ipc_real,4)],
    'Spearman r'   : [round(spearman_nom,4), round(spearman_real,4), '-', '-']
})

print()
print(resumen.to_string(index=False))

# =============================================================
# GRÁFICA 2: Scatter comparativo nominal vs real
# =============================================================
años    = sorted(df['Año'].unique())
colores = sns.color_palette('tab10', len(años))

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

for ax, col, titulo in zip(axes,
                            ['precio_promedio', 'precio_real'],
                            ['Precio nominal', 'Precio real (deflactado)']):
    for año, color in zip(años, colores):
        sub = df[df['Año'] == año]
        ax.scatter(sub['Toneladas'], sub[col],
                   label=str(año), color=color, s=60, alpha=0.85)

    m, b, *_ = stats.linregress(df['Toneladas'], df[col])
    x_range  = pd.Series([df['Toneladas'].min(), df['Toneladas'].max()])
    r        = stats.pearsonr(df['Toneladas'], df[col])[0]
    ax.plot(x_range, m * x_range + b, color='black',
            linewidth=1.5, linestyle='--', label=f'Tendencia (r={r:.2f})')

    ax.set_title(f'{titulo} vs Abastecimiento', fontsize=12, fontweight='bold')
    ax.set_xlabel('Toneladas')
    ax.set_ylabel('$/kg')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend(title='Año', fontsize=7, title_fontsize=8)

plt.suptitle('Comparación correlación: precio nominal vs precio real\nPapa Superior Corabastos (2019–2025)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{PROCESSED}\\grafico_scatter_nominal_vs_real.png", bbox_inches='tight')
plt.show()

# =============================================================
# GUARDAR DATASET ENRIQUECIDO CON IPC
# =============================================================
df.to_csv(f"{PROCESSED}\\papa_superior_corabastos_con_ipc.csv", index=False)
df.to_parquet(f"{PROCESSED}\\papa_superior_corabastos_con_ipc.parquet", index=False)
print("✅ Dataset con IPC guardado")
