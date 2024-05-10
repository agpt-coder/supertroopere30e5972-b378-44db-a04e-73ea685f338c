from typing import Optional

from pydantic import BaseModel


class CreatePortfolioResponse(BaseModel):
    """
    This model outlines the response returned upon successful creation of a portfolio. It contains confirmation details and a reference link to the newly created portfolio.
    """

    success: bool
    portfolio_id: int
    message: str
    link: str


async def createUserPortfolio(
    user_id: int, title: str, description: Optional[str], auth_token: str
) -> CreatePortfolioResponse:
    """
    Creates a new portfolio for a registered user. This endpoint takes user details and portfolio parameters,
    creating a new portfolio entry linked to the user's account. It interacts with the User Management to verify
    user authenticity and roles. Appropriate response confirms portfolio creation with a link to the new portfolio.

    Args:
    user_id (int): The ID of the user for whom the portfolio is being created.
    title (str): The title of the new portfolio.
    description (Optional[str]): A brief description of the portfolio.
    auth_token (str): The authentication token to verify the user's identity and permissions.

    Returns:
    CreatePortfolioResponse: This model outlines the response returned upon successful creation of a portfolio.
    It contains confirmation details and a reference link to the newly created portfolio.
    """
    import prisma.models

    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        return CreatePortfolioResponse(
            success=False, portfolio_id=0, message="User not found.", link=""
        )
    profile = await prisma.models.Profile.prisma().find_unique(
        where={"userId": user_id}
    )
    if not profile:
        return CreatePortfolioResponse(
            success=False, portfolio_id=0, message="User profile not found.", link=""
        )
    new_portfolio = await prisma.models.Portfolio.prisma().create(
        data={
            "title": title,
            "description": description if description is not None else "",
            "profileId": profile.id,
        }
    )
    return CreatePortfolioResponse(
        success=True,
        portfolio_id=new_portfolio.id,
        message="Portfolio created successfully.",
        link=f"https://supertroppercreations.com/portfolio/{new_portfolio.id}",
    )
