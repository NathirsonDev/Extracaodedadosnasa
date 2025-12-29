import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1. Conectar ao Banco
engine = create_engine('sqlite:///asteroides.db')

# 2. Puxar os dados
query = "SELECT data_aproximacao, diametro_max_km, perigoso, nome FROM neos"
df = pd.read_sql(query, con=engine)

# 3. Preparar o Gráfico
plt.figure(figsize=(12, 6)) # Tamanho da imagem

# Separar os grupos para pintar de cores diferentes
seguros = df[df['perigoso'] == False]
perigosos = df[df['perigoso'] == True]

# Plotar os Seguros (Azul, pequenos)
plt.scatter(
    seguros['data_aproximacao'], 
    seguros['diametro_max_km'], 
    c='blue', 
    alpha=0.5, # Transparência
    label='Seguro',
    s=50 # Tamanho da bolinha
)

# Plotar os Perigosos (Vermelho, grandes)
plt.scatter(
    perigosos['data_aproximacao'], 
    perigosos['diametro_max_km'], 
    c='red', 
    alpha=0.8, 
    label='PERIGOSO',
    s=150, # Bolinha maior para destacar
    edgecolors='black' # Borda preta para ficar agressivo
)

# Destacar o Godzilla (O maior de todos)
# Encontra o indice do maior valor
idx_max = df['diametro_max_km'].idxmax()
maior = df.loc[idx_max]

# Adiciona uma anotação (texto com seta) apontando para o maior
plt.annotate(
    f"GODZILLA: {maior['nome']}", 
    xy=(maior['data_aproximacao'], maior['diametro_max_km']),
    xytext=(10, -20), # Posição do texto relativa ao ponto
    textcoords='offset points',
    arrowprops=dict(facecolor='black', shrink=0.05)
)

# Perfumaria do Gráfico
plt.title('Monitoramento de Asteroides (NASA) - Última Semana')
plt.xlabel('Data de Aproximação')
plt.ylabel('Diâmetro Máximo (km)')
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend()
plt.xticks(rotation=45) # Girar as datas para caber

# 4. Salvar
plt.tight_layout()
plt.savefig('grafico_asteroides.png')
print("Gráfico gerado com sucesso: 'grafico_asteroides.png'")