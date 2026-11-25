# Decisões prévias à modelagem

F1 da classe phishing é o critério primário de validação e otimização por equilibrar precisão e recall. Average precision é complementar. Compare candidatos com a mesma validação agrupada. Separe uma validação interna agrupada para comparar modelos antes e depois da otimização. As médias de busca identificam candidatos e carregam viés de seleção.

Considere elegíveis os cenários B e C. Se o F1 de candidatos elegíveis diferir em até 0,002 na validação interna, priorize recall, menor desvio-padrão externo da família e menor tempo de inferência, nessa ordem. Selecione limiares nas predições do fold de validação interna. Na escolha entre cenários, use a mesma tolerância, priorize recall e estabilidade e, persistindo o empate, prefira o modelo lexical. A avaliação final inclui o modelo acadêmico principal e, se este usar sinais de página, um modelo lexical operacional pré-especificado na mesma execução.
