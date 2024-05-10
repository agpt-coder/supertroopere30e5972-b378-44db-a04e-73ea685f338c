from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateProjectResponse(BaseModel):
    """
    Response data for a newly created project which also includes confirmation of notification sent for role assignment.
    """

    projectId: int
    status: str
    roleAssignmentStatus: str


async def createProject(
    name: str, description: Optional[str], userId: int, members: List[int]
) -> CreateProjectResponse:
    """
    Allows the creation of a new project. Users can post project details, which are then saved in the project database. This route also sends a notification to the User Management module to assign default roles to the project.

    Args:
        name (str): The name of the new project.
        description (Optional[str]): An optional description of the project.
        userId (int): The identifier of the user creating the project. This ID will be used to link the project to the user and handle permission settings.
        members (List[int]): A list of member user IDs to be initially added to the project. These may include default roles.

    Returns:
        CreateProjectResponse: Response data for a newly created project which also includes confirmation of notification sent for role assignment.

    Example:
        createProject("Super Trooper Project", "A project for supertrooper creations", 1, [2, 3, 4])
        > {'projectId': 101, 'status': 'success', 'roleAssignmentStatus': 'success'}
    """
    project = await prisma.models.Project.prisma().create(
        data={"name": name, "description": description, "userId": userId}
    )
    for member_id in members:
        await prisma.models.ProjectMember.prisma().create(
            data={
                "projectId": project.id,
                "userId": member_id,
                "role": prisma.enums.ProjectRole.MEMBER,
            }
        )
    await prisma.models.ProjectMember.prisma().create(
        data={
            "projectId": project.id,
            "userId": userId,
            "role": prisma.enums.ProjectRole.OWNER,
        }
    )
    response = CreateProjectResponse(
        projectId=project.id, status="success", roleAssignmentStatus="success"
    )
    return response
