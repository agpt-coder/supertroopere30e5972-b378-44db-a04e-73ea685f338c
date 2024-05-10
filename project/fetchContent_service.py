from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class ContentDataResponse(BaseModel):
    """
    Response model structured to provide comprehensive details of the multimedia content, including metadata and necessary security measures.
    """

    id: int
    title: str
    content: str
    type: str
    createdAt: datetime
    userId: int


async def fetchContent(contentId: int) -> ContentDataResponse:
    """
    Capable of fetching the requested content by contentId for Users and Guests. The route delivers specific content data secured against unauthorized edits, returning the content and its metadata.

    Args:
        contentId (int): Unique identifier for the multimedia content, utilized to retrieve specific content details.

    Returns:
        ContentDataResponse: Response model structured to provide comprehensive details of the multimedia content, including metadata and necessary security measures.

    Example:
        content = await fetchContent(1)
        print(content)
        > ContentDataResponse(id=1, title="Sunset", content="{'url': 'https://example.com/image.jpg'}", type="IMAGE", createdAt=datetime(2023, 1, 12, 15, 34), userId=42)
    """
    post = await prisma.models.Post.prisma().find_unique(where={"id": contentId})
    if not post:
        raise ValueError("Content not found with the given ID.")
    return ContentDataResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        type=post.type.name,
        createdAt=post.createdAt,
        userId=post.userId,
    )
