from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class TaskDetails(BaseModel):
    """
    Detailed information about a task within a project.
    """

    title: str
    dueDate: datetime
    description: Optional[str] = None


class TaskCreationResponse(BaseModel):
    """
    This model provides feedback on the operation of adding a new task to a project, including the task details with a success message.
    """

    success: bool
    message: str
    task_id: int
    task_details: TaskDetails


async def addTaskToProject(
    project_id: int, description: str, deadline: datetime, assigned_user_id: int
) -> TaskCreationResponse:
    """
    Adds a new task to a project with a specific project ID. It requires task details such as the task description, deadline, and the assigned user's ID from User Management.

    Args:
        project_id (int): The unique identifier for the project to which the task is being added.
        description (str): A brief summary or description of the task being added.
        deadline (datetime): The completion deadline for the task.
        assigned_user_id (int): The ID of the user to whom the task is assigned.

    Returns:
        TaskCreationResponse: This model provides feedback on the operation of adding a new task to a project, including the task details with a success message.
    """
    project = await prisma.models.Project.prisma().find_unique(where={"id": project_id})
    user = await prisma.models.User.prisma().find_unique(where={"id": assigned_user_id})
    if not project or not user:
        return TaskCreationResponse(
            success=False,
            message="Project or User does not exist.",
            task_id=0,
            task_details=TaskDetails(
                title="", dueDate=deadline, description=description
            ),
        )
    new_task = await prisma.models.Task.prisma().create(
        data={
            "title": description[:255],
            "description": description,
            "dueDate": deadline,
            "projectId": project_id,
        }
    )
    if not new_task:
        return TaskCreationResponse(
            success=False,
            message="Failed to create a task.",
            task_id=0,
            task_details=TaskDetails(
                title=description[:255], dueDate=deadline, description=description
            ),
        )
    return TaskCreationResponse(
        success=True,
        message="Task successfully added to the project.",
        task_id=new_task.id,
        task_details=TaskDetails(
            title=description[:255], dueDate=deadline, description=description
        ),
    )
