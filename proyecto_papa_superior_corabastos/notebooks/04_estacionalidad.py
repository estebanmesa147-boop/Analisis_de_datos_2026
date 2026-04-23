# =============================================================
# PROYECTO: Análisis Papa Superior Corabastos (2019-2025)
# FASE 4: Estacionalidad
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

sns.set_theme(style='whitegrid')
plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.family'] = 'sans-serif'

# --- RUTAS ---
PROCESSED = r"C:\Users\user\Desktop\Analisis de Datos 2026\proyecto_papa_superior_corabastos\data\processed"

meses_orden = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
               'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
mes_num = {m: str(i+1).zfill(2) for i, m in enumerate(meses_orden)}

# =============================================================
# CARGAR Y PREPARAR SERIE DE TIEMPO
# =============================================================
# Usamos el dataset con IPC generado en la Fase 3b
df = pd.read_parquet(f"{PROCESSED}\\papa_superior_corabastos_con_ipc.parquet")
df['mes'] = pd.Categorical(df['mes'], categories=meses_orden, ordered=True)
df = df.sort_values(['Año','mes']).reset_index(drop=True)

# Crear índice de fecha mensual
df['fecha'] = pd.to_datetime(
    df['Año'].astype(str) + '-' + df['mes'].astype(str).map(mes_num) + '-01'
)
df = df.set_index('fecha')

print(df.shape)
print(df.head())

# =============================================================
# DESCOMPOSICIÓN DE LA SERIE DE PRECIOS
# =============================================================
descomp = seasonal_decompose(
    df['precio_promedio'],
    model='additive',
    period=12
)

fig, axes = plt.subplots(4, 1, figsize=(13, 10), sharex=True)

descomp.observed.plot(ax=axes[0], color='#333333', linewidth=1.5)
axes[0].set_ylabel('Precio original')
axes[0].set_title('Descomposición de la serie de precios — Papa Superior Corabastos (2019–2025)',
                  fontsize=13, fontweight='bold')

descomp.trend.plot(ax=axes[1], color='#E07B39', linewidth=2)
axes[1].set_ylabel('Tendencia')

descomp.seasonal.plot(ax=axes[2], color='#4C9BE8', linewidth=1.5)
axes[2].set_ylabel('Estacionalidad')

descomp.resid.plot(ax=axes[3], color='#888888', linewidth=1, marker='o', markersize=3)
axes[3].set_ylabel('Residuo')
axes[3].set_xlabel('Fecha')

for ax in axes:
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig(f"{PROCESSED}\\grafico_descomposicion_precio.png", bbox_inches='tight')
plt.show()

# =============================================================
# PRECIO PROMEDIO POR MES (patrón estacional)
# =============================================================
df['mes_str'] = df['mes'].astype(str)
estacional_precio = df.groupby('mes_str')['precio_promedio'].mean().reindex(meses_orden)

fig, ax = plt.subplots(figsize=(12, 5))
colores = ['#E07B39' if v == estacional_precio.max()
           else '#4C9BE8' if v == estacional_precio.min()
           else '#A8C8E8' for v in estacional_precio.values]

bars = ax.bar(meses_orden, estacional_precio.values, color=colores, edgecolor='white', width=0.7)

for bar, val in zip(bars, estacional_precio.values):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 15,
            f'${val:,.0f}', ha='center', fontsize=9)

ax.set_title('Precio promedio histórico por mes — Papa Superior Corabastos (2019–2025)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Mes')
ax.set_ylabel('Precio promedio ($/kg)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig(f"{PROCESSED}\\grafico_estacional_precio.png", bbox_inches='tight')
plt.show()

print(f"Mes más caro:   {estacional_precio.idxmax()} (${estacional_precio.max():,.0f})")
print(f"Mes más barato: {estacional_precio.idxmin()} (${estacional_precio.min():,.0f})")

# =============================================================
# ABASTECIMIENTO PROMEDIO POR MES
# =============================================================
estacional_abast = df.groupby('mes_str')['Toneladas'].mean().reindex(meses_orden)

fig, ax = plt.subplots(figsize=(12, 5))
colores_a = ['#2E7D32' if v == estacional_abast.max()
             else '#C62828' if v == estacional_abast.min()
             else '#A5D6A7' for v in estacional_abast.values]

bars = ax.bar(meses_orden, estacional_abast.values, color=colores_a, edgecolor='white', width=0.7)

for bar, val in zip(bars, estacional_abast.values):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 100,
            f'{val:,.0f}', ha='center', fontsize=9)

ax.set_title('Abastecimiento promedio histórico por mes — Papa Superior Corabastos (2019–2025)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Mes')
ax.set_ylabel('Toneladas')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig(f"{PROCESSED}\\grafico_estacional_abastecimiento.png", bbox_inches='tight')
plt.show()

print(f"Mes mayor abasto: {estacional_abast.idxmax()} ({estacional_abast.max():,.0f} t)")
print(f"Mes menor abasto: {estacional_abast.idxmin()} ({estacional_abast.min():,.0f} t)")

# =============================================================
# EVOLUCIÓN MENSUAL POR AÑO (líneas superpuestas)
# =============================================================
años    = sorted(df['Año'].unique())
colores = sns.color_palette('tab10', len(años))

fig, ax = plt.subplots(figsize=(13, 6))

for año, color in zip(años, colores):
    sub  = df[df['Año'] == año]
    vals = sub['precio_promedio'].reindex(
        pd.date_range(f'{año}-01-01', f'{año}-12-01', freq='MS')
    ).values
    ax.plot(meses_orden[:len(vals)], vals,
            marker='o', linewidth=2, label=str(año), color=color, markersize=5)

ax.set_title('Evolución mensual del precio por año — Papa Superior Corabastos',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Mes')
ax.set_ylabel('Precio promedio ($/kg)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.legend(title='Año', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig(f"{PROCESSED}\\grafico_lineas_por_año.png", bbox_inches='tight')
plt.show()

# =============================================================
# GUARDAR ÍNDICE ESTACIONAL
# =============================================================
estacional_df = pd.DataFrame({
    'mes'                          : meses_orden,
    'precio_promedio_historico'    : estacional_precio.values.round(2),
    'toneladas_promedio_historico' : estacional_abast.values.round(2)
})

estacional_df.to_csv(f"{PROCESSED}\\indice_estacional.csv", index=False)
print("✅ Índice estacional guardado")
print()
print(estacional_df.to_string(index=False))
