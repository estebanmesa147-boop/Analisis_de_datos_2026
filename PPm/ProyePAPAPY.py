import pandas as pd
import numpy as np
from scipy import stats
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings; warnings.filterwarnings('ignore')

C_VERDE='#1D9E75'; C_AMBER='#BA7517'; C_BLUE='#185FA5'
C_CORAL='#D85A30'; C_GRAY='#5F5E5A'

plt.rcParams.update({
    'figure.facecolor':'white','axes.facecolor':'#FAFAF8',
    'axes.spines.top':False,'axes.spines.right':False,
    'font.family':'DejaVu Sans','axes.grid':True,
    'grid.color':'#E0DED8','grid.linewidth':0.6,
})
print("Librerías cargadas ✓")

# Carga y Preparacion de datos 
RUTA_PRECIOS = 'Base_Precios_historica_13_2026.xlsx'
RUTA_ABASTOS = 'ABASTECIMIENTO_PAPA_2013_2025.csv'

meses_orden = {
    'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,
    'julio':7,'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12
}
nombres_mes = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']

# --- PRECIOS: filtrar Papa Superior ---
df_pre = pd.read_excel(RUTA_PRECIOS)
df_sup = df_pre[df_pre['variedad'] == 'Superior'].copy()
df_sup['mes_num'] = df_sup['mes'].str.lower().str.strip().map(meses_orden)
pm = df_sup.groupby(['year','mes_num'])['precio'].mean().reset_index()
pm.columns = ['año','mes_num','precio_prom']
pm['fecha'] = pd.to_datetime(dict(year=pm['año'], month=pm['mes_num'], day=1))

# --- ABASTECIMIENTO: filtrar Papa Superior ---
df_aba = pd.read_csv(RUTA_ABASTOS, sep=None, engine='python')
df_aba_sup = df_aba[df_aba['variedad'] == 'Superior'].copy()
df_aba_sup['mes_num'] = df_aba_sup['mes'].str.lower().str.strip().map(meses_orden)
am = df_aba_sup.groupby(['Año','mes_num'])['Toneladas'].sum().reset_index()
am.columns = ['año','mes_num','toneladas']
am['fecha'] = pd.to_datetime(dict(year=am['año'], month=am['mes_num'], day=1))

# --- Merge por período solapado ---
merged = pd.merge(pm, am, on=['año','mes_num','fecha']).sort_values('fecha').reset_index(drop=True)

print(f"Registros de precios (Superior):       {len(df_sup):,}")
print(f"Registros de abastecimiento (Superior): {len(df_aba_sup):,}")
print(f"Dataset unificado: {len(merged)} meses solapados")
print(f"Período: {merged['fecha'].min().strftime('%Y-%m')} → {merged['fecha'].max().strftime('%Y-%m')}")
print(f"Precio promedio: ${merged['precio_prom'].mean():,.0f} COP/kg")
print(f"Abastecimiento promedio: {merged['toneladas'].mean():,.0f} ton/mes")
merged.head(6)

#serie historica
pm_long = pm.sort_values('fecha')

fig, ax = plt.subplots(figsize=(13,4))
ax.plot(pm_long['fecha'], pm_long['precio_prom'], color=C_VERDE, lw=1.5)
ax.fill_between(pm_long['fecha'], pm_long['precio_prom'], alpha=0.1, color=C_VERDE)
ax.set_title('Precio promedio mensual — Papa Superior · Colombia 2014-2026',
             fontsize=13, fontweight='500', pad=10)
ax.set_ylabel('COP / kg', fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${x:,.0f}'))
plt.tight_layout(); plt.show()

#Regresion
slope1, intercept1, r1, p1, se1 = stats.linregress(merged['toneladas'], merged['precio_prom'])
pred1 = intercept1 + slope1 * merged['toneladas']
rmse1 = np.sqrt(mean_squared_error(merged['precio_prom'], pred1))
r2_1  = r1**2

print("="*58)
print("REGRESIÓN 1: Precio ~ Abastecimiento — Papa Superior")
print("="*58)
print(f"  Ecuación : precio = {intercept1:.2f} + {slope1:.5f} × toneladas")
print(f"  R²       : {r2_1:.4f}  ({r2_1*100:.1f}% varianza explicada)")
print(f"  r Pearson: {r1:.4f}")
print(f"  p-valor  : {p1:.5f}  {'*** SIGNIFICATIVO (p<0.05)' if p1<0.05 else '(no significativo)'}")
print(f"  RMSE     : ${rmse1:,.2f} COP/kg")
print()
sentido = 'BAJA' if slope1<0 else 'SUBE'
print(f"  ► Por cada 1.000 ton adicionales de Papa Superior")
print(f"    el precio {sentido} ${abs(slope1)*1000:.2f} COP/kg")
print()
if slope1 > 0:
    print("  ⚠ Nota: relación positiva sugiere que ambas variables")
    print("    crecen en el tiempo (tendencia común). Considerar")
    print("    análisis con variables detrended.")

fig, ax = plt.subplots(figsize=(8,5))
ax.scatter(merged['toneladas']/1000, merged['precio_prom'],
           alpha=0.55, s=32, color=C_BLUE, edgecolors='white', lw=0.4,
           label='Observaciones mensuales')
xr = np.linspace(merged['toneladas'].min(), merged['toneladas'].max(), 200)
ax.plot(xr/1000, intercept1+slope1*xr, color=C_CORAL, lw=2,
        label=f'OLS  R²={r2_1:.3f}  p={p1:.4f}')
ax.set_xlabel('Abastecimiento Papa Superior (miles de toneladas)', fontsize=10)
ax.set_ylabel('Precio promedio (COP/kg)', fontsize=10)
ax.set_title('Regresión 1: Precio ~ Abastecimiento · Papa Superior', fontsize=13, fontweight='500', pad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${x:,.0f}'))
ax.legend(fontsize=9)
txt = (f'y = {intercept1:.0f} + {slope1:.4f}·ton\n'
       f'R² = {r2_1:.3f}   RMSE = ${rmse1:,.0f}/kg')
ax.text(0.97,0.05,txt,transform=ax.transAxes,ha='right',va='bottom',fontsize=9,
        bbox=dict(boxstyle='round,pad=0.4',facecolor='white',edgecolor='#D3D1C7'))
plt.tight_layout(); plt.show()

#Regresion 2

df2 = merged.copy()
df2['t'] = np.arange(len(df2))
for m in range(2,13): df2[f'm{m}'] = (df2['mes_num']==m).astype(int)

feat_cols = ['t'] + [f'm{m}' for m in range(2,13)]
X2c = np.column_stack([np.ones(len(df2)), df2[feat_cols].values])
y2  = df2['precio_prom'].values

# OLS
beta, *_ = np.linalg.lstsq(X2c, y2, rcond=None)
y_hat2   = X2c @ beta
resid2   = y2 - y_hat2
n, k     = X2c.shape
mse2     = np.sum(resid2**2) / (n - k)
inv_XX   = np.linalg.inv(X2c.T @ X2c)
se_b     = np.sqrt(np.diag(mse2 * inv_XX))
t_st     = beta / se_b
p_v      = 2 * stats.t.sf(np.abs(t_st), df=n-k)
r2_2     = r2_score(y2, y_hat2)
rmse2    = np.sqrt(mean_squared_error(y2, y_hat2))

print("="*62)
print("REGRESIÓN 2: Precio ~ Tendencia + Dummies de mes — Papa Superior")
print("="*62)
nombres_param = ['constante','tendencia'] + [f'mes_{m:02d}' for m in range(2,13)]
for nm, b, se, t, p in zip(nombres_param, beta, se_b, t_st, p_v):
    sig = '***' if p<0.01 else '**' if p<0.05 else '*' if p<0.1 else ''
    print(f"  {nm:14s}: {b:+9.2f}   se={se:7.2f}   t={t:+6.2f}   p={p:.4f} {sig}")
print()
print(f"  R²        : {r2_2:.4f}  ({r2_2*100:.1f}% varianza explicada)")
print(f"  RMSE      : ${rmse2:,.2f} COP/kg")
print(f"  Tendencia : +{beta[1]:.2f} COP/kg por mes  (+${beta[1]*12:.0f}/kg por año)")

efectos = [0] + [beta[i] for i in range(2, 13)]

fig, ax = plt.subplots(figsize=(9,4))
colors = [C_AMBER if e >= 0 else C_BLUE for e in efectos]
bars = ax.bar(nombres_mes, efectos, color=colors, width=0.62, edgecolor='white', lw=0.5)
ax.axhline(0, color=C_GRAY, lw=1)
ax.set_title('Efecto estacional mensual — Papa Superior (vs. enero)',
             fontsize=13, fontweight='500', pad=10)
ax.set_ylabel('Diferencia precio (COP/kg)', fontsize=10)
for bar, val in zip(bars, efectos):
    off = 6 if val >= 0 else -28
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+off,
            f'{val:+.0f}', ha='center', va='bottom', fontsize=8.5, color=C_GRAY)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{x:+,.0f}'))
plt.tight_layout(); plt.show()

#Diagnostico 
fig, axes = plt.subplots(1, 3, figsize=(13,4))

# Residuales vs ajustados
axes[0].scatter(y_hat2, resid2, alpha=0.45, s=24, color=C_BLUE, edgecolors='white', lw=0.3)
axes[0].axhline(0, color=C_CORAL, lw=1.5)
axes[0].set_xlabel('Valores ajustados (COP/kg)', fontsize=9)
axes[0].set_ylabel('Residuales (COP/kg)', fontsize=9)
axes[0].set_title('Residuales vs Ajustados', fontsize=11, fontweight='500')

# Q-Q
(osm, osr), (sq, iq, _) = stats.probplot(resid2, dist='norm')
axes[1].scatter(osm, osr, alpha=0.45, s=24, color=C_VERDE, edgecolors='white', lw=0.3)
xq = np.array([osm.min(), osm.max()])
axes[1].plot(xq, sq*xq+iq, color=C_CORAL, lw=1.5)
axes[1].set_xlabel('Cuantiles teóricos', fontsize=9)
axes[1].set_ylabel('Cuantiles observados', fontsize=9)
axes[1].set_title('Q-Q Normal', fontsize=11, fontweight='500')

# Histograma
axes[2].hist(resid2, bins=20, color=C_AMBER, edgecolor='white', lw=0.5, alpha=0.85)
axes[2].set_xlabel('Residuales (COP/kg)', fontsize=9)
axes[2].set_ylabel('Frecuencia', fontsize=9)
axes[2].set_title('Distribución de residuales', fontsize=11, fontweight='500')
axes[2].text(0.97,0.95,f'μ={resid2.mean():.1f}\nσ={resid2.std():.1f}',
             transform=axes[2].transAxes, ha='right', va='top', fontsize=9,
             bbox=dict(boxstyle='round,pad=0.3',facecolor='white',edgecolor='#D3D1C7'))
plt.tight_layout(pad=2); plt.show()

#prediccion

t_crit = stats.t.ppf(0.975, df=n-k)
last_t   = df2['t'].max()
last_mes = df2['mes_num'].iloc[-1]
last_yr  = df2['año'].iloc[-1]

rows = []
for yr in [2026, 2027, 2028]:
    for mn in range(1, 13):
        t_val = last_t + (yr - last_yr)*12 + (mn - last_mes)
        xrow  = np.array([1, t_val] + [int(mn==m) for m in range(2,13)])
        pred  = float(beta @ xrow)
        se_p  = np.sqrt(mse2 * (1 + xrow @ inv_XX @ xrow))
        rows.append({
            'año': yr, 'mes': mn,
            'fecha': pd.Timestamp(yr, mn, 1),
            'precio_pred': pred,
            'ci_lo': pred - t_crit*se_p,
            'ci_hi': pred + t_crit*se_p
        })
pred_df = pd.DataFrame(rows)

print("Predicción de precio Papa Superior (COP/kg)")
print("-"*60)
for _, r in pred_df.iterrows():
    print(f"  {r['fecha'].strftime('%Y-%m')}:  ${r['precio_pred']:7,.0f}  "
          f"  IC95%: [${r['ci_lo']:,.0f} – ${r['ci_hi']:,.0f}]")
    
fig, ax = plt.subplots(figsize=(13,5))

se_obs = np.sqrt(mse2*(1 + np.diag(X2c @ inv_XX @ X2c.T)))
ax.plot(merged['fecha'], merged['precio_prom'], color=C_VERDE, lw=1.4, alpha=0.9,
        label='Histórico (Papa Superior)')
ax.plot(merged['fecha'], y_hat2, color=C_BLUE, lw=1.8, ls='--',
        label=f'Modelo ajustado (R²={r2_2:.3f})')
ax.fill_between(merged['fecha'], y_hat2-t_crit*se_obs, y_hat2+t_crit*se_obs,
                alpha=0.12, color=C_BLUE, label='IC 95% ajuste')
ax.plot(pred_df['fecha'], pred_df['precio_pred'], color=C_CORAL, lw=2.2,
        label='Predicción 2026-28')
ax.fill_between(pred_df['fecha'], pred_df['ci_lo'], pred_df['ci_hi'],
                alpha=0.14, color=C_CORAL, label='IC 95% pred.')
ax.axvline(merged['fecha'].max(), color=C_GRAY, lw=1, ls=':', alpha=0.7)
ax.set_title('Precio Papa Superior — ajuste del modelo y predicción 2026-2028',
             fontsize=13, fontweight='500', pad=10)
ax.set_ylabel('COP / kg', fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'${x:,.0f}'))
ax.legend(fontsize=9, loc='upper left')
plt.tight_layout(); plt.show()

# Exportar 

with pd.ExcelWriter('resultados_papa_superior.xlsx', engine='openpyxl') as writer:
    merged.to_excel(writer, sheet_name='datos_historicos', index=False)
    pred_df[['fecha','año','mes','precio_pred','ci_lo','ci_hi']].to_excel(
        writer, sheet_name='predicciones_2026_2028', index=False)
    pd.DataFrame({
        'variable': ['constante','tendencia'] + [f'mes_{m:02d}' for m in range(2,13)],
        'coeficiente': beta, 'error_est': se_b, 't_stat': t_st, 'p_valor': p_v
    }).to_excel(writer, sheet_name='coeficientes_reg2', index=False)

print("✓ resultados_papa_superior.xlsx generado")
