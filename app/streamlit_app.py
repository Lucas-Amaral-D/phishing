"""Interface local de demonstração do PHISHIELD."""
import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from phishield.prediction import classify, load_operational  # noqa: E402

RESULTS = ROOT / "results"
REFERENCE = RESULTS / "experiments" / "completo-e00004fe47f74cb1994965d5c8d0d5b4"
FINAL = RESULTS / "final" / "39293c0cc63702da8f5475cb060b878905ac68284c06479919d0f138e8157b8f"
REMARK = (
    "O PHISHIELD é um protótipo acadêmico de apoio à identificação de phishing. "
    "Seus resultados podem conter erros e não substituem ferramentas especializadas "
    "de segurança da informação."
)


@st.cache_resource(show_spinner=False)
def model_for(manifest, mtime):
    return load_operational(manifest)


st.set_page_config(page_title="PHISHIELD", page_icon="🛡️", layout="wide")
st.title("PHISHIELD")
st.write("Triagem acadêmica de endereços web por sinais lexicais.")
analysis, overview, performance, data, method = st.tabs([
    "Análise de URL", "Visão geral", "Desempenho", "Sobre os dados", "Metodologia",
])

with analysis:
    st.header("Analisar um endereço")
    st.caption("A análise acontece localmente. Nenhuma página é visitada.")
    candidates = sorted(
        (RESULTS / "experiments").glob("completo-*/freeze.json"),
        key=lambda path: path.stat().st_mtime_ns,
        reverse=True,
    )
    manifest = candidates[0] if candidates else None
    with st.form("url_analysis", clear_on_submit=True):
        url = st.text_input("Endereço HTTP ou HTTPS", placeholder="https://example.org",
                            max_chars=16384)
        submitted = st.form_submit_button("Analisar URL", type="primary")
    if manifest is None or not (ROOT / "models" / f"{manifest.parent.name}-C.joblib").is_file():
        st.info("Modelo indisponível. Execute a etapa de treinamento para gerar um artefato.")
    elif submitted:
        try:
            estimator, spec = model_for(manifest, manifest.stat().st_mtime_ns)
            result = classify(url, estimator, spec["threshold"])
        except FileNotFoundError:
            st.warning("O arquivo do modelo está ausente. Gere o artefato com o treino completo.")
        except (ValueError, UnicodeError) as error:
            st.error(str(error))
        else:
            if result["phishing"]:
                st.warning("Classificado como provável phishing")
            else:
                st.info("Classificado como provável legítimo")
            columns = st.columns(2)
            columns[0].metric("Pontuação do modelo", f"{result['score']:.3f}")
            columns[1].metric("Limiar de classificação", f"{spec['threshold']:.3f}")
            st.caption("A pontuação é uma saída do modelo sem calibração de probabilidade.")
            st.caption(f"Execução local {manifest.parent.name}")
            with st.expander("Características observadas"):
                values = result["features"]
                st.write(
                    f"Comprimento de {values['comprimento']} caracteres, "
                    f"{values['subdominios']} subdomínio(s) e {values['parametros']} parâmetro(s)."
                )
                st.caption("Esses indicadores descrevem a entrada. A validação por permutação "
                           "resume a dependência global do modelo.")
    st.info(REMARK)

with overview:
    st.header("Uma triagem baseada no texto da URL")
    st.write("O protótipo extrai sinais da estrutura do endereço e usa um modelo treinado "
             "no conjunto PhiUSIIL. A separação por domínio mede desempenho em domínios "
             "inéditos da mesma coleta.")
    st.write("O padrão de formatação da coleta favorece a classificação lexical. "
             "Use o resultado como apoio em uma demonstração acadêmica.")

with performance:
    st.header("Resultados da execução acadêmica")
    path = FINAL / "metrics.json"
    if path.is_file():
        figures = json.loads(path.read_text(encoding="utf-8"))
        selected = st.selectbox("Cenário", list(figures),
                                format_func=lambda key: "B — Página e URL" if key == "B" else
                                "C — Apenas URL")
        result = figures[selected]
        columns = st.columns(3)
        for col, name, label in zip(columns, ["f1", "precision", "recall"],
                                    ["F1 de phishing", "Precisão", "Recall"], strict=True):
            col.metric(label, f"{result[name]:.2%}")
        st.image(str(FINAL / f"avaliacao_{selected}.png"), width="stretch")
        st.caption("Teste agrupado com domínios inéditos dentro da mesma coleta.")
    else:
        st.info("Os indicadores finais aparecerão quando a avaliação acadêmica estiver disponível.")
    comparison = REFERENCE / "comparacao.csv"
    if comparison.is_file():
        st.subheader("Validação cruzada")
        st.dataframe(pd.read_csv(comparison).rename(columns={
            "scenario": "Cenário", "model": "Modelo", "mean_f1": "F1 médio", "sd_f1": "Desvio",
        }), hide_index=True, width="stretch")

with data:
    st.header("PhiUSIIL")
    columns = st.columns(3)
    columns[0].metric("Registros originais", "235.795")
    columns[1].metric("Phishing no original", "100.945")
    columns[2].metric("Legítimos no original", "134.850")
    st.markdown("[UCI Machine Learning Repository]"
                "(https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset)")
    st.write("A coleta apresenta diferenças de representação entre as classes. Essa diferença "
             "pode favorecer o resultado dentro do PhiUSIIL.")

with method:
    st.header("Como os modelos foram avaliados")
    st.write("A reserva e os folds agrupam domínios pela Public Suffix List. A seleção e os "
             "limiares foram definidos no desenvolvimento antes da avaliação final.")
    st.write("A aplicação usa exclusivamente sinais textuais calculados pelo mesmo extrator "
             "usado no treino do modelo lexical.")
    attribution = REFERENCE / "importancia_C.csv"
    if attribution.is_file():
        st.subheader("Importância por permutação no desenvolvimento")
        importance = pd.read_csv(attribution).head(8)
        st.bar_chart(importance.set_index("atributo")["media_f1"])
