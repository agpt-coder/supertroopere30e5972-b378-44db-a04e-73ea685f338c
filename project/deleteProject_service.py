import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteProjectResponse(BaseModel):
    """
    Model to confirm the project has been successfully deleted or return an error message.
    """

    success: bool
    message: str


async def deleteProject(id: int, admin_user_id: int) -> DeleteProjectResponse:
    """
    Deletes a project by ID. This route removes the project from the database and also updates the User Management module to reassign or deactivate users associated with this project.

    Args:
        id (int): Unique identifier of the project to be deleted.
        admin_user_id (int): The user ID of the admin making the deletion request. Used for validation purposes.

    Returns:
        DeleteProjectResponse: Model to confirm the project has been successfully deleted or return an error message.

    Example:
        response = deleteProject(1, 101)
        if response.success:
            print("Project deleted successfully.")
        else:
            print(f"Failed to delete project: {response.message}")
    """
    admin_user = await prisma.models.User.prisma().find_unique(
        where={"id": admin_user_id}
    )
    if admin_user is None or admin_user.role != prisma.enums.Role.ADMIN:
        return DeleteProjectResponse(
            success=False, message="User is not authorized to delete projects."
        )
    project = await prisma.models.Project.prisma().find_unique(where={"id": id})
    if project is None:
        return DeleteProjectResponse(success=False, message="Project not found.")
    await prisma.models.ProjectMember.prisma().delete_many(where={"projectId": id})
    await prisma.models.Task.prisma().delete_many(where={"projectId": id})
    await prisma.models.Project.prisma().delete(where={"id": id})
    return DeleteProjectResponse(success=True, message="Project deleted successfully.")
