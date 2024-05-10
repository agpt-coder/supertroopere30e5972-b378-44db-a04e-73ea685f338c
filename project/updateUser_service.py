from typing import List, Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    This response confirms successful updates. It will return the updated user profile and pertinent user information.
    """

    success: bool
    userId: int
    updatedFields: List[str]


async def updateUser(
    userId: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    bio: Optional[str] = None,
    avatar: Optional[str] = None,
) -> UpdateUserProfileResponse:
    """
    Updates user profile information. Accepts partial data like name or password changes. Ensures changes are validated using the security API before applying updates. It is a protected route allowing only the user or an Admin to make updates.

    Args:
        userId (int): The unique identifier for the user to update. Requires Admin rights or ownership of the user account to effect changes.
        name (Optional[str]): New full name of the user, if they decide to update it.
        email (Optional[str]): Updated email address of the user.
        password (Optional[str]): New password for the user account. This will go through encryption before storage.
        bio (Optional[str]): Updated biography of the user, which is part of the profile.
        avatar (Optional[str]): Direct link to the new avatar image.

    Returns:
        UpdateUserProfileResponse: This response confirms successful updates. It will return the updated user profile and pertinent user information.
    """
    updated_fields = []
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"profile": True}
    )
    if not user:
        return UpdateUserProfileResponse(
            success=False, userId=userId, updatedFields=updated_fields
        )
    update_user_data = {}
    update_profile_data = {}
    if email and user.email != email:
        update_user_data["email"] = email
        updated_fields.append("email")
    if password:
        encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        update_user_data["password"] = encrypted_password
        updated_fields.append("password")
    if update_user_data:
        await prisma.models.User.prisma().update(
            where={"id": userId}, data=update_user_data
        )
    if user.profile:
        if bio:
            update_profile_data["bio"] = bio
            updated_fields.append("bio")
        if avatar:
            update_profile_data["avatar"] = avatar
            updated_fields.append("avatar")
        if update_profile_data:
            await prisma.models.Profile.prisma().update(
                where={"userId": userId}, data=update_profile_data
            )
    return UpdateUserProfileResponse(
        success=True, userId=userId, updatedFields=updated_fields
    )
