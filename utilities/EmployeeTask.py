from datetime import datetime


class EmployeeTask:
    def __init__(
            self,
            task_id: int,
            assigned_to_id: str,
            position_id: int,
            assigned_by_id: str,
            assigned_date: datetime = None
    ):
        self.task_id = task_id
        self.assigned_to_id = assigned_to_id
        self.position_id = position_id
        self.assigned_by_id = assigned_by_id
        self.assigned_date = assigned_date or datetime.now()
