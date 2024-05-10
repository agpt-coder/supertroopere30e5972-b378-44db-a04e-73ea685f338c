import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import prisma
import prisma.enums
import project.addTaskToProject_service
import project.authenticateUser_service
import project.createContent_service
import project.createProject_service
import project.createUser_service
import project.createUserPortfolio_service
import project.createWorkspace_service
import project.deleteContent_service
import project.deleteFeedback_service
import project.deleteProject_service
import project.deleteUser_service
import project.deleteUserPortfolio_service
import project.deleteWorkspace_service
import project.fetchContent_service
import project.getFeedback_service
import project.getProject_service
import project.getProjects_service
import project.getProjectTasks_service
import project.getUser_service
import project.getUserPortfolio_service
import project.getWorkspaceDetails_service
import project.listAllWorkspaces_service
import project.listFeedback_service
import project.listUsers_service
import project.publicProjectInfo_service
import project.submitFeedback_service
import project.updateContent_service
import project.updateFeedbackStatus_service
import project.updateProject_service
import project.updateUser_service
import project.updateUserPortfolio_service
import project.updateWorkspace_service
import project.uploadContent_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="supertrooper",
    lifespan=lifespan,
    description="a prject for supertropper createions",
)


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponseModel
)
async def api_delete_deleteUser(
    userId: str,
) -> project.deleteUser_service.DeleteUserResponseModel | Response:
    """
    Deletes a user profile based on the user ID. This action is heavily guarded and only an Admin can execute deletion. The function performs data cleanup across dependent modules like Project Management and User Portfolio to maintain data integrity.
    """
    try:
        res = project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/portfolios/{userId}",
    response_model=project.deleteUserPortfolio_service.DeletePortfolioResponse,
)
async def api_delete_deleteUserPortfolio(
    userId: int,
) -> project.deleteUserPortfolio_service.DeletePortfolioResponse | Response:
    """
    Deletes a user's portfolio. This action removes all portfolio content and its details from the database securely. Access is strictly limited to ensure that only the user themselves or an admin can delete the portfolio. A successful deletion will confirm the removal of the portfolio.
    """
    try:
        res = await project.deleteUserPortfolio_service.deleteUserPortfolio(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/content/delete/{contentId}",
    response_model=project.deleteContent_service.DeleteContentResponse,
)
async def api_delete_deleteContent(
    contentId: int,
) -> project.deleteContent_service.DeleteContentResponse | Response:
    """
    The DELETE endpoint allows the deletion of content by contentId for Admins and authority-holding Users. Upon successful deletion, confirms the action with a success response.
    """
    try:
        res = await project.deleteContent_service.deleteContent(contentId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/workspace",
    response_model=project.createWorkspace_service.WorkspaceCreationResponse,
)
async def api_post_createWorkspace(
    userId: int, workspaceName: str, workspaceDescription: str
) -> project.createWorkspace_service.WorkspaceCreationResponse | Response:
    """
    Allows an authorized user to create a new collaborative workspace. The function also notifies the Project Management Dashboard to add this new workspace to the user's list. Performs user validation to check if the user has 'Admin' privileges.
    """
    try:
        res = await project.createWorkspace_service.createWorkspace(
            userId, workspaceName, workspaceDescription
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/authenticate",
    response_model=project.authenticateUser_service.AuthenticateUserResponse,
)
async def api_post_authenticateUser(
    email: str, password: str
) -> project.authenticateUser_service.AuthenticateUserResponse | Response:
    """
    Handles user authentication. Accepts credentials, verifies them against the stored user data, and returns authentication status along with a session token. This action is public to allow Guest and User roles to authenticate.
    """
    try:
        res = project.authenticateUser_service.authenticateUser(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback", response_model=project.submitFeedback_service.PostFeedbackResponse
)
async def api_post_submitFeedback(
    userId: int, postId: int, content: str
) -> project.submitFeedback_service.PostFeedbackResponse | Response:
    """
    Allows users to submit feedback on the content. Users need to provide their user ID (which will be checked against the User Management module to verify privileges) and feedback details. The API will save this information in the feedback database, linking it to the respective content and user profile if applicable. A successful operation will return a confirmation message and a status code of 201.
    """
    try:
        res = project.submitFeedback_service.submitFeedback(userId, postId, content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/workspace/{workspaceId}",
    response_model=project.updateWorkspace_service.UpdateWorkspaceResponse,
)
async def api_put_updateWorkspace(
    workspaceId: int,
    projectName: Optional[str],
    projectStatus: prisma.enums.ProjectStatus,
    description: Optional[str],
) -> project.updateWorkspace_service.UpdateWorkspaceResponse | Response:
    """
    Updates the settings or details of an existing workspace identified by the workspace ID. Access is secured to ensure only authorized 'Admin' roles can perform updates. It also integrates real-time updates to the Project Management Dashboard.
    """
    try:
        res = project.updateWorkspace_service.updateWorkspace(
            workspaceId, projectName, projectStatus, description
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/feedback/{feedbackId}",
    response_model=project.deleteFeedback_service.DeleteFeedbackResponse,
)
async def api_delete_deleteFeedback(
    feedbackId: int,
) -> project.deleteFeedback_service.DeleteFeedbackResponse | Response:
    """
    Permits an admin to delete a feedback entry. The endpoint requires the feedback ID as a path parameter. It will verify if the requester has admin rights before allowing the deletion from the database. This operation will provide a success or failure status code accordingly.
    """
    try:
        res = await project.deleteFeedback_service.deleteFeedback(feedbackId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/projects/{id}", response_model=project.deleteProject_service.DeleteProjectResponse
)
async def api_delete_deleteProject(
    id: int, admin_user_id: int
) -> project.deleteProject_service.DeleteProjectResponse | Response:
    """
    Deletes a project by ID. This route removes the project from the database and also updates the User Management module to reassign or deactivate users associated with this project.
    """
    try:
        res = await project.deleteProject_service.deleteProject(id, admin_user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/portfolios/{userId}",
    response_model=project.getUserPortfolio_service.UserPortfolioOutput,
)
async def api_get_getUserPortfolio(
    userId: int,
) -> project.getUserPortfolio_service.UserPortfolioOutput | Response:
    """
    Retrieves the portfolio of a specific user. The response includes all content from the user's portfolio, sourced through integration with the Content Creation Tools module. Returns a detailed user portfolio if the specific user ID exists. Suitable for display purposes where any visitor (guest included) can view a user's public portfolio information.
    """
    try:
        res = await project.getUserPortfolio_service.getUserPortfolio(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/projects/{id}/tasks",
    response_model=project.getProjectTasks_service.ProjectTasksResponse,
)
async def api_get_getProjectTasks(
    id: int, role: prisma.enums.Role
) -> project.getProjectTasks_service.ProjectTasksResponse | Response:
    """
    Retrieves all tasks for a specified project. This queries the internal task management system specific to the project's ID and integrates with the User Management to ensure only assigned roles can view their respective tasks.
    """
    try:
        res = await project.getProjectTasks_service.getProjectTasks(id, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/content/update/{contentId}",
    response_model=project.updateContent_service.ContentUpdateResponse,
)
async def api_put_updateContent(
    contentId: str,
    title: str,
    content: Dict[str, Any],
    type: project.updateContent_service.PostType,
) -> project.updateContent_service.ContentUpdateResponse | Response:
    """
    This PUT endpoint enables Admins or the owning User to update existing content specified by contentId. It validates permissions and updates content details stored in the database, returning success or error messages.
    """
    try:
        res = project.updateContent_service.updateContent(
            contentId, title, content, type
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/content/create",
    response_model=project.createContent_service.CreateContentResponse,
)
async def api_post_createContent(
    userId: int, title: str, content: Dict, type: str
) -> project.createContent_service.CreateContentResponse | Response:
    """
    This POST endpoint allows authenticated users to create new multimedia content. It checks user credentials via User Management module and returns a content ID if successful. Only verified Admins and Users can create content.
    """
    try:
        res = await project.createContent_service.createContent(
            userId, title, content, type
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/projects/{id}", response_model=project.updateProject_service.ProjectUpdateResponse
)
async def api_put_updateProject(
    id: int, name: str, description: Optional[str], deadline: Optional[datetime]
) -> project.updateProject_service.ProjectUpdateResponse | Response:
    """
    Updates project details for a specific project ID. Authorized users can modify project parameters such as name, description, deadlines, etc. Changes are synchronized with the Collaborative Workspace module to reflect updates in real-time.
    """
    try:
        res = await project.updateProject_service.updateProject(
            id, name, description, deadline
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/public/projects/{id}",
    response_model=project.publicProjectInfo_service.PublicProjectInfoResponse,
)
async def api_get_publicProjectInfo(
    id: int,
) -> project.publicProjectInfo_service.PublicProjectInfoResponse | Response:
    """
    Provides public information about a project targeted for guest users. Includes non-sensitive data like project name, project description, and overall status, ensuring compliance with confidentiality standards.
    """
    try:
        res = await project.publicProjectInfo_service.publicProjectInfo(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/projects/{id}", response_model=project.getProject_service.ProjectDetailsResponse
)
async def api_get_getProject(
    id: int,
) -> project.getProject_service.ProjectDetailsResponse | Response:
    """
    Fetches detailed information for a specific project using the project ID. This route will retrieve detailed data including tasks, allocated team members from the User Management module, and current status from the Collaborative Workspace module.
    """
    try:
        res = project.getProject_service.getProject(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/projects", response_model=project.getProjects_service.GetProjectsResponse)
async def api_get_getProjects(
    request: project.getProjects_service.GetProjectsRequest,
) -> project.getProjects_service.GetProjectsResponse | Response:
    """
    Retrieves a list of all projects. This endpoint queries the database for all project entries, returning them in a formatted JSON response. It integrates with the Collaborative Workspace module to fetch real-time status updates for each project displayed.
    """
    try:
        res = await project.getProjects_service.getProjects(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/projects", response_model=project.createProject_service.CreateProjectResponse
)
async def api_post_createProject(
    name: str, description: Optional[str], userId: int, members: List[int]
) -> project.createProject_service.CreateProjectResponse | Response:
    """
    Allows the creation of a new project. Users can post project details, which are then saved in the project database. This route also sends a notification to the User Management module to assign default roles to the project.
    """
    try:
        res = await project.createProject_service.createProject(
            name, description, userId, members
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.listUsers_service.QueryUsersResponse)
async def api_get_listUsers(
    role: Optional[str], status: Optional[str]
) -> project.listUsers_service.QueryUsersResponse | Response:
    """
    Lists all user profiles or filters them based on query parameters such as role or status. Useful for Admins to manage and overview all platform users. This route is protected and only accessible by Admins.
    """
    try:
        res = await project.listUsers_service.listUsers(role, status)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/projects/{id}/tasks",
    response_model=project.addTaskToProject_service.TaskCreationResponse,
)
async def api_post_addTaskToProject(
    project_id: int, description: str, deadline: datetime, assigned_user_id: int
) -> project.addTaskToProject_service.TaskCreationResponse | Response:
    """
    Adds a new task to a project with specific project ID. It requires task details such as the task description, deadline, and the assigned user's ID from User Management.
    """
    try:
        res = await project.addTaskToProject_service.addTaskToProject(
            project_id, description, deadline, assigned_user_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/content/{contentId}",
    response_model=project.fetchContent_service.ContentDataResponse,
)
async def api_get_fetchContent(
    contentId: int,
) -> project.fetchContent_service.ContentDataResponse | Response:
    """
    Capable of fetching the requested content by contentId for Users and Guests. The route delivers specific content data secured against unauthorized edits, returning the content and its metadata.
    """
    try:
        res = await project.fetchContent_service.fetchContent(contentId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/feedback", response_model=project.listFeedback_service.FeedbackListResponse)
async def api_get_listFeedback(
    user_id: Optional[int], content_id: Optional[int]
) -> project.listFeedback_service.FeedbackListResponse | Response:
    """
    Retrieves a list of feedback entries from users. This endpoint will query the feedback database and return an array of feedback entries. Each entry will contain user details (if available), feedback content, and a timestamp. Feedback can be filtered by user or content ID through query parameters. The response will be formatted as JSON.
    """
    try:
        res = await project.listFeedback_service.listFeedback(user_id, content_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/workspace/{workspaceId}",
    response_model=project.deleteWorkspace_service.DeleteWorkspaceResponse,
)
async def api_delete_deleteWorkspace(
    workspaceId: int,
) -> project.deleteWorkspace_service.DeleteWorkspaceResponse | Response:
    """
    Deletes a specific workspace by its ID. This is crucial for maintaining data integrity and lifecycle management of workspaces. Additionally, this change is communicated to the Project Management Dashboard to remove the workspace from all linked overviews. Restricted to 'Admin' role for security compliance.
    """
    try:
        res = await project.deleteWorkspace_service.deleteWorkspace(workspaceId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/portfolios",
    response_model=project.createUserPortfolio_service.CreatePortfolioResponse,
)
async def api_post_createUserPortfolio(
    user_id: int, title: str, description: Optional[str], auth_token: str
) -> project.createUserPortfolio_service.CreatePortfolioResponse | Response:
    """
    Creates a new portfolio for a registered user. This endpoint takes user details and portfolio parameters, creating a new portfolio entry linked to the user's account. It interacts with the User Management to verify user authenticity and roles. Appropriate response confirms portfolio creation with a link to the new portfolio.
    """
    try:
        res = await project.createUserPortfolio_service.createUserPortfolio(
            user_id, title, description, auth_token
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/feedback/{feedbackId}/status",
    response_model=project.updateFeedbackStatus_service.UpdateFeedbackStatusResponse,
)
async def api_patch_updateFeedbackStatus(
    feedbackId: int, newStatus: str
) -> project.updateFeedbackStatus_service.UpdateFeedbackStatusResponse | Response:
    """
    Allows an admin to update the status of a feedback entry, such as 'reviewed', 'addressed' or 'pending'. Requires feedback ID and the new status as parameters. Verifies admin rights before updating the entry in the database.
    """
    try:
        res = await project.updateFeedbackStatus_service.updateFeedbackStatus(
            feedbackId, newStatus
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/feedback/{feedbackId}",
    response_model=project.getFeedback_service.FeedbackDetailResponse,
)
async def api_get_getFeedback(
    feedbackId: int,
) -> project.getFeedback_service.FeedbackDetailResponse | Response:
    """
    Fetches details of a specific feedback entry. Requires the feedback ID as a path parameter. This endpoint will retrieve the feedback detail from the database including user details, feedback content, and timestamp. Intended primarily for admin use to monitor or review feedback.
    """
    try:
        res = await project.getFeedback_service.getFeedback(feedbackId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/portfolios/{userId}",
    response_model=project.updateUserPortfolio_service.UpdatePortfolioResponse,
)
async def api_put_updateUserPortfolio(
    userId: int,
    title: str,
    description: Optional[str],
    contentItems: List[project.updateUserPortfolio_service.ContentItem],
) -> project.updateUserPortfolio_service.UpdatePortfolioResponse | Response:
    """
    Updates an existing user portfolio. It allows modification of portfolio details like adding new content items or updating existing items, directly interfacing with Content Creation Tools for content management. Security measures ensure that only the portfolio owner or an admin can make changes. Returns a confirmation of the updates made.
    """
    try:
        res = await project.updateUserPortfolio_service.updateUserPortfolio(
            userId, title, description, contentItems
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserProfileResponse)
async def api_post_createUser(
    name: str, email: str, password: str
) -> project.createUser_service.CreateUserProfileResponse | Response:
    """
    Creates a new user profile. It expects user detail inputs like name, email, and password. Returns the created user profile data. It is a protected endpoint ensuring only authenticated Admins can create users. Utilizes the data validation API to check the integrity of user inputs before creating the profile.
    """
    try:
        res = await project.createUser_service.createUser(name, email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/portfolio/upload/{userId}/{contentId}",
    response_model=project.uploadContent_service.UploadContentResponse,
)
async def api_post_uploadContent(
    userId: int, contentId: int, content: project.uploadContent_service.ContentDetails
) -> project.uploadContent_service.UploadContentResponse | Response:
    """
    This POST endpoint integrates with the User Portfolio module for uploading newly created or updated content by the contentId into the user's portfolio. Available strictly to authenticated Users and Admins.
    """
    try:
        res = await project.uploadContent_service.uploadContent(
            userId, contentId, content
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/workspaces",
    response_model=project.listAllWorkspaces_service.GetWorkspacesResponse,
)
async def api_get_listAllWorkspaces(
    request: project.listAllWorkspaces_service.GetWorkspacesRequest,
) -> project.listAllWorkspaces_service.GetWorkspacesResponse | Response:
    """
    Provides a list of all available workspaces for the guest view, typically used on public dashboards or information screens. This endpoint is designed with limited details exposure, suitable for unauthenticated or lower access level user engagements.
    """
    try:
        res = await project.listAllWorkspaces_service.listAllWorkspaces(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}",
    response_model=project.updateUser_service.UpdateUserProfileResponse,
)
async def api_put_updateUser(
    userId: int,
    name: Optional[str],
    email: Optional[str],
    password: Optional[str],
    bio: Optional[str],
    avatar: Optional[str],
) -> project.updateUser_service.UpdateUserProfileResponse | Response:
    """
    Updates user profile information. Accepts partial data like name or password changes. Ensures changes are validated using the security API before applying updates. It is a protected route allowing only the user or an Admin to make updates.
    """
    try:
        res = await project.updateUser_service.updateUser(
            userId, name, email, password, bio, avatar
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/workspace/{workspaceId}",
    response_model=project.getWorkspaceDetails_service.WorkspaceDetailsResponse,
)
async def api_get_getWorkspaceDetails(
    workspaceId: str,
) -> project.getWorkspaceDetails_service.WorkspaceDetailsResponse | Response:
    """
    Retrieves full details of a specific workspace by ID, including all active users and ongoing projects. This information is essential for displaying the comprehensive state of the workspace on the Project Management Dashboard. Access checks through User Management are performed to ensure only authorized users can access the details.
    """
    try:
        res = await project.getWorkspaceDetails_service.getWorkspaceDetails(workspaceId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/{userId}", response_model=project.getUser_service.UserProfileResponse)
async def api_get_getUser(
    userId: int,
) -> project.getUser_service.UserProfileResponse | Response:
    """
    Retrieves a single user profile based on the user ID. This route is protected to ensure that a user can access only their profile or an Admin can view any profile. Returns detailed user information including linked module data from Content Creation Tools and the User Portfolio module.
    """
    try:
        res = await project.getUser_service.getUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
