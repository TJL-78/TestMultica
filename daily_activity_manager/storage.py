"""Storage backend for persisting activities."""

import json
import os
from typing import List, Optional
from .models import Activity


class JSONStorage:
    """JSON file-based storage for activities."""

    def __init__(self, filepath: str = "activities.json"):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        """Create storage file if it doesn't exist."""
        if not os.path.exists(self.filepath):
            self._write_all([])

    def _read_all(self) -> List[dict]:
        """Read all activities from file."""
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_all(self, data: List[dict]):
        """Write all activities to file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save(self, activity: Activity):
        """Save or update an activity."""
        activities = self._read_all()
        # Update existing or append new
        for i, a in enumerate(activities):
            if a["id"] == activity.id:
                activities[i] = activity.to_dict()
                self._write_all(activities)
                return
        activities.append(activity.to_dict())
        self._write_all(activities)

    def get(self, activity_id: str) -> Optional[Activity]:
        """Get an activity by ID."""
        for a in self._read_all():
            if a["id"] == activity_id:
                return Activity.from_dict(a)
        return None

    def get_all(self) -> List[Activity]:
        """Get all activities."""
        return [Activity.from_dict(a) for a in self._read_all()]

    def delete(self, activity_id: str) -> bool:
        """Delete an activity by ID."""
        activities = self._read_all()
        filtered = [a for a in activities if a["id"] != activity_id]
        if len(filtered) == len(activities):
            return False
        self._write_all(filtered)
        return True
