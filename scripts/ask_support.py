from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
from anthropic import Anthropic
import numpy as np
import os
import sys

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:TuNuevaContraseñaSegura2026XYZ@kodama.proxy.rlwy.net:50752/railway")
print(f"[debug] DATABASE_URL = {repr(DATABASE_URL)}")
engine = create_engine(DATABASE_URL)
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
anthropic_client = Anthropic()


def buscar_relevantes(pregunta, top_k=5):
    pregunta_emb = model.encode([pregunta])[0]

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT source_file, chunk_text, embedding FROM docs_chunks")).mappings().all()

    similitudes = []
    for row in rows:
        emb = np.array(row["embedding"])
        sim = np.dot(pregunta_emb, emb) / (np.linalg.norm(pregunta_emb) * np.linalg.norm(emb))
        similitudes.append((sim, row["source_file"], row["chunk_text"]))

    similitudes.sort(key=lambda x: x[0], reverse=True)
    return similitudes[:top_k]


def preguntar(pregunta):
    relevantes = buscar_relevantes(pregunta)

    contexto = "\n\n---\n\n".join(
        f"[Fuente: {fuente}]\n{texto}" for _, fuente, texto in relevantes
    )

    prompt = f"""Eres el centro de soporte interno del proyecto "Sync Banking". Responde la pregunta del usuario basándote EXCLUSIVAMENTE en el siguiente contexto extraído de la documentación del proyecto. Si el contexto no contiene la respuesta, dilo claramente en vez de inventar.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

Responde en español, de forma directa y práctica, citando qué archivo de documentación contiene cada dato relevante."""

    response = anthropic_client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )

    print("\n" + response.content[0].text)
    print("\n" + "─" * 50)
    print("Fuentes consultadas:", ", ".join(set(f for _, f, _ in relevantes)))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pregunta = " ".join(sys.argv[1:])
        preguntar(pregunta)
    else:
        print("Modo interactivo — escribe 'salir' para terminar.\n")
        while True:
            pregunta = input("Pregunta: ")
            if pregunta.lower() in ("salir", "exit"):
                break
            preguntar(pregunta)