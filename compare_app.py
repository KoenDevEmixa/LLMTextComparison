import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from dotenv import load_dotenv
import json
import os

# --- API-key laden ---
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ Geen OpenAI API key gevonden. Voeg deze toe aan je .env-bestand.")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(page_title="Compliance Document Comparator", page_icon="📄")
st.title("📄 Compliance Vergelijkingstool")
st.write("Vergelijk twee compliance- of beleidsdocumenten op specifieke criteria (bijv. DORA, ISO, SOC2).")

# --- Invoer: documenten ---
col1, col2 = st.columns(2)
with col1:
    doc1 = st.text_area("📘 Document A", height=250, placeholder="Plak hier het eerste document...")
with col2:
    doc2 = st.text_area("📙 Document B", height=250, placeholder="Plak hier het tweede document...")

criteria_input = st.text_area(
    "📋 Vergelijkingscriteria (één per regel)",
    "Governance structuur\nRisicomanagement\nIncident response\nOutsourcing beleid"
)

# --- Knop ---
if st.button("Vergelijken"):
    if not doc1.strip() or not doc2.strip():
        st.warning("⚠️ Vul beide documenten in voordat je vergelijkt.")
        st.stop()

    criteria = [c.strip() for c in criteria_input.split("\n") if c.strip()]

    # --- LangChain setup ---
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    prompt_template = ChatPromptTemplate.from_template("""
    Je bent een compliance-expert gespecialiseerd in DORA, ISO27001 en vergelijkbare standaarden.
    Vergelijk de twee onderstaande documenten per criterium.
    Geef per criterium:
    - een samenvatting van hoe elk document het onderwerp behandelt
    - een beoordeling van de mate van overeenstemming (bijv. "Volledig in lijn", "Gedeeltelijk", "Niet in lijn")
    - een korte toelichting
    - citeer indien mogelijk relevante fragmenten uit beide documenten.

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
    """)

    chain = prompt_template | llm | StrOutputParser()

    with st.spinner("🔍 Vergelijkt documenten..."):
        output = chain.invoke({
            "doc1": doc1,
            "doc2": doc2,
            "criteria": json.dumps(criteria, ensure_ascii=False)
        })

    # --- JSON parsen ---
    try:
        vergelijking = json.loads(output)
    except json.JSONDecodeError:
        vergelijking = json.loads(output[output.find('['):output.rfind(']')+1])

    # --- Resultaten tonen ---
    st.subheader("📊 Vergelijkingsresultaten")
    for item in vergelijking:
        with st.expander(f"{item['criterium']} — {item['overeenstemming']}"):
            st.markdown(f"**Document A:** {item['analyse_document_A']}")
            st.markdown(f"**Document B:** {item['analyse_document_B']}")
            st.markdown(f"**Toelichting:** {item['toelichting']}")
            if item.get("referentie_A") or item.get("referentie_B"):
                st.markdown("> **Referentie A:** " + item.get("referentie_A", "—"))
                st.markdown("> **Referentie B:** " + item.get("referentie_B", "—"))

    st.success("✅ Vergelijking voltooid!")
