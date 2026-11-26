# PHISHIELD

**Detecção Inteligente de Sites de Phishing por Aprendizado de Máquina: Uma Análise Comparativa com Ênfase em Generalização e Explicabilidade**

Projeto acadêmico de classificação binária para a G2 de Machine Learning. Entrega em 07/12/2026 e apresentação em 12/12/2026.

Phishing usa páginas e endereços enganosos para induzir ações como informar credenciais. O PHISHIELD investiga quais sinais observáveis ajudam a identificar essa classe e se as previsões se sustentam em domínios inéditos da mesma coleta.

## Objetivos e dados

Auditar os preditores, comparar cinco classificadores e uma referência trivial, medir generalização por domínio e demonstrar inferência lexical local. A fonte é o PhiUSIIL UCI 967, com 235.795 linhas, 54 preditores, 100.945 registros de phishing e 134.850 legítimos. A edição Kaggle indicada no enunciado foi auditada em separado. [Catálogo UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset) · [Dados e licença](data/README.md)

## Metodologia, modelos e tecnologias

O teste agrupado é reservado antes da exploração. Os pipelines ajustam imputação, codificação e escalonamento dentro dos folds. A métrica primária é F1 de phishing. A comparação inclui Dummy, regressão logística, árvore de decisão, Random Forest, HistGradientBoosting e GaussianNB. O estudo usa Python, Pandas, NumPy, scikit-learn, Matplotlib, Jupyter, Streamlit, Pytest e Ruff. [Metodologia](docs/metodologia.md)

| Diretório | Conteúdo |
|---|---|
| `data/` e `configs/` | Proveniência, índices da reserva e parâmetros de execução |
| `src/phishield/` e `scripts/` | Implementação reutilizável e comandos reproduzíveis |
| `results/` e `models/` | Evidências experimentais e artefatos locais |
| `notebooks/` e `docs/` | Narrativa científica, arquitetura e decisões |
| `app/` e `tests/` | Demonstração local e verificações automatizadas |

## Resultados e limitações

Na reserva de 46.760 linhas, o modelo principal atingiu F1 de 0,99982, com 3 falsos positivos e 4 falsos negativos. O lexical atingiu F1 de 0,99645. No subconjunto interno de formato comum às duas classes, o F1 lexical foi 0,71910. A avaliação mede generalização por domínio na mesma coleta. Validação temporal e externa ainda são trabalhos futuros. [Relatório](RELATORIO.md)

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

Execute em uma cópia de trabalho com os dados oficiais. O comando de reserva gera os índices quando o diretório está vazio e verifica os hashes quando a reserva já existe. Os índices da execução acadêmica estão versionados.

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

Novas execuções registram os índices dos folds agrupados, internos e aleatórios, hashes de código e dependências e um inventário dos artefatos. Os folds internos e aleatórios do estudo inicial foram reconstruídos separadamente a partir do desenvolvimento e conferidos contra os cinco folds externos originais. [Verificação da reconstrução](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/reconstrucao_folds.json)

A avaliação final é executada uma vez por partição e protegida por um marcador exclusivo. Para consultar a partição já avaliada, abra o notebook 08 ou leia as previsões e métricas persistidas. Em um ambiente dedicado à reprodução independente, o comando de avaliação é `python scripts/evaluate_final.py results/experiments/ID_DA_EXECUCAO/freeze.json`.

Use `python scripts/execute_notebooks.py` para atualizar as saídas dos oito notebooks da execução de referência. O notebook final lê apenas artefatos já persistidos.

A ordem é 01 obtenção e validação, 02 exploração, 03 auditoria e preparação, 04 baselines, 05 otimização, 06 comparação, 07 explicabilidade e 08 avaliação final.

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

## Referências e integrantes

Prasad e Chandra descrevem a construção da base e seus atributos. As referências dos algoritmos e do estudo estão no relatório. [Publicação dos autores](https://doi.org/10.1016/j.cose.2023.103545) · [Referências do projeto](RELATORIO.md#referências)

- Integrante 1 — nome pendente
- Integrante 2 — nome pendente
- Integrante 3 — nome pendente
