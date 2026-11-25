# Dicionário do PhiUSIIL

A grafia e o tipo observado seguem o CSV. C recalcula descritores próprios e compartilha a implementação com a aplicação. A disponibilidade abaixo descreve o conceito, enquanto o extrator C estabelece as definições usadas em produção.

| Coluna | Tipo | Significado | Origem | Disponibilidade | Risco auditado | Tratamento e decisão |
|---|---|---|---|---|---|---|
| `FILENAME` | texto | Identificador de arquivo da coleta | Coleta | Indisponível | Memorização | Excluído como entrada bruta |
| `URL` | texto | Endereço original | URL catalogada | Disponível na origem | Memorização | Excluído como entrada bruta |
| `URLLength` | inteiro | Comprimento do endereço | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `Domain` | texto | Host registrado na coleta | URL catalogada | Disponível na origem | Memorização | Excluído como entrada bruta |
| `DomainLength` | inteiro | Comprimento do host | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `IsDomainIP` | inteiro | Indicador de host expresso como endereço IP | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `TLD` | texto | Sufixo do endereço segundo a coleta | URL catalogada | Extraível localmente | Viés de coleta | A com one-hot, C recalculado |
| `URLSimilarityIndex` | real | Índice de similaridade do método dos autores | Derivado dos autores | Reprodução independente incerta | Referência ou semântica incerta | A diagnóstico |
| `CharContinuationRate` | real | Medida de continuidade de caracteres | Derivado dos autores | Reprodução independente incerta | Referência ou semântica incerta | A diagnóstico |
| `TLDLegitimateProb` | real | Escore de legitimidade associado ao sufixo | Derivado dos autores | Reprodução independente incerta | Referência ou semântica incerta | A diagnóstico |
| `URLCharProb` | real | Escore de probabilidade dos caracteres | Derivado dos autores | Reprodução independente incerta | Referência ou semântica incerta | A diagnóstico |
| `TLDLength` | inteiro | Comprimento do sufixo | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfSubDomain` | inteiro | Contagem de subdomínios | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `HasObfuscation` | inteiro | Indicador de ofuscação | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfObfuscatedChar` | inteiro | Contagem de caracteres ofuscados | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `ObfuscationRatio` | real | Proporção de caracteres ofuscados | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfLettersInURL` | inteiro | Contagem de letras no endereço | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `LetterRatioInURL` | real | Proporção de letras | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfDegitsInURL` | inteiro | Contagem de dígitos no endereço | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `DegitRatioInURL` | real | Proporção de dígitos | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfEqualsInURL` | inteiro | Contagem de sinais de igualdade | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfQMarkInURL` | inteiro | Contagem de interrogações | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfAmpersandInURL` | inteiro | Contagem de sinais & | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `NoOfOtherSpecialCharsInURL` | inteiro | Contagem de outros caracteres especiais | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `SpacialCharRatioInURL` | real | Proporção de caracteres especiais | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `IsHTTPS` | inteiro | Indicador de protocolo HTTPS | URL catalogada | Conceito disponível pela URL | Definição do catálogo | A e B, mediana defensiva |
| `LineOfCode` | inteiro | Contagem de linhas no código da página | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `LargestLineLength` | inteiro | Comprimento da maior linha | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasTitle` | inteiro | Indicador de presença de título | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `Title` | texto | Título da página | Página | Disponível na origem | Memorização | Excluído como entrada bruta |
| `DomainTitleMatchScore` | real | Escore de correspondência entre domínio e título | Derivado dos autores | Reprodução independente incerta | Referência ou semântica incerta | A diagnóstico |
| `URLTitleMatchScore` | real | Escore de correspondência entre URL e título | Derivado dos autores | Reprodução independente incerta | Referência ou semântica incerta | A diagnóstico |
| `HasFavicon` | inteiro | Indicador de favicon | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `Robots` | inteiro | Indicador de diretivas para robôs | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `IsResponsive` | inteiro | Indicador de responsividade | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfURLRedirect` | inteiro | Contagem de redirecionamentos | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfSelfRedirect` | inteiro | Contagem de redirecionamentos próprios | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasDescription` | inteiro | Indicador de descrição da página | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfPopup` | inteiro | Contagem de pop-ups | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfiFrame` | inteiro | Contagem de iframes | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasExternalFormSubmit` | inteiro | Indicador de formulário que envia para destino externo | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasSocialNet` | inteiro | Indicador de presença de rede social | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasSubmitButton` | inteiro | Indicador de botão de envio | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasHiddenFields` | inteiro | Indicador de campos ocultos | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasPasswordField` | inteiro | Indicador de campo para senha | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `Bank` | inteiro | Indicador de sinal relacionado a banco | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `Pay` | inteiro | Indicador de sinal relacionado a pagamento | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `Crypto` | inteiro | Indicador de sinal relacionado a criptoativos | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `HasCopyrightInfo` | inteiro | Indicador de informação de direitos autorais | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfImage` | inteiro | Contagem de imagens | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfCSS` | inteiro | Contagem de referências CSS | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfJS` | inteiro | Contagem de referências JavaScript | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfSelfRef` | inteiro | Contagem de referências próprias | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfEmptyRef` | inteiro | Contagem de referências vazias | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `NoOfExternalRef` | inteiro | Contagem de referências externas | Página ou coleta | Com coleta externa | Viés de coleta | A e B, mediana defensiva |
| `label` | inteiro | 0 phishing e 1 legítimo no original | Anotação | Indisponível | Alvo direto | Inversão explícita para treino |

O catálogo e a publicação dos autores complementam as descrições. [Catálogo UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset) · [Publicação](https://doi.org/10.1016/j.cose.2023.103545)
