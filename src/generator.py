
import google.generativeai as genai
from src.retrieval import retrieve

def query_rag(user_query, index, embed_model, all_chunks, all_tags):
    manual_ctx, example_ctx = retrieve(
        user_query, index, embed_model, all_chunks, all_tags
    )

    prompt = f"""
You are a Synopsys Sentaurus TCAD expert.

EXAMPLES:
{example_ctx}

DOCUMENTATION:
{manual_ctx}

TASK:
Generate complete and runnable SDE and SDevice scripts.

USER:
{user_query}

OUTPUT:
### SDE SCRIPT
### SDEVICE SCRIPT
"""

    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )

    return response.text if response.text else "No response"
