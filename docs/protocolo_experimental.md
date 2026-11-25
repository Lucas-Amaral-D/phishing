# Protocolo experimental inicial

A unidade de classificação é o registro de URL e página associada. A classe positiva interna é phishing. O alvo original será preservado nos dados brutos.

As configurações iniciais são [semente 42, teste de 20% e validação cruzada com cinco folds](../configs/experiment_config.json). Após auditoria estrutural de duplicatas e conflitos, a próxima etapa reservará o teste. A exploração detalhada e as decisões sobre atributos serão feitas com os dados de desenvolvimento.

A comparação principal investigará a separação por domínio, com verificação da ausência de sobreposição entre partições. A comparação com uma separação estratificada por registro será investigada no desenvolvimento. Imputação, codificação e escalonamento serão ajustados dentro dos folds.

A comparação inclui DummyClassifier, regressão logística, árvore de decisão, Random Forest, HistGradientBoosting e GaussianNB. O F1 da classe phishing orienta a comparação e a otimização, acompanhado de average precision, recall, precisão, ROC-AUC e matriz de confusão. A busca usa cinco folds internos agrupados e duas combinações por família. O primeiro fold externo fica reservado para comparação antes e depois da busca e escolha do limiar. Essa escolha é descritiva no desenvolvimento e a estimativa final vem da partição de teste independente.

Selecione o modelo e o limiar com evidências de desenvolvimento. Congele pipeline, atributos e limiar antes da avaliação única no teste reservado. Registre configurações, versões, hashes, métricas e tempos por execução.
