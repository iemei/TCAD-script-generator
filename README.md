# TCAD RAG Pipeline: Automated Sentaurus Script Generation

A Retrieval-Augmented Generation (RAG) pipeline that converts natural language prompts into executable Synopsys Sentaurus TCAD scripts (`SDE` and `SDevice`) using vector search and Google's Gemini large language model.

---

## Overview

Writing Sentaurus scripts manually is time-consuming and requires detailed knowledge of syntax, device physics models, and simulation workflows.

This project automates the process by combining:

- **Retrieval-Augmented Generation (RAG)** to retrieve relevant sections from Sentaurus manuals and example scripts
- **FAISS** for vector similarity search
- **Sentence Transformers** for semantic embeddings
- **Google Gemini** for script generation
- **Streamlit** for an interactive web interface

Users can describe a device in plain English, and the system generates complete, runnable TCAD scripts.

---

## Example Prompt

> Generate a 35nm NMOSFET with LDD and halo doping and an Id-Vg sweep.

### Output

- `SDE` script defining geometry, contacts, doping, and mesh
- `SDevice` script containing physics models, solver settings, and bias sweeps

---

## Key Features

- Natural language to Sentaurus script generation
- Hybrid retrieval from:
  - Sentaurus SDE and SDevice manuals
  - Example device scripts
- FAISS vector database for fast semantic search
- Prompt engineering to enforce script structure
- Built-in validation for required sections
- Downloadable `.cmd` files
- Streamlit web application

---

## Architecture

```text
User Prompt
    ↓
Embedding Model (all-MiniLM-L6-v2)
    ↓
FAISS Similarity Search
    ↓
Retrieve:
  • Manual Context
  • Example Scripts
    ↓
Prompt Construction
    ↓
Google Gemini
    ↓
Generated:
  • SDE Script
  • SDevice Script
    ↓
Validation + Download
