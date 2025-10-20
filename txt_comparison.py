import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import json

from helper_funcs import read_txt_file_to_string, get_api_key_url

API_KEY, API_URL = get_api_key_url()

# --- Streamlit UI ---
st.set_page_config(page_title="DORA Compliance Vergelijker", layout="wide")
st.title("⚖️ DORA / ISO27001 Documentvergelijker")

# Sidebar for LLM settings
st.sidebar.header("🔧 LLM-instellingen")
model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"])
temperature = st.sidebar.slider("Temperatuur", 0.0, 1.0, 0.2)

# Sidebar criteria
criteria = st.sidebar.text_area(
    "Vergelijkingscriteria (één per regel)",
    "Governance structuur\n" \
    "Risicomanagement\n" \
    "Incident response\n" \
    "Outsourcing beleid"
)

# File uploaders
st.subheader("📂 Upload documenten")
col1, col2 = st.columns(2)
with col1:
    filepath1 = st.file_uploader("Upload Document A (.txt)", type="txt")
with col2:
    filepath2 = st.file_uploader("Upload Document B (.txt)", type="txt")

# Prompt editor
st.subheader("🧠 Prompt template")
default_prompt = """Je bent een compliance-expert gespecialiseerd in DORA, ISO27001 en vergelijkbare standaarden.
Vergelijk de twee onderstaande documenten per criterium.
Geef per criterium:
- een samenvatting van hoe elk document het onderwerp behandelt
- een beoordeling van de mate van overeenstemming (bijv. "Volledig in lijn", "Gedeeltelijk", "Niet in lijn")
- een korte toelichting
- citeer indien mogelijk relevante fragmenten uit beide documenten met het pagina nummer erbij

Document A:
\"\"\"{doc1}\"\"\"

Document B:
\"\"\"{doc2}\"\"\"

Criteria:
{criteria}

Antwoord in geldig JSON-formaat als volgt:
[
    {{
    "criterium": "...",
    "overeenstemming": "...",
    "analyse_document_A": "...",
    "analyse_document_B": "...",
    "toelichting": "...",
    "referentie_A": "...",
    "referentie_B": "..."
    }},
    ...
]
"""
prompt_text = st.text_area("Prompt-template", value=default_prompt, height=400)

# Run button
if st.button("🚀 Vergelijk documenten"):
    if not (API_KEY and filepath1 and filepath2):
        st.error("Vul een API key in en upload beide documenten.")
    else:
        with st.spinner("AI vergelijkt de documenten... ⏳"):
            # Prepare LLM
            llm = ChatOpenAI(model=model_name, temperature=temperature, api_key=API_KEY)
            embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=API_KEY)

            # Read documents
            doc1 = read_txt_file_to_string(filepath1)
            doc2 = read_txt_file_to_string(filepath2)

            # Prompt chain
            prompt_template = ChatPromptTemplate.from_template(prompt_text)
            chain = prompt_template | llm | StrOutputParser()

            # Run model
            output = chain.invoke({
                "doc1": doc1,
                "doc2": doc2,
                "criteria": criteria
            })

            # Display output
            st.success("✅ Vergelijking voltooid!")
            try:
                json_output = json.loads(output)
                st.json(json_output)
            except json.JSONDecodeError:
                st.text_area("Ruwe AI-output", output, height=400)

            # Download option
            st.download_button(
                label="💾 Download resultaat als JSON",
                data=output.encode("utf-8"),
                file_name="dora_compliance_result.json",
                mime="application/json"
            )

# Footer
st.markdown("---")
st.caption("💡 Gemaakt met LangChain + Streamlit — GPT-5 Compliance Analyzer Prototype")
