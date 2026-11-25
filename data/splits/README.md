# Partições reservadas

Os índices são posições de linha com base zero no CSV oficial, excluído o cabeçalho. Consulte manifest.json para os hashes. A sobreposição de domínios registráveis entre desenvolvimento e teste é zero. URLs com a mesma grafia após remoção de barras finais são tratadas como repetidas; conflitos de rótulo são excluídos por completo e duplicatas de mesmo rótulo mantêm a primeira linha. URLs incompatíveis com o esquema lexical comum também são excluídas.

A Public Suffix List distribuída com tldextract inclui sufixos privados. IPs usam a forma canônica e hosts sem sufixo reconhecido ficam agrupados pelo host completo.
