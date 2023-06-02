CREATE TABLE task_tracking.Employee(
    employee_id CHAR(100) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    is_admin SMALLINT
);

CREATE TABLE task_tracking.Position (
    position_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

CREATE TABLE task_tracking.employee_position (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(100) NOT NULL,
    position_id INT NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active SMALLINT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES task_tracking.Employee(employee_id),
    FOREIGN KEY (position_id) REFERENCES task_tracking.Position(position_id)
);

CREATE TABLE task_tracking.Task (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(100),
    date_active DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE task_tracking.employee_task (
    task_id INT,
    assigned_to_id VARCHAR(100) NOT NULL,
    position_id INT NOT NULL,
    assigned_by_id VARCHAR(100) NOT NULL,
    assigned_date DATETIME,
    PRIMARY KEY (task_id, assigned_to_id),
    FOREIGN KEY (task_id) REFERENCES task_tracking.Task(task_id),
    FOREIGN KEY (assigned_to_id) REFERENCES task_tracking.employee_position(employee_id),
    FOREIGN KEY (assigned_by_id) REFERENCES task_tracking.employee_position(employee_id),
    FOREIGN KEY (position_id) REFERENCES task_tracking.employee_position(position_id)
);