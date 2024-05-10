from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteContentResponse(BaseModel):
    """
    Confirms the success of the content deletion operation.
    """

    success: bool
    message: Optional[str] = None


async def deleteContent(contentId: int) -> DeleteContentResponse:
    """
    The DELETE endpoint allows the deletion of content by contentId for Admins and authority-holding Users.
    Upon successful deletion, confirms the action with a success response.

    Args:
        contentId (int): The unique identifier of the content to be deleted, provided through the URL path.

    Returns:
        DeleteContentResponse: Confirms the success of the content deletion operation with an indicator flag.
    """
    post = await prisma.models.Post.prisma().delete(where={"id": contentId})
    if post:
        return DeleteContentResponse(
            success=True,
            message=f"Content with ID {contentId} was successfully deleted.",
        )
    else:
        return DeleteContentResponse(
            success=False,
            message="Content not found or you do not have the right permissions.",
        )
