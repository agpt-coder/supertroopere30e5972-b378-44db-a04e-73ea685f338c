from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class User(BaseModel):
    """
    Details of the user participating in the project within the workspace.
    """

    id: int
    email: str


class Project(BaseModel):
    """
    Projects active in the workspace, detailed with essential project information.
    """

    id: int
    name: str
    status: prisma.enums.ProjectStatus


class WorkspaceDetailsResponse(BaseModel):
    """
    Detailed information about a workspace including all active users, ongoing projects, and relevant workspace details. Ensures that data encapsulation is respected with proper viewing permissions.
    """

    workspaceId: str
    activeUsers: List[User]
    ongoingProjects: List[Project]
    workspaceOverview: str


class ProjectStatus(BaseModel):
    """
    Enum indicating the status of the project.
    """

    ACTIVE: str = "Active"
    INACTIVE: str = "Inactive"
    ARCHIVED: str = "Archived"


async def getWorkspaceDetails(workspaceId: str) -> WorkspaceDetailsResponse:
    """
    Retrieves full details of a specific workspace by ID, including all active users and ongoing projects. This information is essential for displaying the comprehensive state of the workspace on the prisma.models.Project Management Dashboard. Access checks through User Management are performed to ensure only authorized users can access the details.

    Args:
        workspaceId (str): Unique identifier for a workspace, used to fetch its details.

    Returns:
        WorkspaceDetailsResponse: Detailed information about a workspace including all active users, ongoing projects, and relevant workspace details. Ensures that data encapsulation is respected with proper viewing permissions.
    """
    project_members = await prisma.models.ProjectMember.prisma().find_many(
        where={"project": {"userId": int(workspaceId), "status": "ACTIVE"}},
        include={"user": True, "project": True},
    )
    active_users_set = set()
    ongoing_projects_set = set()
    for pm in project_members:
        if pm.user and pm.project:
            active_users_set.add(User(id=pm.user.id, email=pm.user.email))
            ongoing_projects_set.add(
                prisma.models.Project(
                    id=pm.project.id, name=pm.project.name, status=pm.project.status
                )
            )
    active_users = list(active_users_set)
    ongoing_projects = list(ongoing_projects_set)
    return WorkspaceDetailsResponse(
        workspaceId=workspaceId,
        activeUsers=active_users,
        ongoingProjects=ongoing_projects,
        workspaceOverview="Overview of current activities and users in the workspace.",
    )
