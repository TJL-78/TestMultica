"""Core manager for daily activities."""

from datetime import date, time, datetime
from typing import List, Optional
from .models import Activity, ActivityStatus, ActivityPriority, RecurrenceType
from .storage import JSONStorage


class ActivityManager:
    """Manages daily activities with CRUD and query operations."""

    def __init__(self, storage_path: str = "activities.json"):
        self.storage = JSONStorage(storage_path)

    def create_activity(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        scheduled_date: Optional[date] = None,
        scheduled_time: Optional[time] = None,
        duration_minutes: Optional[int] = None,
        category: str = "",
        tags: Optional[List[str]] = None,
        recurrence: str = "none",
    ) -> Activity:
        """Create a new activity."""
        activity = Activity(
            title=title,
            description=description,
            priority=ActivityPriority(priority),
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            duration_minutes=duration_minutes,
            category=category,
            tags=tags or [],
            recurrence=RecurrenceType(recurrence),
        )
        self.storage.save(activity)
        return activity

    def get_activity(self, activity_id: str) -> Optional[Activity]:
        """Get an activity by ID."""
        return self.storage.get(activity_id)

    def list_activities(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        scheduled_date: Optional[date] = None,
    ) -> List[Activity]:
        """List activities with optional filters."""
        activities = self.storage.get_all()

        if status:
            activities = [a for a in activities if a.status == ActivityStatus(status)]
        if priority:
            activities = [a for a in activities if a.priority == ActivityPriority(priority)]
        if category:
            activities = [a for a in activities if a.category == category]
        if scheduled_date:
            activities = [a for a in activities if a.scheduled_date == scheduled_date]

        return activities

    def today_activities(self) -> List[Activity]:
        """Get all activities scheduled for today."""
        return self.list_activities(scheduled_date=date.today())

    def complete_activity(self, activity_id: str) -> Optional[Activity]:
        """Mark an activity as completed."""
        activity = self.storage.get(activity_id)
        if activity:
            activity.complete()
            self.storage.save(activity)
        return activity

    def start_activity(self, activity_id: str) -> Optional[Activity]:
        """Mark an activity as in progress."""
        activity = self.storage.get(activity_id)
        if activity:
            activity.start()
            self.storage.save(activity)
        return activity

    def cancel_activity(self, activity_id: str) -> Optional[Activity]:
        """Cancel an activity."""
        activity = self.storage.get(activity_id)
        if activity:
            activity.cancel()
            self.storage.save(activity)
        return activity

    def delete_activity(self, activity_id: str) -> bool:
        """Delete an activity permanently."""
        return self.storage.delete(activity_id)

    def update_activity(self, activity_id: str, **kwargs) -> Optional[Activity]:
        """Update activity fields."""
        activity = self.storage.get(activity_id)
        if not activity:
            return None

        for key, value in kwargs.items():
            if hasattr(activity, key):
                if key == "priority":
                    value = ActivityPriority(value)
                elif key == "recurrence":
                    value = RecurrenceType(value)
                setattr(activity, key, value)

        activity.updated_at = datetime.now()
        self.storage.save(activity)
        return activity

    def get_statistics(self) -> dict:
        """Get activity statistics."""
        activities = self.storage.get_all()
        total = len(activities)
        by_status = {}
        for status in ActivityStatus:
            count = len([a for a in activities if a.status == status])
            if count > 0:
                by_status[status.value] = count

        by_priority = {}
        for priority in ActivityPriority:
            count = len([a for a in activities if a.priority == priority])
            if count > 0:
                by_priority[priority.value] = count

        return {
            "total": total,
            "by_status": by_status,
            "by_priority": by_priority,
        }
