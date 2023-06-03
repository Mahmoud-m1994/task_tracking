from datetime import datetime


def is_start_date_after_end_date(start_date: datetime, end_date: datetime) -> bool:
    return start_date >= end_date


def is_date_in_past(date_str: str) -> bool:
    date = datetime.strptime(date_str, "%Y-%m-%d")  # Convert the string to a datetime object
    return date < datetime.now()


def is_existing_end_date_after_start_date(existing_end_date_str: str, new_start_date_str: str) -> bool:
    existing_end_date = datetime.strptime(existing_end_date_str, "%Y-%m-%d %H:%M:%S").date()
    new_start_date = datetime.strptime(new_start_date_str, "%Y-%m-%d").date()
    return existing_end_date >= new_start_date


def is_existing_end_date_after_end_date(existing_end_date_str: str, new_end_date_str: str) -> bool:
    existing_end_date = datetime.strptime(existing_end_date_str, "%Y-%m-%d %H:%M:%S").date()
    new_end_date = datetime.strptime(new_end_date_str, "%Y-%m-%d").date()
    return existing_end_date >= new_end_date


def is_existing_start_date_before_end_date(existing_start_date_str: str, new_end_date_str: str) -> bool:
    existing_start_date = datetime.strptime(existing_start_date_str, "%Y-%m-%d %H:%M:%S").date()
    new_end_date = datetime.strptime(new_end_date_str, "%Y-%m-%d").date()
    return existing_start_date <= new_end_date
