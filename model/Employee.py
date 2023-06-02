class Employee:
    def __init__(self, employee_id: str, name: str, is_admin: int = 0):
        self.employee_id = employee_id
        self.name = name
        self.is_admin = is_admin
