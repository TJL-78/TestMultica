"""Command-line interface for the Daily Activity Management System."""

import argparse
import sys
from datetime import date, time
from .manager import ActivityManager


def main():
    parser = argparse.ArgumentParser(
        description="日常活动管理系统 - Daily Activity Management System"
    )
    parser.add_argument(
        "--data", default="activities.json", help="Path to data file"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add activity
    add_parser = subparsers.add_parser("add", help="Add a new activity")
    add_parser.add_argument("title", help="Activity title")
    add_parser.add_argument("-d", "--description", default="", help="Description")
    add_parser.add_argument(
        "-p", "--priority", choices=["low", "medium", "high", "urgent"], default="medium"
    )
    add_parser.add_argument("--date", help="Scheduled date (YYYY-MM-DD)")
    add_parser.add_argument("--time", help="Scheduled time (HH:MM)")
    add_parser.add_argument("--duration", type=int, help="Duration in minutes")
    add_parser.add_argument("-c", "--category", default="", help="Category")
    add_parser.add_argument("-t", "--tags", nargs="*", default=[], help="Tags")
    add_parser.add_argument(
        "--recurrence", choices=["none", "daily", "weekly", "monthly"], default="none"
    )

    # List activities
    list_parser = subparsers.add_parser("list", help="List activities")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--priority", help="Filter by priority")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--today", action="store_true", help="Show today's activities")

    # Complete activity
    complete_parser = subparsers.add_parser("complete", help="Complete an activity")
    complete_parser.add_argument("id", help="Activity ID")

    # Start activity
    start_parser = subparsers.add_parser("start", help="Start an activity")
    start_parser.add_argument("id", help="Activity ID")

    # Cancel activity
    cancel_parser = subparsers.add_parser("cancel", help="Cancel an activity")
    cancel_parser.add_argument("id", help="Activity ID")

    # Delete activity
    delete_parser = subparsers.add_parser("delete", help="Delete an activity")
    delete_parser.add_argument("id", help="Activity ID")

    # Statistics
    subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()
    manager = ActivityManager(args.data)

    if args.command == "add":
        scheduled_date = date.fromisoformat(args.date) if args.date else None
        scheduled_time = time.fromisoformat(args.time) if args.time else None
        activity = manager.create_activity(
            title=args.title,
            description=args.description,
            priority=args.priority,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            duration_minutes=args.duration,
            category=args.category,
            tags=args.tags,
            recurrence=args.recurrence,
        )
        print(f"Created activity: {activity.title} (ID: {activity.id})")

    elif args.command == "list":
        if args.today:
            activities = manager.today_activities()
        else:
            activities = manager.list_activities(
                status=args.status, priority=args.priority, category=args.category
            )
        if not activities:
            print("No activities found.")
        else:
            for a in activities:
                status_icon = {
                    "pending": "○",
                    "in_progress": "◑",
                    "completed": "●",
                    "cancelled": "✕",
                }.get(a.status.value, "?")
                date_str = f" [{a.scheduled_date}]" if a.scheduled_date else ""
                print(f"  {status_icon} [{a.priority.value}] {a.title}{date_str}")
                print(f"    ID: {a.id}")

    elif args.command == "complete":
        activity = manager.complete_activity(args.id)
        if activity:
            print(f"Completed: {activity.title}")
        else:
            print("Activity not found.")

    elif args.command == "start":
        activity = manager.start_activity(args.id)
        if activity:
            print(f"Started: {activity.title}")
        else:
            print("Activity not found.")

    elif args.command == "cancel":
        activity = manager.cancel_activity(args.id)
        if activity:
            print(f"Cancelled: {activity.title}")
        else:
            print("Activity not found.")

    elif args.command == "delete":
        if manager.delete_activity(args.id):
            print("Activity deleted.")
        else:
            print("Activity not found.")

    elif args.command == "stats":
        stats = manager.get_statistics()
        print(f"Total activities: {stats['total']}")
        if stats["by_status"]:
            print("By status:")
            for s, c in stats["by_status"].items():
                print(f"  {s}: {c}")
        if stats["by_priority"]:
            print("By priority:")
            for p, c in stats["by_priority"].items():
                print(f"  {p}: {c}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
