# Auditoria de atributos

| Atributo | Origem e disponibilidade | Decisão |
|---|---|---|
| FILENAME | Identificador do acervo. Pode memorizar a coleta e está ausente em produção | Excluir |
| URL e Domain | Strings disponíveis na entrada. Podem memorizar endereços; o domínio registrável serve para agrupamento | Excluir valores brutos, recalcular descritores no cenário C |
| Title | Texto de página, com alta cardinalidade e potencial de memorização | Excluir texto bruto |
| TLD | Sufixo categórico público. Pode refletir viés de coleta. Independente dos rótulos, extraível pela PSL | Diagnóstico em A e extração própria em C |
| URLSimilarityIndex | Similaridade do método dos autores, com possíveis referências externas ao fold | Diagnóstico A |
| CharContinuationRate | Derivado documentado; paridade exata com cálculo local incerta | Diagnóstico A |
| URLCharProb | Probabilidade derivada. População e isolamento fold a fold não verificados | Diagnóstico A |
| TLDLegitimateProb | Estimativa de legitimidade por TLD, dependente de referências de legitimidade; isolamento não verificado | Diagnóstico A |
| URLTitleMatchScore e DomainTitleMatchScore | Escores derivados da URL e título. Definições exatas e independência das referências não reproduzidas | Diagnóstico A |
| Demais contagens, razões e marcadores de página | Sinais observáveis no endereço ou no HTML; a disponibilidade dos sinais de página depende de coleta externa | B experimental |

A inclui indicadores suspeitos para medir sensibilidade. B exclui esses indicadores e categorias de alta cardinalidade. C recalcula todos os sinais a partir da URL, com o mesmo extrator na aplicação. Uma associação forte com o alvo requer investigação da origem do atributo. O modelo final exclui A.

A alimentação original foi mantida. Mediana defensiva e categoria explícita para vazio são ajustadas por fold. O one-hot tem teto de 16 categorias, viabilizando representação densa para HistGradientBoosting e GaussianNB. StandardScaler é usado na regressão logística. O experimento mantém extremos e proporções observadas sem reamostragem de classe.

Fontes: catálogo UCI 967 e artigo dos autores no DOI 10.1016/j.cose.2023.103545.
