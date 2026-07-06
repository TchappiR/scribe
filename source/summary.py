"""Génération d'un compte rendu structuré (LLM) via l'API Groq."""
import os
from groq import Groq
from source.config import GROQ_API_KEY, LLM_MODEL

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "summary.txt")


def _load_system_prompt() -> str:
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return f.read()


def summarize(transcript: str) -> str:
    """Reçoit une transcription brute, retourne un compte rendu structuré."""
    client = Groq(api_key=GROQ_API_KEY)
    try:
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": _load_system_prompt()},
                {"role": "user", "content": transcript},
            ],
            temperature=0.2,
        )
    except Exception as exc:
        raise RuntimeError(f"Erreur lors de l'appel LLM Groq : {exc}") from exc

    return completion.choices[0].message.content