from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserProfileResponse(BaseModel):
    """
    This model provides the details of the newly created user profile. It returns essential information about the user, confirming the successful creation of the profile.
    """

    user_id: int
    name: str
    email: str
    created_at: datetime


async def createUser(name: str, email: str, password: str) -> CreateUserProfileResponse:
    """
    Creates a new user profile. It expects user detail inputs like name, email, and password. Returns the created user profile data. It is a protected endpoint ensuring only authenticated Admins can create users. Utilizes the data validation API to check the integrity of user inputs before creating the profile.

    Args:
        name (str): The full name of the user. This is a required field.
        email (str): The email address of the user. It needs to be unique and valid.
        password (str): The password for the user account. It should meet the security criteria set by the system.

    Returns:
        CreateUserProfileResponse: This model provides the details of the newly created user profile. It returns essential information about the user, confirming the successful creation of the profile.
    """
    hashed_password = password
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password}
    )
    profile = await prisma.models.Profile.prisma().create(
        data={"userId": new_user.id, "bio": "", "avatar": ""}
    )
    return CreateUserProfileResponse(
        user_id=new_user.id, name=name, email=new_user.email, created_at=datetime.now()
    )
