import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "vendas_oltp")

BASE_DRIVE = Path(r"D:\drive\projeto GitHUb")
BRONZE_DIR = BASE_DRIVE / "data-lake-portfolio-bronze"
GOLD_DIR = BASE_DRIVE / "data-lake-portfolio-gold"

BRONZE_DIR.mkdir(parents=True, exist_ok=True)
GOLD_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def extrair_para_bronze():
    print("1. Extraindo tabelas do PostgreSQL para a camada Bronze...")
    tabelas = ["clientes", "produtos", "pedidos"]
    dados = {}

    for tabela in tabelas:
        df = pd.read_sql(f"SELECT * FROM {tabela}", engine)
        df["data_extracao"] = datetime.now()
        df.to_parquet(BRONZE_DIR / f"{tabela}.parquet", index=False)
        df.to_csv(BRONZE_DIR / f"{tabela}.csv", index=False, encoding="utf-8-sig")
        dados[tabela] = df
        print(f"   [OK] {tabela}: {len(df)} linhas salvas em Bronze.")

    return dados

def transformar_para_gold(dados):
    print("\n2. Modelando Star Schema para a camada Gold...")

    dim_clientes = dados["clientes"][["cliente_id", "nome", "email", "cidade", "estado"]].copy()
    dim_clientes["nome"] = dim_clientes["nome"].str.strip().str.upper()

    dim_produtos = dados["produtos"][["produto_id", "nome_produto", "categoria", "preco_unitario"]].copy()

    fato_vendas = dados["pedidos"][[
        "pedido_id", "cliente_id", "produto_id", "quantidade", "valor_total", "status_pedido", "data_pedido"
    ]].copy()
    fato_vendas["data_carga_dw"] = datetime.now()

    tabelas_gold = {
        "dim_clientes": dim_clientes,
        "dim_produtos": dim_produtos,
        "fato_vendas": fato_vendas,
    }

    for nome, df_gold in tabelas_gold.items():
        df_gold.to_parquet(GOLD_DIR / f"{nome}.parquet", index=False)
        df_gold.to_csv(GOLD_DIR / f"{nome}.csv", index=False, encoding="utf-8-sig")
        print(f"   [OK] {nome}: {len(df_gold)} linhas salvas em Gold.")

if __name__ == "__main__":
    dados_extraidos = extrair_para_bronze()
    transformar_para_gold(dados_extraidos)
    print("\nPipeline finalizado com sucesso!")