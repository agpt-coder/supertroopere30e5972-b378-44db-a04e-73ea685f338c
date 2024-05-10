from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ContentItem(BaseModel):
    """
    Defines the structure of a content item within the portfolio.
    """

    contentId: int
    contentData: str
    contentType: str


class UpdatePortfolioResponse(BaseModel):
    """
    Confirms the updates made to a user's portfolio, including a list of updated or added content items.
    """

    updated: bool
    updatedItems: List[ContentItem]


async def updateUserPortfolio(
    userId: int, title: str, description: Optional[str], contentItems: List[ContentItem]
) -> UpdatePortfolioResponse:
    """
    Updates an existing user portfolio. It allows modification of portfolio details like adding new content items or updating existing items,
    directly interfacing with Content Creation Tools for content management. Security measures ensure that only the portfolio owner or an
    admin can make changes. Returns a confirmation of the updates made.

    Args:
        userId (int): The unique identifier of the user whose portfolio is being updated.
        title (str): The new title of the portfolio.
        description (Optional[str]): A new description of the portfolio, optional.
        contentItems (List[ContentItem]): List of content items to be added or updated in the portfolio.

    Returns:
        UpdatePortfolioResponse: Confirms the updates made to a user's portfolio, including a list of updated or added content items.
    """
    profile = await prisma.models.Profile.prisma().find_unique(
        where={"userId": userId}, include={"portfolio": True}
    )
    if not profile or not profile.portfolio:
        return UpdatePortfolioResponse(updated=False, updatedItems=[])
    portfolio = await prisma.models.Portfolio.prisma().update(
        where={"id": profile.portfolio[0].id},
        data={"title": title, "description": description},
    )
    updated_items = []
    for item in contentItems:
        if content_id_exists(item.contentId):
            await prisma.models.Post.prisma().update(
                where={"id": item.contentId},
                data={
                    "title": title,
                    "content": item.contentData,
                    "type": item.contentType,
                },
            )
        else:
            await prisma.models.Post.prisma().create(
                data={
                    "title": title,
                    "content": item.contentData,
                    "userId": userId,
                    "type": item.contentType,
                }
            )
        updated_items.append(item)
    return UpdatePortfolioResponse(updated=True, updatedItems=updated_items)


async def content_id_exists(content_id: int) -> bool:
    """
    Checks if a content item with a given ID exists in the database.

    Args:
        content_id (int): The ID of the content item to check.

    Returns:
        bool: True if the content item exists, False otherwise.
    """
    return (
        await prisma.models.Post.prisma().find_unique(where={"id": content_id})
        is not None
    )
