import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Charger la clé API secrète depuis le fichier .env
load_dotenv()

def poser_question(question):
    print("1. Traduction de la question et recherche dans ChromaDB...")
    # On prépare la base de données
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # On récupère les 3 meilleurs extraits
    resultats = db.similarity_search(question, k=3)
    
    # On rassemble ces 3 extraits en un seul gros texte (le contexte)
    contexte_trouve = "\n\n".join([doc.page_content for doc in resultats])
    
    print("2. Envoi des extraits au LLM (Google Gemini) pour rédaction...\n")
    
    # On initialise le LLM
    llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

    # On construit le "Prompt" (les instructions strictes pour le LLM)
    prompt = f"""
    Tu es un expert technique. Réponds à la question posée en te basant UNIQUEMENT sur le contexte ci-dessous. 
    Ne tire aucune information de tes connaissances générales. Si la réponse ne figure pas dans le contexte, dis simplement "L'information n'est pas dans le document".
    
    CONTEXTE :
    {contexte_trouve}
    
    QUESTION : {question}
    """
    
    # Le LLM lit le prompt et génère la réponse finale
    reponse = llm.invoke(prompt)
    
    print("================ RÉPONSE FINALE ================")
    print(reponse.content)
    print("================================================\n")

if __name__ == "__main__":
    ma_question = "Quels sont les outils utilisés dans cette plateforme ?"
    poser_question(ma_question)