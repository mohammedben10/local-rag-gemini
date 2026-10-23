from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def tester_recherche():
    # 1. On charge le même modèle de traduction mathématique
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. On se connecte à ta base de données stockée sur le disque
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # 3. La question (à modifier selon le contenu de ton document !)
    question = "Quels sont les outils utilisés dans cette plateforme ?"
    
    # 4. On demande à ChromaDB de trouver les 3 morceaux les plus pertinents (k=3)
    resultats = db.similarity_search(question, k=3)
    
    print(f"Question posée : '{question}'\n")
    for i, doc in enumerate(resultats):
        print(f"--- Extrait trouvé n°{i+1} ---")
        print(doc.page_content)
        print("-" * 30 + "\n")

if __name__ == "__main__":
    tester_recherche()