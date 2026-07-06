"""Configuration centrale de Scribe : clé API et identifiants des modèles."""
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY manquante. Copie .env.example vers .env et renseigne ta clé."
    )

# Les noms de modèles ne sont définis QU'ICI (un seul endroit dans le projet).
STT_MODEL = "whisper-large-v3-turbo"    # rapide et peu cher pour la transcription
LLM_MODEL = "llama-3.3-70b-versatile"   # bon rapport qualité/coût pour la rédaction