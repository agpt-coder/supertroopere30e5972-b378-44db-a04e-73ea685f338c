from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserDetail(BaseModel):
    """
    Describes basic details of a user, used in the context of feedback response to identify the submitter.
    """

    userId: int
    email: str
    avatar: Optional[str] = None


class FeedbackDetailResponse(BaseModel):
    """
    Represents detailed information about a specific feedback, including associated user details and feedback content.
    """

    id: int
    content: str
    createdAt: datetime
    userDetails: UserDetail


async def getFeedback(feedbackId: int) -> FeedbackDetailResponse:
    """
    Fetches details of a specific feedback entry. Requires the feedback ID as a path parameter. This endpoint will retrieve the feedback detail from the database including user details, feedback content, and timestamp. Intended primarily for admin use to monitor or review feedback.

    Args:
        feedbackId (int): The unique identifier of the feedback entry to fetch.

    Returns:
        FeedbackDetailResponse: Represents detailed information about a specific feedback, including associated user details and feedback content.

    Example:
        feedback_detail = await getFeedback(1)
        > FeedbackDetailResponse(id=1, content="Great service!", createdAt=datetime.datetime(...), userDetails=UserDetail(userId=10, email='user@example.com', avatar='http://example.com/avatar.png'))
    """
    feedback = await prisma.models.Feedback.prisma().find_unique(
        where={"id": feedbackId}, include={"user": {"include": {"profile": True}}}
    )
    if not feedback or not feedback.user:
        raise ValueError("Feedback not found or lacks associated user details")
    user_detail = UserDetail(
        userId=feedback.user.id,
        email=feedback.user.email,
        avatar=feedback.user.profile.avatar if feedback.user.profile else None,
    )
    feedback_response = FeedbackDetailResponse(
        id=feedback.id,
        content=feedback.content,
        createdAt=feedback.createdAt,
        userDetails=user_detail,
    )
    return feedback_response
