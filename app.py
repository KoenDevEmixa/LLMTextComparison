import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from dotenv import load_dotenv
import json
import os

# --- Laad de API-key uit .env ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ Geen OpenAI API-key gevonden. Voeg deze toe aan je .env-bestand.")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(page_title="AI Nakijktool", page_icon="🧠")
st.title("🧠 AI Nakijktool")
st.write("Laat een tekst automatisch nakijken op vooraf ingestelde criteria met behulp van GPT.")

# --- Invoer: tekst en criteria ---
tekst = st.text_area(
    "✍️ Tekst om na te kijken",
    height=250,
    placeholder="Plak hier de tekst van de leerling of student..."
)

criteria_input = st.text_area(
    "📋 Beoordelingscriteria (één per regel)",
    "Structuur van de tekst\nSterkte van de argumentatie\nStijl en taalgebruik\nGebruik van voorbeelden"
)

# --- Knop ---
if st.button("Nakijken"):
    if not tekst.strip():
        st.warning("⚠️ Voer eerst een tekst in om na te kijken.")
        st.stop()

    # Zet criteria om naar lijst
    criteria = [c.strip() for c in criteria_input.split("\n") if c.strip()]

    # --- LangChain setup ---
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    prompt_template = ChatPromptTemplate.from_template("""
    Je bent een ervaren docent Nederlands. 
    Beoordeel de onderstaande tekst op elk van de gegeven criteria.
    Geef per criterium:
    - een score van 1 tot 10
    - een korte toelichting
    - citeer een relevante passage waarop je oordeel is gebaseerd.

    Tekst:
    \"\"\"{tekst}\"\"\"

    Criteria:
    {criteria}

    Antwoord in geldig JSON-formaat als volgt:
    [
      {{
        "criterium": "...",
        "score": ...,
        "toelichting": "...",
        "referentie": "..."
      }},
      ...
    ]
    """)

    chain = prompt_template | llm | StrOutputParser()

    # --- Run de chain ---
    with st.spinner("🔍 Tekst wordt nagekeken..."):
        output = chain.invoke({"tekst": tekst, "criteria": json.dumps(criteria, ensure_ascii=False)})

    # --- JSON proberen te parsen ---
    try:
        beoordeling = json.loads(output)
    except json.JSONDecodeError:
        beoordeling = json.loads(output[output.find('['):output.rfind(']')+1])

    # --- Resultaten tonen ---
    st.subheader("📊 Resultaten")
    for item in beoordeling:
        with st.expander(f"{item['criterium']} — Score: {item['score']}"):
            st.markdown(f"**Toelichting:** {item['toelichting']}")
            st.markdown(f"> **Referentie:** {item['referentie']}")

    st.success("✅ Nakijken voltooid!")
