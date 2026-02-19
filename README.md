# ISS Tracker

Aplicação simples em Streamlit que mostra a posição em tempo real da Estação Espacial Internacional (ISS) em um mapa.

## Visão geral

- Mostra a latitude, longitude e a última data/hora de atualização em uma caixa acima do mapa.
- Exibe a ISS no mapa utilizando uma imagem local (`iss.png`).
- Por padrão o projeto inclui um modo de simulação (gerando coordenadas aleatórias). É possível usar a API real removendo a simulação.

## Pré-requisitos

- Python 3.10+ (recomendado)
- `pip` ou `venv` para criar um ambiente virtual

## Instalação

1. Clone ou baixe o repositório.
2. Crie e ative um ambiente virtual (opcional, recomendado):

```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
# ou
. .venv/bin/activate
```

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando a aplicação

No diretório do projeto execute:

```bash
streamlit run app.py
```

Isso abrirá a interface Streamlit no navegador. A página mostrará a caixa com a última data/hora, latitude e longitude acima do mapa, botões de controle (Iniciar / Parar) centralizados e o ícone da ISS no mapa.

## Modo de simulação vs API real

Por padrão o projeto já usa a API real. Se precisar modificar ou dar manutenção enquanto o programa estiver em execução, remova a chamada à API e habilite o modo de simulação:

```python
# substituir (uso da API)
iss_lat, iss_lon = await get_iss_location(timeout=10.0)

# por (modo de simulação)
import random
iss_lat, iss_lon = random.uniform(-90, 90), random.uniform(-180, 180)
```

Certifique-se de que `iss_api.py` esteja presente e funcionando (usa `aiohttp` para consultar `http://api.open-notify.org/iss-now.json`).

## Arquivos importantes

- `app.py` — interface Streamlit e lógica de exibição
- `iss_api.py` — cliente assíncrono para obter a posição da ISS (usado se desativar o modo de simulação)
- `iss.png` — imagem usada como ícone da ISS no mapa
- `requirements.txt` — dependências do projeto

## Notas

- Se o ícone não aparecer, verifique o nome do arquivo e caminho (`iss.png`) e se o navegador permitiu o carregamento da imagem pelo pydeck.
- Ajuste o `timeout` e `zoom` em `app.py` conforme necessário.

## Aviso sobre erros de conexões

- Se ocorrerem erros de conexão ao usar a API real, verifique sua conexão com a internet e se o endpoint da API está acessível.
- O código inclui backoff exponencial com jitter para lidar com falhas temporárias na API, mas se os erros persistirem, pode ser necessário aumentar o número de tentativas ou o tempo entre elas.
- Para depuração, verifique os logs no console onde o Streamlit está rodando.
