from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Profile(BaseModel):
    """
    Profile sub-type in the User model.
    """

    bio: str
    avatar: str


class QueryUsersResponse(BaseModel):
    """
    Responds with a list of user profiles, each encapsulated with user's diverse details like role and status.
    """

    profiles: List[Profile]


async def listUsers(role: Optional[str], status: Optional[str]) -> QueryUsersResponse:
    """
    Lists all user profiles or filters them based on query parameters such as role or status. Useful for Admins to manage and overview all platform users. This route is protected and only accessible by Admins.

    Args:
        role (Optional[str]): Role of the users to filter the list by. Optional parameter.
        status (Optional[str]): Status to filter the users by. This can be active, inactive, etc. Optional parameter

    Returns:
        QueryUsersResponse: Responds with a list of user profiles, each encapsulated with user's diverse details like role and status.

    Example:
        # Assuming the filtering by role and/or status
        listUsers(role="ADMIN", status="ACTIVE")

        # Response could be a QueryUsersResponse object with a list of filtered profiles or an empty list.
    """
    query_conditions = {}
    if role:
        query_conditions["role"] = role
    if status:
        query_conditions["projects"] = {"some": {"status": status}}
    users = await prisma.models.User.prisma().find_many(
        where=query_conditions, include={"profile": True, "projects": True}
    )
    profiles = [
        Profile(bio=user.profile.bio, avatar=user.profile.avatar)
        for user in users
        if user.profile
    ]
    return QueryUsersResponse(profiles=profiles)
