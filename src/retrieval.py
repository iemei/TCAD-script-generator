
def retrieve(query, index, embed_model, all_chunks, all_tags,
             k_manual=5, k_example=3):
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
