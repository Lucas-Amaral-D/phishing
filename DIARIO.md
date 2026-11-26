# Diário de desenvolvimento

## Sessão 01 — 25/11/2026

### Participantes

- Codex, na implementação e execução desta sessão. Participação dos integrantes do grupo a confirmar.

### Objetivo

Fundar o PHISHIELD e identificar, obter e validar o conjunto de dados oficial.

### Atividades executadas

Inspeção do diretório vazio, inicialização do Git em `main`, criação da `.venv` em Python 3.13.7, instalação das dependências, consulta ao catálogo UCI e auditoria dos CSVs. Implementação do download, registro de SHA-256, notebook, documentação e testes.

### Tentativas

Executados `git init -b main`, `python -m venv .venv`, `pip install` das ferramentas, download do ZIP da UCI via `curl.exe`, `kagglehub.dataset_download` e `python scripts/download_data.py`. Dependências transitivas registradas a partir de `pip freeze`.

### Problemas encontrados

O acesso inicial pelo terminal falhou tanto para a UCI quanto para o índice Python. A instalação apresentou WinError 10013. As novas tentativas com acesso de rede aprovado funcionaram.

### Tentativas que não funcionaram

O primeiro download do ZIP UCI e a primeira instalação das dependências sob as permissões padrão do terminal.

### Decisões tomadas e justificativas

Adotado o CSV publicado pela UCI para manter os identificadores e o esquema original. A base Kaggle v2 tem 11.055 linhas, alvo `Result` e cabeçalho incompatível. A validação em fluxo evita carregar o arquivo inteiro em memória. Os hashes observados da UCI identificam a cópia usada no estudo.

### Resultados e evidências

A [auditoria](results/data_audit/eedb92afaef04c27b08941e64df07dfc.json) confirmou 235.795 registros, 54 preditores e a distribuição oficial do alvo. `python -m pytest -q` aprovou 16 testes, `python -m ruff check .` aprovou a análise estática e `python -m pip check` confirmou a consistência do ambiente.

As funções de aquisição baixaram ambas as fontes novamente em um diretório temporário sem cache e reproduziram os totais de 11.055 e 235.795 registros. A célula de código do notebook foi executada diretamente com Python e sua saída foi preservada no arquivo.

### Pendências e próximos passos

Auditar duplicatas e conflitos e reservar o conjunto de teste antes da análise exploratória detalhada.

## Sessão 02 — 25/11/2026

### Participantes

- Codex, na implementação e execução. Participação dos integrantes do grupo a confirmar.

### Objetivo

Executar as etapas restantes em sequência, do particionamento ao roteiro de apresentação.

### Atividades executadas

1. Executados `scripts/prepare_data.py` e `scripts/explore_data.py`. A auditoria estrutural identificou repetições e conflitos, a reserva foi feita por domínio e a exploração detalhada leu somente o desenvolvimento.
2. Auditados os atributos, implementados três cenários e ajustados os pipelines dentro dos cinco folds agrupados. Registradas as decisões nos documentos de auditoria e seleção.
3. Executados `scripts/run_experiments.py --rapido` e `scripts/run_experiments.py`. Treinados cinco modelos e um Dummy; completadas quatro buscas e comparações de cenários, grupos, limiares e volumes de treino.
4. Executados `scripts/audit_collection.py`, `scripts/summarize_experiments.py` e `scripts/check_collection_bias.py`. Medidos efeitos do formato de coleta no desenvolvimento; registrados permutação, coeficientes, casos e erros.
5. Congelados os dois modelos definidos no protocolo. Executado `scripts/evaluate_final.py` uma vez, com guarda por hash. Lidos os resultados persistidos para a discussão.
6. Implementado o protótipo Streamlit. Executados testes Pytest, Ruff, verificação das dependências, inferência via AppTest com endereço reservado para documentação e teste de rejeição de protocolo inválido. Os oito notebooks foram executados com `scripts/execute_notebooks.py`.
7. Consolidados relatório, ficha dos modelos, matriz de rastreabilidade e roteiro de dez minutos.

### Tentativas, problemas encontrados e recuperação

- O primeiro preparo ocorreu antes da instalação terminar e retornou ausência de Pandas. A execução após a instalação gerou a reserva e a EDA.
- O fallback de Matplotlib criou cache temporário após o diretório padrão falhar. As execuções seguintes usaram cache gravável no ambiente virtual.
- O Joblib registrou fallback para processadores lógicos porque o utilitário WMIC estava ausente. O experimento prosseguiu com limite de quatro threads.
- A primeira execução via Jupyter falhou por falta de permissão de escrita no perfil IPython. A execução com diretórios temporários completou os oito notebooks.
- Uma consulta exploratória ao CSV por classe usou um nome de coluna que o índice exportado não tinha. A leitura do cabeçalho e dos dados exportados forneceu os valores corretos.
- Um comando de inventário via WMI foi bloqueado. Python identificou Windows 11 e 16 processadores lógicos.
- A primeira operação no índice Git foi bloqueada no sandbox. A nova tentativa viu um proprietário diferente para o repositório criado na sessão anterior. As operações locais aprovadas usaram uma exceção de propriedade restrita ao caminho e ao comando.
- A checagem do diff apontou finais de linha mistos nos arquivos novos. Os arquivos de texto envolvidos foram normalizados antes dos commits finais.

### Decisões tomadas e justificativas

A divisão grupal elimina compartilhamento de domínio, enquanto a auditoria de representação investiga um viés que essa divisão preserva. O estudo restringiu A a diagnóstico, escolheu B como modelo acadêmico e congelou C para a aplicação. O viés de formato explica parte da diferença entre a validação lexical geral e o subconjunto comparável. A demonstração usa apenas endereços reservados para documentação e a pontuação é apresentada sem calibração.

### Resultados e evidências

- [Partições](data/splits/manifest.json) com 187.434 linhas de desenvolvimento e 46.760 de teste.
- [Execução completa](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/metadata.json) e [diagnóstico de formato](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/sensibilidade_coleta.json) com F1 lexical de 0,71910 no subconjunto interno de formato comum.
- [Avaliação registrada](results/final/39293c0cc63702da8f5475cb060b878905ac68284c06479919d0f138e8157b8f/execucao.json) com F1 de 0,99982 no modelo principal e 0,99645 no lexical.
- [Notebook final](notebooks/08_avaliacao_final.ipynb) com métricas e gráficos de teste derivados dos artefatos persistidos.
- 38 testes Pytest aprovados. Ruff e `pip check` aprovados. O servidor Streamlit respondeu HTTP 200 localmente. O AppTest verificou as cinco seções, mostrou pontuação 0,999 para o endereço de demonstração e rejeitou protocolo inválido.
- Uma leitura independente das previsões persistidas confirmou as matrizes de confusão, os valores de F1 e os hashes das duas partições, sem repetir inferência no teste.

### Pendências e próximos passos

O roteiro está pronto para ensaio e divisão de falas entre os integrantes. Validação temporal, teste em outra coleta e calibração são extensões de pesquisa. A publicação no GitHub depende de autorização para publicação.

## Sessão 03 — 25/11/2026

### Participantes e objetivo

Codex realizou a revisão de lacunas do prompt e a implementação complementar.

### Atividades executadas

O README recebeu os itens de apresentação, objetivos, origem, tecnologias, arquitetura, metodologia, ordem dos notebooks, resultados e integrantes pendentes. O relatório passou a seguir a estrutura acadêmica do enunciado e incorporou o gráfico de domínios e a análise de correlações. Os notebooks 02 e 05 foram atualizados e executados.

A reserva passou a conferir hashes e a retomar gravações interrompidas. Novos experimentos guardam índices internos e aleatórios, hashes do código e das dependências e o inventário de arquivos. A reconstrução histórica usou apenas o desenvolvimento, conferiu os cinco folds externos com os arquivos originais e encontrou zero grupos compartilhados em todos os folds internos.

### Tentativas, dificuldades e decisões

O teste inicial de repetição da reserva encontrou uma diferença entre chaves inteiras na memória e chaves textuais no JSON. O retorno inicial foi alinhado à representação persistida. O modo rápido emitiu o aviso anterior de indisponibilidade do WMIC e completou a execução com o fallback em processadores lógicos.

### Resultados e evidências

- 40 testes Pytest aprovados e verificações Ruff e `pip check` aprovadas.
- [Execução técnica de verificação](results/experiments/rapido-0ce1874546e24a06987bc2a23759e8d3/metadata.json) completou treinamento rápido e gerou os novos registros.
- [Auditoria dos folds internos](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/reconstrucao_folds.json) e [gráfico dos domínios](results/exploracao/dominios.png) foram produzidos a partir do desenvolvimento. A avaliação única do teste permaneceu registrada nos artefatos da sessão anterior.

### Pendências

Identificação dos integrantes, distribuição de falas, publicação mediante autorização e extensões de pesquisa documentadas no relatório.
