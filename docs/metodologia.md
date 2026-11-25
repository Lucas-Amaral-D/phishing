# Metodologia

## Dados e unidade de análise

Cada linha representa uma URL e indicadores de uma página. A pergunta trata da generalização a registros ausentes do treinamento. A separação por domínio registrável mede um aspecto mais exigente da generalização dentro da coleta. Conflitos e URLs repetidas são tratados antes da reserva. Estatísticas exploratórias e escolhas de atributos usam desenvolvimento.

## Modelos

- Dummy por prevalência dá uma referência para o ganho sobre o acaso operacional. Com maioria legítima, o limiar de 0,5 produz apenas negativos.
- A regressão logística ajusta uma fronteira linear regularizada. A padronização facilita o ajuste, e coeficientes são expressos na escala do pipeline.
- A árvore aprende partições não lineares. Profundidade e tamanho mínimo de folha limitam sobreajuste.
- A floresta combina árvores ajustadas em amostras bootstrap. O orçamento de 24 árvores prioriza reprodutibilidade em CPU e a busca investiga capacidade e regularização.
- O boosting de histogramas combina árvores sequencialmente. A busca explora taxa, folhas, amostra mínima e regularização.
- GaussianNB estima densidades gaussianas por classe e usa independência condicional. A hipótese é difícil para contagens e razões redundantes, mas fornece uma referência com perfil computacional diferente.

## Métricas

F1 equilibra precisão e recall. F2 dá mais peso ao recall, útil para entender ameaças perdidas. Especificidade e taxa de falsos positivos medem o custo para sites legítimos. Balanced accuracy e MCC complementam a avaliação. ROC-AUC mede ordenação e average precision resume precisão por mudanças de recall. A área trapezoidal precisão-recall é registrada à parte.

## Explicabilidade e eficiência

A importância por permutação usa 4.000 registros de validação com três repetições e semente 42. Os coeficientes e perturbações locais são descritivos. A substituição pela moda pode gerar vetores pouco comuns, então a diferença observada é sensibilidade sob a intervenção aplicada. O custo é medido em tempo e bytes serializados. O pico de memória por modelo e SHAP ficam fora do orçamento experimental desta execução.
