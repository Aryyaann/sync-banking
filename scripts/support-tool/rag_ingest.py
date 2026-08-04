from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer
import uuid
import os
import re
import glob

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:TuNuevaContraseñaSegura2026XYZ@kodama.proxy.rlwy.net:50752/railway")
engine = create_engine(DATABASE_URL)

print("Cargando modelo de embeddings (la primera vez tarda un poco, descarga ~80MB)...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")  # soporta español bien


def chunk_markdown(texto, max_chars=800):
    """Divide un markdown en fragmentos por secciones (##), y si una sección es muy larga, la subdivide por párrafos."""
    secciones = re.split(r"\n(?=#{1,3} )", texto)
    chunks = []
    for seccion in secciones:
        seccion = seccion.strip()
        if not seccion:
            continue
        if len(seccion) <= max_chars:
            chunks.append(seccion)
        else:
            parrafos = seccion.split("\n\n")
            actual = ""
            for p in parrafos:
                if len(actual) + len(p) > max_chars and actual:
                    chunks.append(actual.strip())
                    actual = p
                else:
                    actual += "\n\n" + p
            if actual.strip():
                chunks.append(actual.strip())
    return chunks


def main():
    archivos = ["README.md"] + glob.glob("docs/*.md")

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM docs_chunks"))  # re-ingesta completa cada vez, más simple que actualizar incrementalmente

        total = 0
        for archivo in archivos:
            if not os.path.exists(archivo):
                print(f"  (aviso: {archivo} no encontrado, se omite)")
                continue

            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()

            chunks = chunk_markdown(contenido)
            embeddings = model.encode(chunks)

            for chunk_text, embedding in zip(chunks, embeddings):
                conn.execute(text("""
                    INSERT INTO docs_chunks (id, source_file, chunk_text, embedding)
                    VALUES (:id, :source, :chunk, :emb)
                """), {
                    "id": str(uuid.uuid4()),
                    "source": archivo,
                    "chunk": chunk_text,
                    "emb": list(map(float, embedding)),
                })
                total += 1

            print(f"  {archivo}: {len(chunks)} fragmentos")

    print(f"\n✅ Ingesta completa: {total} fragmentos indexados")


if __name__ == "__main__":
    main()