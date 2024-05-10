from datetime import datetime
from enum import Enum
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Project(BaseModel):
    """
    Projects active in the workspace, detailed with essential project information.
    """

    id: int
    name: str
    status: prisma.enums.ProjectStatus


class ProjectUpdateResponse(BaseModel):
    """
    Response model for updating a project. Contains confirmation of the update and the updated project details.
    """

    success: bool
    project: Project


class ProjectStatus(Enum):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"
    ARCHIVED: str = "ARCHIVED"


async def updateProject(
    id: int, name: str, description: Optional[str], deadline: Optional[datetime]
) -> ProjectUpdateResponse:
    """
    Updates project details for a specific project ID. Authorized users can modify project parameters such as name, description, deadlines, etc. Changes are synchronized with the Collaborative Workspace module to reflect updates in real-time.

    Args:
        id (int): The unique identifier of the project to be updated.
        name (str): The new name to update the project with.
        description (Optional[str]): New description outlining the project's purpose and scope.
        deadline (Optional[datetime]): The revised completion deadline for the project.

    Returns:
        ProjectUpdateResponse: Response model for updating a project. Contains confirmation of the update and the updated project details.
    """
    update_data = {"name": name}
    if description is not None:
        update_data["description"] = description
    if deadline:
        update_data["deadline"] = deadline
    db_project = await prisma.models.Project.prisma().update(
        where={"id": id}, data=update_data, include={"tasks": True}
    )
    if db_project:
        project_model = Project(
            id=db_project.id, name=db_project.name, status=db_project.status
        )
        return ProjectUpdateResponse(success=True, project=project_model)
    else:
        return ProjectUpdateResponse(success=False, project=None)
