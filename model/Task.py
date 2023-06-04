from datetime import datetime


class Task:
    def __init__(
            self,
            task_id: int,
            name: str,
            description: str,
            date_active: datetime,
            created_at: datetime,
            status: str
    ):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.date_active = date_active
        self.created_at = created_at
        self.status = status
