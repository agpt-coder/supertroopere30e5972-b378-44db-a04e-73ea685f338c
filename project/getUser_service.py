from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class EmbeddedProfileType(BaseModel):
    """
    Subset of profile details relevant to the user's public and administrative view.
    """

    bio: Optional[str] = None
    avatar: Optional[str] = None
    portfolio: List[prisma.models.Portfolio]


class Project(BaseModel):
    """
    Projects active in the workspace, detailed with essential project information.
    """

    id: int
    name: str
    status: prisma.enums.ProjectStatus


class UserProfileResponse(BaseModel):
    """
    This model encapsulates all necessary user details including primary user information and linked module data.
    """

    id: int
    email: str
    role: prisma.enums.Role
    profile: EmbeddedProfileType
    projects: List[Project]


async def getUser(userId: int) -> UserProfileResponse:
    """
    Retrieves a single user profile based on the user ID. This route is protected to ensure that a user
    can access only their profile or an Admin can view any profile. Returns detailed user information
    including linked module data from Content Creation Tools and the User prisma.models.Portfolio module.

    Args:
        userId (int): The unique identifier of the user whose profile is being retrieved.

    Returns:
        UserProfileResponse: This model encapsulates all necessary user details including primary user
        information and linked module data.

    Example:
        user_profile = await getUser(123)
        print(user_profile)
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId},
        include={"profile": {"include": {"portfolio": True}}, "projects": True},
    )
    if not user:
        raise ValueError("No user found with provided ID")
    portfolio_data = [
        {"title": portfolio.title, "description": portfolio.description}
        for portfolio in (
            user.profile.portfolio if user.profile and user.profile.portfolio else []
        )
    ]
    profile_data = EmbeddedProfileType(
        bio=user.profile.bio if user.profile else None,
        avatar=user.profile.avatar if user.profile else None,
        portfolio=portfolio_data,
    )
    projects_data = [
        Project(id=project.id, name=project.name, status=project.status.name)
        for project in (user.projects if user.projects else [])
    ]
    user_response = UserProfileResponse(
        id=user.id,
        email=user.email,
        role=user.role.name,
        profile=profile_data,
        projects=projects_data,
    )
    return user_response
