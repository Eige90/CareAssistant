import json
from datetime import datetime
from uuid import uuid4

from core.paths import DATA_DIR


class ClientStore:
    def __init__(self):
        self.path = DATA_DIR / "clients.json"
        self._clients = []
        self.load()

    def load(self):
        if not self.path.exists():
            self._clients = []
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self._clients = data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            self._clients = []

    def save(self):
        self.path.write_text(
            json.dumps(self._clients, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def all(self):
        return sorted(
            [dict(x) for x in self._clients],
            key=lambda x: (x.get("last_name", "").lower(), x.get("first_name", "").lower()),
        )

    def get(self, client_id):
        for item in self._clients:
            if item.get("id") == client_id:
                return dict(item)
        return None

    def add(self, data):
        item = dict(data)
        item["id"] = str(uuid4())
        item["created_at"] = datetime.now().isoformat(timespec="seconds")
        item["updated_at"] = item["created_at"]
        self._clients.append(item)
        self.save()
        return dict(item)

    def update(self, client_id, data):
        for i, item in enumerate(self._clients):
            if item.get("id") == client_id:
                updated = dict(item)
                updated.update(data)
                updated["updated_at"] = datetime.now().isoformat(timespec="seconds")
                self._clients[i] = updated
                self.save()
                return dict(updated)
        return None

    def archive(self, client_id):
        client = self.get(client_id)
        if not client:
            return None
        client["status"] = "Beendet"
        return self.update(client_id, client)
