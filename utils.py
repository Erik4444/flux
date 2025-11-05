import os
import json
import datetime
from pathlib import Path

def make_output_dir(base_path: str) -> str:
    """
    Erstellt einen neuen Unterordner im angegebenen Basisordner.
    Der Name enthält Datum und Uhrzeit, z. B. outputs/2025-10-29_11-23-45.
    Gibt den Pfad zurück.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.expanduser(os.path.join(base_path, timestamp))
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")
    return output_dir


def load_prompts(prompt_file: str) -> list[str]:
    """
    Lädt Textprompts aus einer Datei (eine Zeile = ein Prompt).
    Leerzeilen und Kommentare (# ...) werden ignoriert.
    """
    prompt_file = Path(prompt_file)
    if not prompt_file.is_file():
        raise FileNotFoundError(f"File not found: {prompt_file}")

    with open(prompt_file, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines()]

    prompts = [ln for ln in lines if ln and not ln.startswith("#")]
    print(f"Loaded {len(prompts)} prompts from {prompt_file}")
    return prompts


def save_metadata(output_dir: str, metadata: dict) -> None:
    """
    Speichert Metadaten (z. B. Modellname, Prompts etc.) als JSON im Output-Ordner.
    """
    meta_file = os.path.join(output_dir, "metadata.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Saved metadata → {meta_file}")