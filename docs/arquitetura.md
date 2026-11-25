# Arquitetura

O CSV em data/raw é a fonte imutável. A reserva persiste identificadores de linha agrupados; scripts de desenvolvimento carregam exclusivamente o índice dev. O extrator lexical e a PSL local servem tanto para preparação quanto para inferência.

O pipeline ajusta as transformações dentro dos folds. Os experimentos persistem configurações, predições resumidas, evidências de validação e hashes. Os modelos serializados e o manifesto congelado antecedem a abertura da reserva final. O script de avaliação gera resultados e estados de execução para cada partição. A aplicação lê métricas persistidas e carrega o artefato lexical.

Os notebooks apresentam as etapas e consomem os mesmos artefatos dos scripts. Essa separação permite reexecutar as análises sem reabrir o teste.
