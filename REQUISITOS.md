# Matriz de rastreabilidade

| ID | Requisito acadêmico | Implementação | Evidência | Situação |
|---|---|---|---|---|
| 01 | Pelo menos 1.000 registros e seis preditores | UCI 967 com 235.795 linhas e 54 preditores | [Auditoria](results/data_audit/eedb92afaef04c27b08941e64df07dfc.json) | Validado |
| 02 | Uma pergunta preditiva | Pergunta central única | [README](README.md) | Validado |
| 03 | Classificação ou regressão | Classificação binária, phishing positivo | [Métricas finais](results/final/39293c0cc63702da8f5475cb060b878905ac68284c06479919d0f138e8157b8f/metrics.json) | Validado |
| 04 | EDA antes da modelagem | Exploração após reserva e antes dos baselines | [Notebook 02](notebooks/02_analise_exploratoria.ipynb) | Validado |
| 05 | Qualidade e comportamentos atípicos | Duplicatas, conflito, tipos, extremos, ausentes e formato | [Partições](data/splits/manifest.json) · [Qualidade](results/exploracao/qualidade.json) | Validado |
| 06 | Preparação justificada | Mediana, one-hot limitado e escala na logística, ajustados por fold | [Pipeline](src/phishield/preprocessing.py) · [Auditoria](docs/auditoria_atributos.md) | Validado |
| 07 | Quatro modelos obrigatórios | Cinco modelos efetivos e Dummy | [Comparação](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/comparacao.csv) | Validado |
| 08 | Validação cruzada | Cinco folds agrupados sem sobreposição, com rastreabilidade dos índices da busca e da comparação aleatória | [Auditoria dos folds](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/folds.json) · [Reconstrução histórica](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/reconstrucao_folds.json) | Validado |
| 09 | Métricas adequadas | F1 phishing primário e métricas complementares | [Métricas por fold](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/metricas_agregadas.csv) · [Teste](results/final/39293c0cc63702da8f5475cb060b878905ac68284c06479919d0f138e8157b8f/metrics.json) | Validado |
| 10 | Teste reservado para avaliação única | Artefatos congelados e marcador exclusivo por hash | [Congelamento](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/freeze.json) · [Execução](results/final/39293c0cc63702da8f5475cb060b878905ac68284c06479919d0f138e8157b8f/execucao.json) | Validado |
| 11 | Otimização de pelo menos dois modelos | Quatro buscas em cinco folds internos e comparação independente da busca | [Notebook 05](notebooks/05_otimizacao_hiperparametros.ipynb) | Validado |
| 12 | README, relatório, notebooks e diário | Documentos e oito notebooks executados | [README](README.md) · [Relatório](RELATORIO.md) · [Notebook final](notebooks/08_avaliacao_final.ipynb) · [Diário](DIARIO.md) | Validado |
| 13 | Diário de cada sessão | Atividades, tentativas e dificuldades de cada sessão | [Diário](DIARIO.md) | Validado |
| 14 | Preparar apresentação de dez minutos | Roteiro e perguntas com resultados reais | [Apresentação](APRESENTACAO.md) | Validado |

## Diferenciais e limites

| Entrega | Evidência | Situação |
|---|---|---|
| Comparação de cenários e estratégias de generalização | [Comparação](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/comparacao.png) · [Análise de coleta](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/sensibilidade_coleta.json) | Validado |
| Explicabilidade global, local e análise de erros | [Notebook 07](notebooks/07_explicabilidade.ipynb) | Validado |
| Limiar de decisão e curva de aprendizado | [Curvas B](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/curvas_B.png) · [Curvas C](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/curvas_C.png) | Validado |
| Eficiência computacional | [Ficha dos modelos](docs/ficha_modelo.md) · [Relatório](RELATORIO.md) | Validado |
| Protótipo Streamlit com inferência exclusivamente lexical | [Aplicação](app/streamlit_app.py) · [Testes](tests/test_prediction.py) | Validado |
| Avaliação externa e temporal | [Limitações](RELATORIO.md) | Pendente como trabalho futuro |

A apresentação foi preparada. O ensaio e a atribuição de falas dependem dos integrantes do grupo. SHAP e pico de memória por modelo ficaram fora do orçamento experimental; permutação, coeficientes, perturbações locais, tempos e tamanho dos artefatos estão registrados.
