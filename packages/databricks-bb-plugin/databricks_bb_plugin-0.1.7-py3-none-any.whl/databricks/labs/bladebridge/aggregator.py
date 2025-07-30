import os
from email.message import EmailMessage
from pathlib import Path


class Aggregator:

    def __init__(self, folder: Path):
        self._folder = folder

    def aggregate(self) -> str:
        if self.needs_aggregate(self._folder):
            return self._aggregate()
        return self._single()

    @classmethod
    def needs_aggregate(cls, folder: Path) -> bool:
        names = list(name for name in os.listdir(folder) if not name.startswith("."))
        if len(names) == 0:
            return False
        if len(names) > 1:
            return True
        obj = folder / names[0]
        if obj.is_file():
            return False
        return cls.needs_aggregate(obj)

    def _single(self) -> str:
        name = next(
            name for name in os.listdir(self._folder) if not name.startswith(".")
        )
        path = self._folder / name
        return path.read_text("utf-8")

    def _aggregate(self) -> str:
        message = EmailMessage()
        self._add_folder(message, "", self._folder)
        return message.as_string()

    def _add_folder(self, message: EmailMessage, prefix: str, folder: Path):
        names = list(name for name in os.listdir(folder) if not name.startswith("."))
        for name in names:
            path = folder / name
            if path.is_file():
                with open(path, "r", encoding="utf-8") as content:
                    message.add_attachment(content.read(), filename=prefix + name)
            else:
                self._add_folder(message, prefix + name + "/", path)
