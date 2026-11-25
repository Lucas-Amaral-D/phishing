# PHISHIELD — Apresentação em dez minutos

Apresentação em 12/12/2026. Os responsáveis por cada bloco serão definidos após confirmação dos três integrantes.

| Tempo | Conteúdo | Evidência |
|---|---|---|
| 00:00–01:00 | Defina phishing e apresente a pergunta preditiva do projeto | [Introdução](RELATORIO.md) |
| 01:00–02:00 | Compare Kaggle e UCI. Explique os 235.795 registros e 54 preditores e mostre o painel de comprimento e sinais de página | [Painel](results/exploracao/painel.png) |
| 02:00–03:30 | Explique a exclusão de conflitos, a reserva por domínio, os cinco folds e os cenários A, B e C | [Protocolo](docs/protocolo_experimental.md) |
| 03:30–05:00 | Decisão mais difícil. Domínios inéditos preservam o viés de formato. Mostre a queda do F1 lexical de 0,99622 para 0,71910 quando as duas classes compartilham o formato | [Sensibilidade](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/sensibilidade_coleta.json) |
| 05:00–07:00 | Mostre comparação, otimização e teste único. B obteve F1 0,99982 e perdeu 4 casos. C obteve F1 0,99645 e perdeu 127 | [Comparação](results/experiments/completo-e00004fe47f74cb1994965d5c8d0d5b4/comparacao.png) · [Teste](results/final/39293c0cc63702da8f5475cb060b878905ac68284c06479919d0f138e8157b8f/avaliacao_B.png) |
| 07:00–09:00 | Demonstre a análise com `https://example.org` e uma entrada inválida. No ensaio técnico, o endereço reservado para documentação recebeu pontuação 0,999 e alerta; use-o para ilustrar a limitação | [Protótipo](app/streamlit_app.py) |
| 09:00–10:00 | Responda que houve generalização a domínios inéditos desta coleta. Explique a necessidade de comparação externa e temporal | [Conclusão](RELATORIO.md) |

## Perguntas prováveis

**Por que reservar domínios?** A validação aleatória compartilhou de 2.512 a 2.543 grupos por fold. Com agrupamento, a sobreposição foi zero.

**Por que excluir os atributos derivados?** A origem ou disponibilidade de alguns escores durante a inferência exige evidência adicional. Eles ficam restritos ao diagnóstico A. A exclusão deixou F1 de 0,99966 no boosting B na validação agrupada.

**O resultado se aplica a qualquer URL?** O teste mede domínios inéditos dentro do PhiUSIIL. O F1 lexical no subconjunto interno de formato comum foi 0,71910, ilustrando sensibilidade à coleta.

**Por que dois modelos no teste?** O modelo B responde à comparação acadêmica com sinais de página. O C permite inferência local. Ambos foram definidos antes da abertura da reserva na mesma sessão.

**Por que F1 e não só acurácia?** F1 combina precisão e recall de phishing. A matriz de confusão revela diretamente os falsos alertas e ameaças perdidas.
