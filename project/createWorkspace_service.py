import prisma
import prisma.models
from pydantic import BaseModel


class WorkspaceCreationResponse(BaseModel):
    """
    Response model representing the newly created workspace. It returns the workspace information along with a success message.
    """

    workspaceId: int
    workspaceName: str
    workspaceDescription: str
    creationStatus: str


async def createWorkspace(
    userId: int, workspaceName: str, workspaceDescription: str
) -> WorkspaceCreationResponse:
    """
    Allows an authorized user to create a new collaborative workspace. The function also notifies the prisma.models.Project Management Dashboard to add this new workspace to the user's list. Performs user validation to check if the user has 'Admin' privileges.

    Args:
        userId (int): ID of the user creating the workspace. This is used to validate if the user has admin rights.
        workspaceName (str): The name of the new workspace to be created.
        workspaceDescription (str): A brief description of the workspace to be created.

    Returns:
        WorkspaceCreationResponse: Response model representing the newly created workspace. It returns the workspace information along with a success message.

    Example:
        response = createWorkspace(1, "Dev Team Workspace", "A workspace for development team collaborations")
        print(response)
        > { 'workspaceId': 101, 'workspaceName': 'Dev Team Workspace', 'workspaceDescription': 'A workspace for development team collaborations', 'creationStatus': 'Workspace created successfully!' }
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"projects": False}
    )
    if user is None or user.role != "ADMIN":
        return WorkspaceCreationResponse(
            workspaceId=-1,
            workspaceName="",
            workspaceDescription="",
            creationStatus=f"Creation failed. prisma.models.User ID {userId} not authorized or not found.",
        )
    project = await prisma.models.Project.prisma().create(
        data={"name": workspaceName, "status": "ACTIVE", "userId": userId}
    )
    return WorkspaceCreationResponse(
        workspaceId=project.id,
        workspaceName=workspaceName,
        workspaceDescription=workspaceDescription,
        creationStatus="Workspace created successfully!",
    )
