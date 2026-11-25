# Modelos

Os arquivos Joblib são gerados localmente por scripts/run_experiments.py e ignorados pelo Git. Cada freeze.json descreve o algoritmo, os atributos, o limiar, o nome e a integridade de cada arquivo. A aplicação verifica o hash e usa o modelo lexical. Carregue somente artefatos produzidos por uma execução confiável do próprio projeto.
