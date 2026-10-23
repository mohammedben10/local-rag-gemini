import os
from dotenv import load_dotenv
from google import genai

# On charge le fichier .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Erreur : Le fichier .env n'est pas lu ou la clé est vide.")
else:
    print(f"Clé détectée (commence par) : {api_key[:10]}...")
    
    # On se connecte à Google pour voir les modèles autorisés
    try:
        client = genai.Client(api_key=api_key)
        print("\nModèles autorisés pour cette clé :")
        for m in client.models.list():
            if "gemini" in m.name:
                print("-", m.name)
    except Exception as e:
        print("Erreur de connexion :", e)