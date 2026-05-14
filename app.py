
import streamlit as st
import fitz
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from google.colab import userdata

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="TCAD RAG Generator", layout="wide")

# =========================
# LOAD MODELS
# =========================
@st.cache_resource
def load_models():
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    return embed_model

embed_model = load_models()

# =========================
# LOAD DATA (FAISS + chunks)
# =========================
@st.cache_resource
def load_index():
    index = faiss.read_index(FAISS_INDEX_PATH)

    with open(CHUNKS_PATH, "rb") as f:
        all_chunks = pickle.load(f)

    with open(TAGS_PATH, "rb") as f:
        all_tags = pickle.load(f)

    return index, all_chunks, all_tags

index, all_chunks, all_tags = load_index()

# =========================
# GEMINI SETUP
# =========================
import os
# Sidebar input for API key
st.sidebar.title("🔑 API Configuration")

api_key = st.sidebar.text_input(
    "Enter your Gemini API Key",
    type="password"
)

# Stop app if no key
if not api_key:
    st.warning("Please enter your API key to continue")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel('gemini-flash-latest')

# =========================
# RETRIEVAL
# =========================
def retrieve(query, k_manual=5, k_example=3):
    q_emb = embed_model.encode([query])
    D, I = index.search(q_emb, k_manual + k_example)

    manual_context = []
    example_context = []

    for i in I[0]:
        tag = all_tags[i]
        if "EXAMPLE" in tag and len(example_context) < k_example:
            example_context.append(f"[{tag}] {all_chunks[i]}")
        elif "MANUAL" in tag and len(manual_context) < k_manual:
            manual_context.append(f"[{tag}] {all_chunks[i]}")

    return "\n\n".join(manual_context), "\n\n".join(example_context)

# =========================
# GENERATION
# =========================
def query_rag(user_query):

    manual_ctx, example_ctx = retrieve(user_query)

    prompt = f"""
You are a Synopsys Sentaurus TCAD expert.

EXAMPLES:
{example_ctx}

DOCUMENTATION:
{manual_ctx}

TASK:
Generate complete scripts.

SDE:
- substrate, source, drain, channel, oxide, gate
- LDD + Halo
- mesh + contacts

SDevice:
- Physics (Mobility, SRH, Fermi)
- Solve
- Id-Vg sweep

RULES:
- Follow example structure
- No explanation

USER:
{user_query}

OUTPUT:

### SDE SCRIPT
### SDEVICE SCRIPT
"""

    response = gemini_model.generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )

    return response.text if response.text else "⚠️ No response"

# =========================
# VALIDATOR
# =========================
def validate(script):
    errors = []
    if "Physics {" not in script:
        errors.append("Missing Physics block")
    if "Solve {" not in script:
        errors.append("Missing Solve block")
    if "contact" not in script.lower():
        errors.append("Missing contacts")
    return errors

# =========================
# UI
# =========================
st.title("🧠 TCAD Script Generator (RAG + Gemini)")

col1, col2 = st.columns(2)

with col1:
    device = st.selectbox("Device Type", ["NMOS", "PMOS"])
    node = st.selectbox("Technology Node", ["45nm", "35nm", "28nm"])
    halo = st.checkbox("Include Halo Doping", True)

with col2:
    user_query = st.text_area(
        "Describe your device",
        f"Generate a {node} {device} with LDD and halo doping and Id-Vg sweep"
    )

if st.button("🚀 Generate Scripts"):

    with st.spinner("Generating TCAD scripts..."):
        output = query_rag(user_query)

    st.success("Done!")

    # Split output
    if "### SDEVICE SCRIPT" in output:
        sde, sdevice = output.split("### SDEVICE SCRIPT")
    else:
        sde, sdevice = output, ""

    # Display scripts
    st.subheader("📄 SDE Script")
    st.code(sde, language="python")

    st.subheader("📄 SDevice Script")
    st.code(sdevice, language="python")

    # Download buttons
    st.download_button("Download SDE", sde, "sde.cmd")
    st.download_button("Download SDevice", sdevice, "sdevice.cmd")

    # Validation
    st.subheader("🧪 Validation")
    errors = validate(output)

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("No major issues detected ✅")



import os
os.environ["GEMINI_API_KEY"] = "Gemini_API_Key"


from google.colab import userdata
from pyngrok import ngrok

# Get ngrok auth token from Colab secrets
NGROK_AUTH_TOKEN = userdata.get('NGROK_AUTH_TOKEN')
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

print("ngrok authenticated!")


#Run streamlit app

!streamlit run app.py &>/dev/null &
from pyngrok import ngrok
print(ngrok.connect(8501))
