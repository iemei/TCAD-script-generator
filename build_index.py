
from src.loaders import load_pdf, load_text_file, chunk_text
from src.embeddings import load_embedding_model
import faiss
import pickle
import os

os.makedirs("vectorstore", exist_ok=True)

embed_model = load_embedding_model()

# Load data
sde_text = load_pdf(SDE_MANUAL)
sdevice_text = load_pdf(SDEVICE_MANUAL)
sample_sde = load_text_file(SDE_EXAMPLE)
sample_sdevice = load_text_file(SDEVICE_EXAMPLE)

manual_chunks, manual_tags = [], []
example_chunks, example_tags = [], []

for c in chunk_text(sde_text):
    manual_chunks.append(c)
    manual_tags.append("MANUAL_SDE")

for c in chunk_text(sdevice_text):
    manual_chunks.append(c)
    manual_tags.append("MANUAL_SDEVICE")

for c in chunk_text(sample_sde):
    example_chunks.append(c)
    example_tags.append("EXAMPLE_SDE")

for c in chunk_text(sample_sdevice):
    example_chunks.append(c)
    example_tags.append("EXAMPLE_SDEVICE")

all_chunks = manual_chunks + example_chunks
all_tags = manual_tags + example_tags

embeddings = embed_model.encode(all_chunks, batch_size=32, show_progress_bar=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "vectorstore/faiss_index.bin")

with open("vectorstore/chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

with open("vectorstore/tags.pkl", "wb") as f:
    pickle.dump(all_tags, f)

print("RAG index built successfully.")
