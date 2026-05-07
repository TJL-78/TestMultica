"""Data models for the Daily Activity Management System."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, date, time
from enum import Enum
from typing import Optional, List


class ActivityStatus(Enum):
    """Status of an activity."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ActivityPriority(Enum):
    """Priority level of an activity."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class RecurrenceType(Enum):
    """Recurrence pattern for repeating activities."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Activity:
    """Represents a daily activity."""
    title: str
    description: str = ""
    status: ActivityStatus = ActivityStatus.PENDING
    priority: ActivityPriority = ActivityPriority.MEDIUM
    scheduled_date: Optional[date] = None
    scheduled_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    category: str = ""
    tags: List[str] = field(default_factory=list)
    recurrence: RecurrenceType = RecurrenceType.NONE
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def complete(self):
        """Mark this activity as completed."""
        self.status = ActivityStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def cancel(self):
        """Mark this activity as cancelled."""
        self.status = ActivityStatus.CANCELLED
        self.updated_at = datetime.now()

    def start(self):
        """Mark this activity as in progress."""
        self.status = ActivityStatus.IN_PROGRESS
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert activity to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "duration_minutes": self.duration_minutes,
            "category": self.category,
            "tags": self.tags,
            "recurrence": self.recurrence.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Activity":
        """Create an Activity from a dictionary."""
        activity = cls(
            title=data["title"],
            description=data.get("description", ""),
            status=ActivityStatus(data.get("status", "pending")),
            priority=ActivityPriority(data.get("priority", "medium")),
            category=data.get("category", ""),
            tags=data.get("tags", []),
            recurrence=RecurrenceType(data.get("recurrence", "none")),
            duration_minutes=data.get("duration_minutes"),
        )
        activity.id = data.get("id", activity.id)
        if data.get("scheduled_date"):
            activity.scheduled_date = date.fromisoformat(data["scheduled_date"])
        if data.get("scheduled_time"):
            activity.scheduled_time = time.fromisoformat(data["scheduled_time"])
        if data.get("created_at"):
            activity.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            activity.updated_at = datetime.fromisoformat(data["updated_at"])
        if data.get("completed_at"):
            activity.completed_at = datetime.fromisoformat(data["completed_at"])
        return activity
