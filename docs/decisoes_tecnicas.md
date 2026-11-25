# Decisões técnicas

| Decisão | Justificativa | Evidência |
|---|---|---|
| Validar as duas fontes em separado | Kaggle v2 diverge da base oficial | [Auditoria](../results/data_audit/eedb92afaef04c27b08941e64df07dfc.json) |
| Reservar por domínio registrável | 43.516 registros elegíveis compartilham grupo com outra linha | [Manifesto](../data/splits/manifest.json) |
| Excluir conflitos sem imputar o rótulo | Uma entrada com rótulos concorrentes não determina uma classe confiável | [Regra da reserva](../data/splits/README.md) |
| Separar diagnóstico de seleção | A inclui escores com proveniência ou paridade pendente. A seleção aceita B e C | [Auditoria](auditoria_atributos.md) |
| Manter orçamento limitado por modelo | Cinco folds e dados completos têm prioridade sobre ampliar grades | [Protocolo](protocolo_experimental.md) |
| Medir o viés de representação | A representação dos legítimos é homogênea no desenvolvimento. O subconjunto de formato comum quantifica a sensibilidade | [Auditoria de formato](../results/exploracao/formato_coleta.json) |
| Expor pontuação sem calibração no protótipo | A calibração fora da coleta permanece uma questão aberta | [Metodologia](metodologia.md) |

A decisão mais difícil foi manter a avaliação por domínio como resposta à pergunta acadêmica e explicitar que ela preserva o viés da coleta. A análise do subconjunto em formato comum quantifica parte da diferença sem consumir a partição final.
