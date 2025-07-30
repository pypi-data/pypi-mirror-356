from pathlib import Path

from platformdirs import user_data_dir

APP_NAME = "gpg-chat"


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def conv_file(recipients: list[str]) -> Path:
    return _ensure_dir(Path(user_data_dir(APP_NAME))) / f"conversation-{'-'.join(recipients)}.txt"
