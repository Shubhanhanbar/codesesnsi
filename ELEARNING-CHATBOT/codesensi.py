# =========================
# IMPORTS
# =========================
import streamlit as st
import chromadb
import ollama
from pypdf import PdfReader
import hashlib


# =========================
# CONFIG
# =========================
CHROMA_PATH = "./codesensei_db"
COLLECTION = "rules"

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "phi3:mini"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
N_RESULTS = 5


# =========================
# DB INIT
# =========================
@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=COLLECTION)


# =========================
# CHUNKING
# =========================
def chunk_text(text):

    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - CHUNK_OVERLAP

    return chunks


# =========================
# FILE READ
# =========================
def read_file(file):

    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    return file.read().decode("utf-8")


# =========================
# EMBEDDING
# =========================
def embed(texts):
    res = ollama.embed(
        model=EMBED_MODEL,
        input=texts
    )
    return res["embeddings"]


def make_id(name, i):
    return hashlib.md5(f"{name}_{i}".encode()).hexdigest()


# =========================
# INGEST RULES
# =========================
def ingest(file, collection):

    text = read_file(file)
    chunks = chunk_text(text)

    collection.upsert(
        documents=chunks,
        embeddings=embed(chunks),
        ids=[make_id(file.name, i)
             for i in range(len(chunks))],
        metadatas=[
            {"source": file.name}
            for _ in chunks
        ]
    )

    return len(chunks)


# =========================
# RETRIEVE RULES
# =========================
def retrieve(code, collection):

    if collection.count() == 0:
        return []

    vec = embed([code])[0]

    results = collection.query(
        query_embeddings=[vec],
        n_results=N_RESULTS,
        include=["documents", "metadatas"]
    )

    rules = []

    for doc, meta in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        rules.append(
            f"[SOURCE: {meta['source']}]\n{doc}"
        )

    return rules


# =========================
# PROMPT
# =========================
SYSTEM_PROMPT = """
You are CodeSensei, a strict coding-standards reviewer.

Review user code ONLY using the retrieved coding standards.
Do NOT evaluate logic, performance, security, or correctness.

Every issue MUST be backed by an exact RULE_ID from retrieved documents.
If no rule applies, return PASS and stay silent.

Allowed topics:
• Style
• Naming
• Formatting
• Documentation
• Architecture patterns
• Explicit anti-patterns

Forbidden:
• Debugging
• Feature suggestions
• Personal opinions

If code language is not covered → return PASS with message.

Output STRICT JSON:

{
 "verdict": "PASS | NEEDS_CHANGES",
 "issues": [
   {
     "rule_id": "",
     "severity": "LOW | MEDIUM | HIGH",
     "guideline": "",
     "problem": "",
     "suggested_fix": ""
   }
 ],
 "positive_notes": []
}

Deduplicate repeated rules.
If rules conflict, prefer the more specific.
If you cannot cite a rule — do NOT say it.
"""


def build_prompt(code, lang, rules):

    context = "\n\n".join(rules)

    return f"""
LANGUAGE: {lang}

CODING RULES:
{context}

CODE:
{code}
"""


# =========================
# STREAMLIT UI
# =========================
st.title("🧠 CodeSensei - AI Code Reviewer")

collection = get_collection()

# -------- Upload Rules ------
with st.sidebar:
    st.header("Upload Coding Standards")

    files = st.file_uploader(
        "Upload documents",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )

    if files and st.button("Ingest"):
        for f in files:
            n = ingest(f, collection)
            st.success(f"{f.name} → {n} chunks")


# -------- Input -------------
language = st.selectbox(
    "Language",
    ["Python", "C++", "Java"]
)

code = st.text_area(
    "Paste Code",
    height=300
)


# -------- Review ------------
if st.button("Review Code"):

    if not code.strip():
        st.warning("Paste code first")
        st.stop()

    rules = retrieve(code, collection)

    if not rules:
        st.warning("No coding rules found")
        st.stop()

    prompt = build_prompt(code, language, rules)

    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {"role": "system",
             "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": prompt}
        ]
    )

    st.markdown(response["message"]["content"])