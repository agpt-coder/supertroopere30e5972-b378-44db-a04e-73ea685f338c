from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ContentDetails(BaseModel):
    """
    Structure containing all details necessary for content identification and display.
    """

    title: str
    description: Optional[str] = None
    type: str
    data: str


class UploadContentResponse(BaseModel):
    """
    Response after successfully uploading content into the user's portfolio. It includes a confirmation message and the ID of the newly created or updated content entity.
    """

    success: bool
    message: str
    contentId: int


async def uploadContent(
    userId: int, contentId: int, content: ContentDetails
) -> UploadContentResponse:
    """
    This POST endpoint integrates with the User Portfolio module for uploading newly created or updated content by the contentId into the user's portfolio.
    Available strictly to authenticated Users and Admins.

    Args:
        userId (int): The ID of the user who is uploading the content. Must correspond to an existing user in the User database.
        contentId (int): The unique identifier for the content that is being uploaded. This should match with an existing content entry or be created afresh if it is new.
        content (ContentDetails): Detailed information about the content being uploaded.

    Returns:
        UploadContentResponse: Response after successfully uploading content into the user's portfolio. It includes a confirmation message and the ID of the newly created or updated content entity.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        return UploadContentResponse(
            success=False, message="User not found.", contentId=0
        )
    content_data = {
        "title": content.title,
        "content": content.data,
        "type": prisma.enums.PostType[content.type.upper()],
        "userId": userId,
    }
    if contentId > 0:
        existing_post = await prisma.models.Post.prisma().find_unique(
            where={"id": contentId}
        )
        if not existing_post:
            return UploadContentResponse(
                success=False, message="Content ID not found.", contentId=contentId
            )
        updated_post = await prisma.models.Post.prisma().update(
            where={"id": contentId}, data=content_data
        )
        message = "Content updated successfully."
    else:
        updated_post = await prisma.models.Post.prisma().create(data=content_data)
        message = "Content uploaded successfully."
        contentId = updated_post.id
    return UploadContentResponse(success=True, message=message, contentId=contentId)
