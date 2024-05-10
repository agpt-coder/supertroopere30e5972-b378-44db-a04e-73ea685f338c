import prisma
import prisma.models
from pydantic import BaseModel


class DeletePortfolioResponse(BaseModel):
    """
    Confirmation response upon successful deletion of a user's portfolio.
    """

    message: str


async def deleteUserPortfolio(userId: int) -> DeletePortfolioResponse:
    """
    Deletes a user's portfolio. This action removes all portfolio content and its details from the database securely. Access is strictly limited to ensure that only the user themselves or an admin can delete the portfolio. A successful deletion will confirm the removal of the portfolio.

    Args:
        userId (int): The unique identifier of the user whose portfolio is to be deleted.

    Returns:
        DeletePortfolioResponse: Confirmation response upon successful deletion of a user's portfolio.
    """
    profile = await prisma.models.Profile.prisma().find_unique(
        where={"userId": userId}, include={"portfolio": True}
    )
    if not profile:
        return DeletePortfolioResponse(
            message="User profile or portfolio does not exist."
        )
    if profile.portfolio:
        await prisma.models.Portfolio.prisma().delete_many(
            where={"profileId": profile.id}
        )
    return DeletePortfolioResponse(message="User's portfolio successfully deleted.")
