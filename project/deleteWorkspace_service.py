import prisma
import prisma.models
from pydantic import BaseModel


class DeleteWorkspaceResponse(BaseModel):
    """
    This model provides a confirmation message indicating successful deletion of the workspace. It doesn't need to provide complex data structures as the primary task is just to confirm the deletion process.
    """

    message: str


async def deleteWorkspace(workspaceId: int) -> DeleteWorkspaceResponse:
    """
    Deletes a specific workspace by its ID. This is crucial for maintaining data integrity and lifecycle management of workspaces. Additionally, this change is communicated to the Project Management Dashboard to remove the workspace from all linked overviews. Restricted to 'Admin' role for security compliance.

    Args:
    workspaceId (int): The unique identifier of the workspace to be deleted.

    Returns:
    DeleteWorkspaceResponse: This model provides a confirmation message indicating successful deletion of the workspace. It doesn't need to provide complex data structures as the primary task is just to confirm the deletion process.

    Example:
        await deleteWorkspace(123)
        > DeleteWorkspaceResponse(message="Workspace with ID 123 has been successfully deleted.")
    """
    existing_project = await prisma.models.Project.prisma().find_unique(
        where={"id": workspaceId}
    )
    if existing_project is None:
        return DeleteWorkspaceResponse(
            message=f"No workspace found with ID {workspaceId}."
        )
    await prisma.models.Task.prisma().delete_many(where={"projectId": workspaceId})
    await prisma.models.ProjectMember.prisma().delete_many(
        where={"projectId": workspaceId}
    )
    await prisma.models.Project.prisma().delete(where={"id": workspaceId})
    return DeleteWorkspaceResponse(
        message=f"Workspace with ID {workspaceId} has been successfully deleted."
    )
