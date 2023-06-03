from datetime import datetime


class EmployeePosition:
    def __init__(
            self,
            id: int,
            employee_id: str,
            position_id: int,
            start_date: datetime,
            end_date: datetime,
            created_at: datetime,
            is_active: int
    ):
        self.id = id
        self.employee_id = employee_id
        self.position_id = position_id
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.is_active = is_active
