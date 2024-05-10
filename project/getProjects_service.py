from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetProjectsRequest(BaseModel):
    """
    This model represents the GET request for all projects. It does not require input fields as it retrieves all projects without conditions. But, it might include authorization checks based on user roles.
    """

    pass


class TaskDetails(BaseModel):
    """
    Detailed information about a task within a project.
    """

    title: str
    dueDate: datetime
    description: Optional[str] = None


class ProjectDetails(BaseModel):
    """
    Details of a single project along with real-time status updates.
    """

    id: int
    name: str
    status: prisma.enums.ProjectStatus
    tasks: List[TaskDetails]


class GetProjectsResponse(BaseModel):
    """
    This model represents the response returned by the GET /projects endpoint. Each project is returned with essential details and real-time status updates integrated from the Collaborative Workspace module.
    """

    projects: List[ProjectDetails]


class ProjectStatus(BaseModel):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"
    ARCHIVED: str = "ARCHIVED"


async def getProjects(request: GetProjectsRequest) -> GetProjectsResponse:
    """
    Retrieves a list of all projects from the database. Each project includes its tasks and current status.

    Args:
        request (GetProjectsRequest): Contains any user-specific filters or authentication data (unused in this simplified version).

    Returns:
        GetProjectsResponse: a response instance which contains a list of all projects with details.
    """
    projects_query = await prisma.models.Project.prisma().find_many(
        include={"tasks": True}
    )
    projects = []
    for project in projects_query:
        tasks = (
            [
                TaskDetails(
                    title=task.title,
                    dueDate=task.dueDate,
                    description=task.description if task.description else "",
                )
                for task in project.tasks
            ]
            if project.tasks is not None
            else []
        )
        project_details = ProjectDetails(
            id=project.id,
            name=project.name,
            status=prisma.enums.ProjectStatus(project.status),
            tasks=tasks,
        )
        projects.append(project_details)
    response = GetProjectsResponse(projects=projects)
    return response
