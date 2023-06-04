from datetime import datetime


class Task:
    def __init__(
            self,
            task_id: int,
            name: str,
            date_active: datetime,
            status: str,
            created_at: datetime = None,
            description: str = None,
    ):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.date_active = date_active
        self.created_at = created_at or datetime.now()
        self.status = status
