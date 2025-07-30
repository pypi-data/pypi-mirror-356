import base64
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileEnvelope:
    filename: str
    content: str

    @staticmethod
    def encode(path: Path) -> "FileEnvelope":
        b64_content = base64.b64encode(path.read_bytes()).decode("ascii")
        return FileEnvelope(path.name, b64_content)

    def decode(self) -> str:
        path = Path(self.filename)
        _ = path.write_bytes(base64.b64decode(self.content))
        return str(path)


def try_parse_envelope(decrypted_text: str) -> FileEnvelope | None:
    try:
        data = json.loads(decrypted_text)
        if isinstance(data, dict) and "filename" in data:
            return FileEnvelope(**data)
    except Exception:
        return None
