from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserDetails(BaseModel):
    """
    User details including username and possibly other relevant user information.
    """

    user_id: int
    username: str
    avatar: Optional[str] = None


class FeedbackDetail(BaseModel):
    """
    Detailed feedback model including user and timestamp information.
    """

    id: int
    user_details: Optional[UserDetails] = None
    content: str
    created_at: datetime


class FeedbackListResponse(BaseModel):
    """
    Response model containing a list of feedback entries, potentially including related user details.
    """

    feedbacks: List[FeedbackDetail]


async def listFeedback(
    user_id: Optional[int], content_id: Optional[int]
) -> FeedbackListResponse:
    """
    Retrieves a list of feedback entries from users. This endpoint will query the feedback database and
    return an array of feedback entries. Each entry will contain user details (if available),
    feedback content, and a timestamp. Feedback can be filtered by user or content ID through
    query parameters. The response will be formatted as JSON.

    Args:
        user_id (Optional[int]): Optional query parameter to filter feedback by specific user.
        content_id (Optional[int]): Optional query parameter to filter feedback by specific content.

    Returns:
        FeedbackListResponse: Response model containing a list of feedback entries, potentially including
                              related user details.
    """
    filters = {}
    if user_id:
        filters["userId"] = user_id
    if content_id:
        filters["postId"] = content_id
    feedbacks = await prisma.models.Feedback.prisma().find_many(
        where=filters, include={"user": {"include": {"profile": True}}}
    )
    feedback_details = []
    for feedback in feedbacks:
        user_detail = None
        if feedback.user:
            user_detail = UserDetails(
                user_id=feedback.user.id,
                username=feedback.user.email,
                avatar=feedback.user.profile.avatar if feedback.user.profile else None,
            )
        feedback_details.append(
            FeedbackDetail(
                id=feedback.id,
                user_details=user_detail,
                content=feedback.content,
                created_at=feedback.createdAt,
            )
        )
    return FeedbackListResponse(feedbacks=feedback_details)
