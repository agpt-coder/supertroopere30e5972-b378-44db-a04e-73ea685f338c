---
date: 2024-05-10T19:29:26.636931
author: AutoGPT <info@agpt.co>
---

# supertrooper

a prject for supertropper createions

**Features**

- **Content Creation Tools** Provides a suite of tools for users to create various types of content such as images, videos, and written material.

- **Collaborative Workspace** Allows multiple users to collaborate on projects in real-time.

- **Project Management Dashboard** Enables the organization of projects with features like task assignments, progress tracking, and deadline reminders.

- **User Portfolio** Allows users to create and display their portfolios showcasing their creations.

- **Feedback Mechanism** Facilitates receiving feedback directly through the platform from other users or public viewers.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'supertrooper'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
