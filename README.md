# PHISHIELD

**Detecção Inteligente de Sites de Phishing por Aprendizado de Máquina: Uma Análise Comparativa com Ênfase em Generalização e Explicabilidade**

Projeto acadêmico de classificação binária para a G2 de Machine Learning. Entrega em 07/12/2026 e apresentação em 12/12/2026.

## Pergunta preditiva

É possível identificar URLs fraudulentas associadas a phishing, a partir de características observáveis das URLs e páginas web, utilizando modelos supervisionados de aprendizado de máquina capazes de generalizar para registros não utilizados no treinamento?

## Instalação e reprodução

As dependências fixadas exigem Python 3.12 ou superior. O ambiente foi verificado em Windows com Python 3.13.7. Crie e ative o ambiente virtual na raiz do projeto.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Em Linux ou macOS, ative com `source .venv/bin/activate`.

```sh
python -m pip install -r requirements.txt
python scripts/download_data.py
python -m pytest -q
python -m ruff check .
```

O download inicial precisa de acesso ao Kaggle e à UCI. `python scripts/download_data.py --only-uci` consulta somente a fonte oficial. As execuções reutilizam os arquivos locais e produzem registros JSON separados. Consulte [a auditoria de referência](results/data_audit/eedb92afaef04c27b08941e64df07dfc.json) e as [instruções dos dados](data/README.md).

Abra [o notebook 01](notebooks/01_obtencao_e_validacao.ipynb) em um ambiente Jupyter ou na extensão Jupyter do VS Code. Ele lê a auditoria registrada e apresenta somente os agregados da inspeção estrutural.

### Desenvolvimento e avaliação

Execute em uma cópia de trabalho com os dados oficiais. O comando de reserva é necessário quando o diretório de partições está vazio. Os índices da execução acadêmica estão versionados com seus hashes.

```sh
python scripts/prepare_data.py
python scripts/explore_data.py
python scripts/audit_collection.py
python scripts/run_experiments.py --rapido
python scripts/run_experiments.py
python scripts/summarize_experiments.py results/experiments/ID_DA_EXECUCAO
python scripts/check_collection_bias.py results/experiments/ID_DA_EXECUCAO/freeze.json
```

Use o identificador exibido pelo experimento completo. O modo rápido é um teste técnico e usa até 2.500 registros. A análise acadêmica usa o desenvolvimento completo.

A avaliação final é executada uma vez por partição e protegida por um marcador exclusivo. Para consultar a partição já avaliada, abra o notebook 08 ou leia as previsões e métricas persistidas. Em um ambiente dedicado à reprodução independente, o comando de avaliação é `python scripts/evaluate_final.py results/experiments/ID_DA_EXECUCAO/freeze.json`.

Use `python scripts/execute_notebooks.py` para atualizar as saídas dos oito notebooks da execução de referência. O notebook final lê apenas artefatos já persistidos.

### Aplicação local

```sh
python -m streamlit run app/streamlit_app.py
```

Gere os artefatos Joblib com a execução completa. A aplicação usa a mesma extração textual do cenário C e analisa endereços localmente.

## Documentação

- [Relatório inicial](RELATORIO.md)
- [Diário de desenvolvimento](DIARIO.md)
- [Matriz de requisitos](REQUISITOS.md)
- [Protocolo experimental](docs/protocolo_experimental.md)
- [Dicionário estrutural](docs/dicionario_dados.md)
- [Roteiro de apresentação](APRESENTACAO.md)
- [Arquitetura](docs/arquitetura.md)
- [Ficha do modelo](docs/ficha_modelo.md)
