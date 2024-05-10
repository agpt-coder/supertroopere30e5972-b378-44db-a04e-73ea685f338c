import prisma
import prisma.models
from pydantic import BaseModel


class PublicProjectInfoResponse(BaseModel):
    """
    Response model for providing public information on a project. It includes basic data such as project name, description, and its current status without revealing sensitive details.
    """

    id: int
    name: str
    description: str
    status: str


async def publicProjectInfo(id: int) -> PublicProjectInfoResponse:
    """
    Provides public information about a project targeted for guest users. Includes non-sensitive data like project name,
    project description, and overall status, ensuring compliance with confidentiality standards.

    Args:
        id (int): The unique identifier of the project for which the public data is requested.

    Returns:
        PublicProjectInfoResponse: Response model for providing public information on a project.
        It includes basic data such as project name, description, and its current status without revealing
        sensitive details.

    Example:
        project_info = await publicProjectInfo(1)
        print(project_info)
        > PublicProjectInfoResponse(id=1, name='Project Alpha', description='Exploration into Alpha sector.', status='ACTIVE')
    """
    project = await prisma.models.Project.prisma().find_unique(
        where={"id": id},
        select={"id": True, "name": True, "description": True, "status": True},
    )  # TODO(autogpt): No parameter named "select". reportCallIssue
    if project is None:
        raise ValueError(f"No project found with ID {id}")
    return PublicProjectInfoResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        status=project.status,
    )
