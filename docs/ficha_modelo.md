# Ficha dos modelos congelados

Avaliação de 25/11/2026. Execução `completo-e00004fe47f74cb1994965d5c8d0d5b4`. Fonte PhiUSIIL UCI 967. Rótulo positivo interno igual a 1 para phishing.

| Campo | Modelo principal B | Modelo lexical C |
|---|---|---|
| Finalidade | Avaliação acadêmica com sinais controlados de página e URL | Demonstração em Streamlit usando a estrutura textual da URL |
| Algoritmo | HistGradientBoosting otimizado | HistGradientBoosting basal |
| Atributos | 44 numéricos do CSV após auditoria | 14 descritores numéricos e sufixo categórico recalculados |
| Parâmetros principais | 90 iterações, taxa 0,12, 31 folhas, mínimo 20 por folha | 90 iterações, taxa 0,10, 31 folhas, mínimo 20 por folha |
| Limiar | 0,175 | 0,50 |
| F1 no teste agrupado | 0,99982 | 0,99645 |
| SHA-256 | `e516d37e01379fbb2c4c95c386514328938ea7d27818b07751621e6f36f3f892` | `7edf9f6e76da657ffb1ed11fecd2cae7b54cfa3b8a3eba85c3af0068c51ee9f1` |
| Arquivo | `completo-e00004fe47f74cb1994965d5c8d0d5b4-B.joblib` | `completo-e00004fe47f74cb1994965d5c8d0d5b4-C.joblib` |

Treino final com 187.434 registros após seleção em desenvolvimento agrupado. Teste pré-reservado com 46.760 registros e domínios disjuntos. A lista de atributos e os parâmetros completos estão no [manifesto de congelamento](../results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/freeze.json). [Métricas finais](../results/final/39293c0cc63702da8f5475cb060b878905ac68284c06479919d0f138e8157b8f/metrics.json)

O escore indica a saída do modelo. A avaliação se restringe à mesma coleta e é sensível ao formato das classes. O modelo B precisa de sinais de página fornecidos pela fonte oficial. O modelo C opera localmente no texto do endereço e o recall no subconjunto interno de formato comum foi 58,18%. Recomenda-se uso acadêmico e demonstração assistida. Bloqueio automático de sites e decisões de segurança em produção exigem validação externa.
