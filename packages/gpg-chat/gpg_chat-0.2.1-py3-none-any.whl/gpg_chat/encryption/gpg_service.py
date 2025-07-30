import json
import subprocess
from pathlib import Path

from .utils import FileEnvelope


def encrypt_message(text: str, recipients: list[str]) -> str:
    args = ["gpg", "-aes"] + [f"-r {r}" for r in recipients]
    return _run_gpg(args, input_data=text.encode())


def decrypt_message(ciphertext: str) -> str:
    return _run_gpg(["gpg", "-d"], input_data=ciphertext.encode())


def encrypt_file(filepath: Path, recipients: list[str]) -> str:
    file = FileEnvelope.encode(filepath)
    envelope_json = json.dumps(file.__dict__)
    return encrypt_message(envelope_json, recipients)


def recipient_exists(recipient: str) -> bool:
    try:
        proc = subprocess.run(
            ["gpg", "--list-keys", recipient],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(proc.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def _run_gpg(args: list[str], input_data: bytes) -> str:
    proc = subprocess.run(args, input=input_data, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    return proc.stdout.decode()
