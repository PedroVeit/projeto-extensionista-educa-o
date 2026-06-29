import pandas as pd
import os

SAIDA = os.path.join("..", "dados-processados")

for ano in [2019, 2023]:
    df = pd.read_parquet(os.path.join(SAIDA, f"enem{ano}_RS_SP.parquet"))

    #filtro de presenca nos 2 dias
    presentes = (df['TP_PRESENCA_CN']==1) & (df['TP_PRESENCA_CH']==1) & \
                (df['TP_PRESENCA_LC']==1) & (df['TP_PRESENCA_MT']==1)
    df = df[presentes].copy()
    # Nota média
    areas = ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT','NU_NOTA_REDACAO']
    df['NOTA_MEDIA'] = df[areas].mean(axis=1)
    
    #CSV para o BI
    saida_csv = os.path.join(SAIDA, f"enem{ano}_powerbi.csv")
    df.to_csv(saida_csv, sep=';', index=False, encoding='utf-8-sig')
    print(f"{ano}: {len(df):,} linhas -> {saida_csv}")

print("CSVs para o Power BI gerados.")