from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    target_dir = repo_root / "09_MobileApps" / "flutter_app" / "assets" / "models"
    target_dir.mkdir(parents=True, exist_ok=True)
    note_path = target_dir / "coral_single_float32.tflite.README.txt"
    note_path.write_text(
        "Place the exported coral_single_float32.tflite file here after converting the seed42 SWA model.\n",
        encoding="utf-8",
    )
    print(f"Prepared model asset folder: {target_dir}")


if __name__ == "__main__":
    main()
