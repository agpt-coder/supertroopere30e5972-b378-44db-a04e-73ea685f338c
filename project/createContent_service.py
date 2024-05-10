from typing import Dict

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateContentResponse(BaseModel):
    """
    Response Model for the POST /content/create endpoint that returns information about the newly created content.
    """

    success: bool
    message: str
    contentId: int


async def createContent(
    userId: int, title: str, content: Dict, type: str
) -> CreateContentResponse:
    """
    This POST endpoint allows authenticated users to create new multimedia content. It checks user credentials via User Management module and returns a content ID if successful. Only verified Admins and Users can create content.

    Args:
        userId (int): Unique identifier for the user initiating the content creation.
        title (str): Title of the multimedia content being created.
        content (Dict): Actual multimedia content in a JSON format, which could be a text, image, or video content.
        type (str): Type of the content being posted, must be one of the predefined types in the PostType enum.

    Returns:
        CreateContentResponse: Response Model for the POST /content/create endpoint that returns information about the newly created content.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user or user.role not in [prisma.enums.Role.ADMIN, prisma.enums.Role.USER]:
        return CreateContentResponse(
            success=False, message="Unauthorized or user not found", contentId=-1
        )
    try:
        post = await prisma.models.Post.prisma().create(
            data={
                "userId": userId,
                "title": title,
                "content": content,
                "type": prisma.enums.PostType[type],
            }
        )
        return CreateContentResponse(
            success=True, message="Content created successfully", contentId=post.id
        )
    except Exception as e:
        return CreateContentResponse(success=False, message=str(e), contentId=-1)
