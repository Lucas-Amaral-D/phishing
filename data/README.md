# Dados

`data/raw/` guarda o ZIP público da UCI, o CSV original contido nele e o cache separado da Kaggle. Os arquivos brutos são ignorados pelo Git. O script verifica os hashes antes de aceitar os arquivos e usa links físicos para publicar cópias completas sem substituir arquivos existentes. O diretório bruto deve estar em um sistema de arquivos com suporte a links físicos.

| Fonte | Edição consultada | Papel |
|---|---|---|
| [Kaggle](https://www.kaggle.com/datasets/akashkr/phishing-website-dataset) | v2 | Auditoria de origem |
| [UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset) | ID 967, publicação de 03/03/2024 | Base do projeto |
| [Mendeley Data](https://data.mendeley.com/datasets/shwpxscxy2/2) | v2, DOI 10.17632/shwpxscxy2.2 | Referência complementar |

O catálogo UCI identifica a base sob CC BY 4.0. A revisão do ZIP e do CSV é identificada pelos hashes registrados em [auditoria](../results/data_audit/eedb92afaef04c27b08941e64df07dfc.json). As datas `*_mtime_utc` correspondem ao horário de modificação local e `checked_at_utc` registra o início da auditoria. Nesta sessão, as duas fontes foram obtidas em 25/11/2026.

O CSV contém URLs associadas a phishing. Trate as strings como dados inertes e evite abrir os endereços ou incluir os valores brutos em materiais de apresentação.
