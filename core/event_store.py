import json
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from core.paths import DATA_DIR


class EventStore:
    def __init__(self):
        self.path = DATA_DIR / "events.json"
        self._events = []
        self.load()

    def load(self):
        if not self.path.exists():
            self._events = []
            return
        try:
            self._events = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self._events = []

    def save(self):
        self.path.write_text(
            json.dumps(self._events, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add(self, event):
        item = dict(event)
        item["id"] = str(uuid4())
        item["created_at"] = datetime.now().isoformat(timespec="seconds")
        self._events.append(item)
        self.save()
        return item

    def all(self):
        return list(self._events)

    def for_date(self, iso_date):
        items = [x for x in self._events if x.get("date") == iso_date]
        return sorted(items, key=lambda x: (x.get("all_day", False) is False, x.get("start_time", "")))

    def upcoming(self, limit=6):
        today = date.today().isoformat()
        items = [x for x in self._events if x.get("date", "") >= today]
        items.sort(key=lambda x: (x.get("date", ""), x.get("start_time", "")))
        return items[:limit]
