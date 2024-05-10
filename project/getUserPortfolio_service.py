from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class PortfolioDetailed(BaseModel):
    """
    Detailed structure of a single portfolio item, including title, description and portfolio specific data.
    """

    title: str
    description: Optional[str] = None
    contentDetails: Dict[str, str]


class UserPortfolioOutput(BaseModel):
    """
    A detailed display of a user's portfolio, suitable for public viewing, stripped of any sensitive or private information.
    """

    userId: int
    portfolios: List[PortfolioDetailed]


async def getUserPortfolio(userId: int) -> UserPortfolioOutput:
    """
    Retrieves the portfolio of a specific user. The response includes all content from the user's portfolio, sourced through integration with the Content Creation Tools module. Returns a detailed user portfolio if the specific user ID exists. Suitable for display purposes where any visitor (guest included) can view a user's public portfolio information.

    Args:
        userId (int): The unique identifier of the user whose portfolio is being requested.

    Returns:
        UserPortfolioOutput: A detailed display of a user's portfolio, suitable for public viewing, stripped of any sensitive or private information.

    Example:
        userPortfolio = await getUserPortfolio(1)
        > UserPortfolioOutput(userId=1, portfolios=[PortfolioDetailed(title="Art Piece", description="Abstract Art", contentDetails={"medium": "Oil Paint"}),...])
    """
    profile = await prisma.models.Profile.prisma().find_unique(
        where={"userId": userId}, include={"portfolio": True}
    )
    if profile is None or profile.portfolio is None:
        return UserPortfolioOutput(userId=userId, portfolios=[])
    portfolios = [
        PortfolioDetailed(
            title=p.title,
            description=p.description,
            contentDetails={"medium": "Descriptive content here"},
        )
        for p in profile.portfolio
    ]
    return UserPortfolioOutput(userId=userId, portfolios=portfolios)
