# proj-pct-estatistico
Projeto em Python: Pacote Estatístico Simples

# estatistica_simples

Um pacote Python simples para realizar cálculos estatísticos básicos como média, mediana, desvio padrão e variância.

## Instalação

```bash
pip install estatistica_simples


# estrutura do pacote

estatistica_simples/
    ├── estatistica_simples/
    │   ├── __init__.py
    │   ├── medidas_tendencia_central.py
    │   ├── medidas_dispersao.py
    │   └── utilidades.py
    ├── setup.py
    └── README.md


# exemplo de uso

import estatistica_simples as est

dados = [1, 2, 3, 4, 5]

media = est.media(dados)
mediana = est.mediana(dados)
desvio_padrao = est.desvio_padrao(dados)

print(f"Média: {media}")
print(f"Mediana: {mediana}")
print(f"Desvio Padrão: {desvio_padrao}")