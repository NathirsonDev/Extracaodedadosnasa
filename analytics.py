import pandas as pd
from sqlalchemy import create_engine

# Conectar ao banco que tu criaste (sem internet necessária!)
db_name = 'asteroides.db'
engine = create_engine(f'sqlite:///{db_name}')

print("--- RELATÓRIO DE INTELIGÊNCIA DE ASTEROIDES ---\n")

# PERGUNTA 1: Quantos asteroides são perigosos?
# SQL: SELECT conta tudo, AGRUPADO por periculosidade
query_perigo = """
SELECT 
    perigoso, 
    COUNT(*) as quantidade 
FROM neos 
GROUP BY perigoso
"""
df_perigo = pd.read_sql(query_perigo, con=engine)
print("1. Distribuição de Perigo:")
print(df_perigo)
print("-" * 30)

# PERGUNTA 2: Qual é o maior asteroide de todos?
# SQL: Selecione nome e diametro, ORDENE pelo diametro DESCENDENTE, pegue o TOP 1
query_big_boss = """
SELECT 
    id, 
    nome, 
    diametro_max_km, 
    data_aproximacao 
FROM neos 
ORDER BY diametro_max_km DESC 
LIMIT 1
"""
df_maior = pd.read_sql(query_big_boss, con=engine)

# Extraindo os dados para mostrar bonito
maior_nome = df_maior['nome'][0]
maior_tam = df_maior['diametro_max_km'][0]
maior_data = df_maior['data_aproximacao'][0]

print(f"2. O 'Godzilla' da semana:")
print(f"   Nome: {maior_nome}")
print(f"   Tamanho: {maior_tam:.3f} km (Isso são {maior_tam*1000:.0f} metros!)")
print(f"   Passou em: {maior_data}")
print("-" * 30)

# PERGUNTA 3: Média de tamanho dos perigosos vs não perigosos
# SQL: Média (AVG) agrupada por tipo
query_media = """
SELECT 
    perigoso, 
    AVG(diametro_max_km) as media_tamanho_km
FROM neos 
GROUP BY perigoso
"""
df_media = pd.read_sql(query_media, con=engine)
print("3. Comparação de Tamanho Médio:")
print(df_media)
print("-" * 30)