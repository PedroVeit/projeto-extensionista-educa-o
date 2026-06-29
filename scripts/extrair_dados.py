#extração dos microdados do ENEM 2019 e 2023

import os
import pandas as pd

BASE = os.path.join("..", "Microdados{ano}", "DADOS", "MICRODADOS_ENEM_{ano}.csv")
SAIDA = os.path.join("..", "dados-processados")

#colunas para fazer as análises
COLUNAS = [
    'NU_INSCRICAO', 'TP_FAIXA_ETARIA', 'TP_SEXO', 'TP_COR_RACA',
    'TP_ESCOLA', 'TP_DEPENDENCIA_ADM_ESC', 'SG_UF_PROVA', 
    'CO_MUNICIPIO_PROVA', 'NO_MUNICIPIO_PROVA',
    'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
    'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO',
    'Q001', 'Q002', 'Q006'
]

ESTADOS = ['RS', 'SP']


def extrair_ano(ano: int) -> None:
    csv_entrada = BASE.format(ano=ano)
    arquivo_saida = os.path.join(SAIDA, f"enem{ano}_RS_SP.parquet")

    print(f"\n[{ano}] Lendo {csv_entrada}")

    partes = []
    total_lido = 0

    #pedaços de 300 mil linhas para nao estourar a memória
    leitor = pd.read_csv(
        csv_entrada,
        sep=';',
        encoding='latin-1',
        usecols=COLUNAS,
        chunksize=300_000,
        low_memory=False
    )

    for chunk in leitor:
        total_lido += len(chunk)
        filtro = chunk[chunk['SG_UF_PROVA'].isin(ESTADOS)]
        partes.append(filtro)
        print(f"   ... lidos {total_lido:,} / filtrados {sum(len(p) for p in partes):,}")

    df = pd.concat(partes, ignore_index=True)
    df['NU_ANO'] = ano  #coluna pra identificar o ano depois

    df.to_parquet(arquivo_saida, index=False)
    print(f"[{ano}] Concluido: {len(df):,} linhas")
    print(f"[{ano}] Quebra por UF:\n{df['SG_UF_PROVA'].value_counts()}")
    print(f"[{ano}] Arquivo salvo em: {arquivo_saida}")


if __name__ == "__main__":
    os.makedirs(SAIDA, exist_ok=True)
    for ano in [2019, 2023]:
        extrair_ano(ano)
    print("\nExtração finalizada.")