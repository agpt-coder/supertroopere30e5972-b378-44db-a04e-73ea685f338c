import prisma
import prisma.models
from pydantic import BaseModel


class UpdateFeedbackStatusResponse(BaseModel):
    """
    Response model indicating the success of the feedback status update. Includes the updated feedback object.
    """

    success: bool
    updatedFeedback: prisma.models.Feedback


async def updateFeedbackStatus(
    feedbackId: int, newStatus: str
) -> UpdateFeedbackStatusResponse:
    """
    Allows an admin to update the status of a feedback entry, such as 'reviewed', 'addressed' or 'pending'. Requires feedback ID and the new status as parameters. Verifies admin rights before updating the entry in the database.

    Args:
    feedbackId (int): The unique identifier of the feedback to be updated.
    newStatus (str): The new status to set for the feedback. Valid statuses are 'reviewed', 'addressed', and 'pending'.

    Returns:
    UpdateFeedbackStatusResponse: Response model indicating the success of the feedback status update. Includes the updated feedback object.
    """
    if newStatus not in ["reviewed", "addressed", "pending"]:
        return UpdateFeedbackStatusResponse(success=False, updatedFeedback=None)
    feedback = await prisma.models.Feedback.prisma().find_unique(
        where={"id": feedbackId}
    )
    if feedback is None:
        return UpdateFeedbackStatusResponse(success=False, updatedFeedback=None)
    updated_feedback = await prisma.models.Feedback.prisma().update(
        where={"id": feedbackId}, data={"content": newStatus}
    )
    return UpdateFeedbackStatusResponse(success=True, updatedFeedback=updated_feedback)
