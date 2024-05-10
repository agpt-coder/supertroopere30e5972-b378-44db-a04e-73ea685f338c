from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class GetWorkspacesRequest(BaseModel):
    """
    As this is a straightforward GET request meant for public dashboards, no specific input parameters are required.
    """

    pass


class Project(BaseModel):
    """
    Projects active in the workspace, detailed with essential project information.
    """

    id: int
    name: str
    status: prisma.enums.ProjectStatus


class GetWorkspacesResponse(BaseModel):
    """
    Provides a list of workspaces with just enough details for a guest or public view. This model will adapt the Project model's basic information without exposing sensitive details.
    """

    workspaces: List[Project]


async def listAllWorkspaces(request: GetWorkspacesRequest) -> GetWorkspacesResponse:
    """
    Provides a list of all available workspaces for the guest view, typically used on public dashboards or information screens. This endpoint is designed with limited details exposure, suitable for unauthenticated or lower access level user engagements.

    Args:
        request (GetWorkspacesRequest): As this is a straightforward GET request meant for public dashboards, no specific input parameters are required.

    Returns:
        GetWorkspacesResponse: Provides a list of workspaces with just enough details for a guest or public view. This model will adapt the Project model's basic information without exposing sensitive details.
    """
    projects = await prisma.models.Project.prisma().find_many(
        where={
            "status": {
                "in": [
                    prisma.enums.ProjectStatus.ACTIVE,
                    prisma.enums.ProjectStatus.INACTIVE,
                ]
            }
        }
    )
    workspace_list = [
        Project(id=project.id, name=project.name, status=project.status)
        for project in projects
    ]
    return GetWorkspacesResponse(workspaces=workspace_list)
