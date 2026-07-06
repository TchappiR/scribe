"""Transcription audio (Speech-to-Text) via l'API Groq."""
import os
from groq import Groq
from source.config import GROQ_API_KEY, STT_MODEL


def transcribe(audio_path: str) -> str:
    """Reçoit le chemin d'un fichier audio, retourne sa transcription texte."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

    client = Groq(api_key=GROQ_API_KEY)
    try:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_path), audio_file.read()),
                model=STT_MODEL,
                response_format="verbose_json",
            )
    except Exception as exc:
        raise RuntimeError(f"Erreur lors de l'appel STT Groq : {exc}") from exc

    return transcription.text