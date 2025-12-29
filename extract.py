import os
import requests
import pandas as pd
import time # Para dar uma pausa entre pedidos
from datetime import date, timedelta # Para lidar com datas
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('NASA_API_KEY')

# --- CONFIGURAÇÃO DO BANCO ---
db_name = 'asteroides.db'
engine = create_engine(f'sqlite:///{db_name}')

# --- DEFININDO O PERÍODO AUTOMATICAMENTE ---
hoje = date.today()
# Queremos os ultimos 7 dias (inclusive hoje)
data_inicio = hoje - timedelta(days=6) 

# Cria uma lista de datas: [Hoje-6, Hoje-5, ..., Hoje]
lista_de_datas = pd.date_range(start=data_inicio, end=hoje)

print(f"--- INICIANDO ETL: De {data_inicio} até {hoje} ---")

# --- O GRANDE LOOP ---
total_novos_acumulados = 0

for data_atual in lista_de_datas:
    # Converte a data para texto 'YYYY-MM-DD' (formato que a NASA pede)
    data_str = data_atual.strftime('%Y-%m-%d')
    
    print(f"\n> Processando dia: {data_str}...")
    
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    parametros = {
        'start_date': data_str,
        'end_date': data_str, # Pegamos 1 dia de cada vez para facilitar
        'api_key': api_key
    }

    try:
        resposta = requests.get(url, params=parametros)
        
        if resposta.status_code != 200:
            print(f"  [ERRO] A API recusou: {resposta.status_code}")
            continue # Pula para o proximo dia do loop

        dados = resposta.json()
        
        # O try/except aqui protege caso a NASA nao tenha dados para aquele dia
        try:
            lista_bruta = dados['near_earth_objects'][data_str]
        except KeyError:
            print("  [AVISO] Nenhum asteroide encontrado nesta data.")
            continue

        # Transforma em Lista de Dicionarios
        cesta = []
        for item in lista_bruta:
            cesta.append({
                'id': item['id'],
                'nome': item['name'],
                'perigoso': item['is_potentially_hazardous_asteroid'],
                'diametro_max_km': item['estimated_diameter']['kilometers']['estimated_diameter_max'],
                'data_aproximacao': data_str
            })
        
        df_novos = pd.DataFrame(cesta)
        
        # --- FILTRAGEM (IDEMPOTÊNCIA) ---
        inspector = inspect(engine)
        if inspector.has_table('neos'):
            ids_existentes = pd.read_sql("SELECT id FROM neos", con=engine)
            lista_ids_banco = ids_existentes['id'].astype(str).tolist()
            
            # Filtra apenas os que NÃO estão no banco
            df_para_salvar = df_novos[~df_novos['id'].isin(lista_ids_banco)]
        else:
            df_para_salvar = df_novos

        # --- SALVAR ---
        if not df_para_salvar.empty:
            df_para_salvar.to_sql('neos', con=engine, if_exists='append', index=False)
            print(f"  [SUCESSO] +{len(df_para_salvar)} asteroides novos salvos.")
            total_novos_acumulados += len(df_para_salvar)
        else:
            print("  [SKIP] Todos os asteroides deste dia já estavam no banco.")

        # Pausa de segurança para não ser bloqueado
        time.sleep(1) 

    except Exception as e:
        print(f"  [CRÍTICO] Falha no dia {data_str}: {e}")

print("\n" + "="*40)
print(f"FIM DO PROCESSO. Total adicionado na sessão: {total_novos_acumulados}")
print("="*40)

# Verificação final
total_geral = pd.read_sql("SELECT count(*) as total FROM neos", con=engine)
print(f"Total GERAL no Banco de Dados: {total_geral['total'][0]}")