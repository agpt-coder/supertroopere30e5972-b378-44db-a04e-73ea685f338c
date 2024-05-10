from datetime import datetime
from enum import Enum
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class ProjectTasksResponse(BaseModel):
    """
    The response includes a list of tasks for the project with control as per the roles defined.
    """

    tasks: List[prisma.models.Task]


class Task(BaseModel):
    """
    Represents a task entity with necessary fields such as title, description, due date, and project ID.
    """

    id: int
    title: str
    description: str
    dueDate: datetime
    projectId: int


class Role(Enum):
    """
    Enum representing different roles that a user can have within the system.
    """

    ADMIN: str = "ADMIN"
    USER: str = "USER"
    GUEST: str = "GUEST"


async def getProjectTasks(id: int, role: Role) -> ProjectTasksResponse:
    """
    Retrieves all tasks for a specified project. This queries the internal task management system
    specific to the project's ID and integrates with the User Management to ensure only assigned
    roles can view their respective tasks.

    Args:
        id (int): The unique identifier of the project to fetch tasks for.
        role (Role): Role of the user, which determines access permissions to the tasks.

    Returns:
        ProjectTasksResponse: The response includes a list of tasks for the project with control as per the roles defined.

    Example:
        - getProjectTasks(1, Role.OWNER)
        - getProjectTasks(2, Role.MEMBER)
    """
    tasks = await prisma.models.Task.prisma().find_many(
        where={
            "project": {"id": id, "members": {"some": {"userId": 1, "role": role.name}}}
        }
    )
    task_list = [
        prisma.models.Task(
            id=task.id,
            title=task.title,
            description=task.description or "",
            dueDate=task.dueDate,
            projectId=task.projectId,
        )
        for task in tasks
    ]
    return ProjectTasksResponse(tasks=task_list)
