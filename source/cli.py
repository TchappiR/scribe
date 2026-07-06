import argparse
import os
from datetime import datetime

from source.transcription import transcribe
from source.summary import summarize


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scribe : transforme un audio en compte rendu structuré."
    )
    parser.add_argument("audio", help="Chemin du fichier audio à traiter")
    args = parser.parse_args()

    print("→ Transcription en cours...")
    transcript = transcribe(args.audio)

    print("→ Rédaction du compte rendu...")
    report = summarize(transcript)

    os.makedirs("output", exist_ok=True)
    filename = f"output/compte-rendu-{datetime.now():%Y-%m-%d_%H-%M-%S}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print("\n" + report)
    print(f"\n✓ Compte rendu enregistré dans {filename}")


if __name__ == "__main__":
    main()