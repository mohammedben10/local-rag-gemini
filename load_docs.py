from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def load_docs(folder):
    docs = []
    for path in Path(folder).glob("*.md"):
        text = path.read_text(encoding="utf-8")
        docs.append({"source": path.name, "text": text})
    return docs

def split_text(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = []
    for doc in docs:
        text_chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(text_chunks):
            chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })
    return chunks

def build_vector_db():
    docs = load_docs("docs")
    chunks = split_text(docs)
    
    print(f"Chargement de {len(chunks)} chunks dans la base de données...")
    
    # 1. On charge le modèle d'embedding local gratuit
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. On extrait juste le texte de chaque dictionnaire chunk
    texts = [chunk["text"] for chunk in chunks]
    
    # 3. On génère les vecteurs et on sauvegarde sur le disque
    db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print("Base de données vectorielle (ChromaDB) sauvegardée avec succès !")

if __name__ == "__main__":
    build_vector_db()