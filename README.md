# task_tracking
Task tracking system for managing employee positions and assignments.

## Database
![Entity relationship diagram](images/ERD.png)

The most important thing to emphasize in the database model 
is that the relationship between employee and position is many-to-many. 
Therefore, I have a third table called 'employee_position'. 
The reason for this is that an employee can have multiple non-overlapping positions. Additionally, a position can belong to multiple employees at the same time.

For the relationship between Task and Employee, I chose to connect them again through a third table. 
This is because it is natural for an employee to have multiple tasks at the same time. Additionally, I wanted to make it possible that a task can be assignable to none or many employees.