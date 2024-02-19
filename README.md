# Task Manager

A web application built with Django for managing tasks and projects.

## Features:

#### User Authentication:
Users can register and create accounts to access the application.
### Task Management:
Users can create, edit, and delete tasks within the application.

### Due Dates:
Users can set due dates for their tasks to help them manage deadlines.
### Task Search:
The application provides a search functionality to allow users to quickly find specific tasks by title or description.
### Task Pagination:
Tasks are displayed in a paginated format, making it easier to navigate through a large number of tasks.

### RESTful API: 
The application includes a RESTful API built with Django REST Framework, which can be useful for integrating with other systems or building a separate frontend.
### No Frontend:
The project currently does not have a dedicated frontend and relies on the Django server-rendered views for the user interface.

## Technologies Used:

      Django,
      PostgreSQL, 
      Django REST Framework
      Docker

## Setup

### Prerequisites

- Python (version 3.9)
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Kris-R-Slavchev/django_task_manager.git

   cd django_task_manager

   python3.9 -m venv env
   source env/bin/activate
   
## Install dependencies

      pip install -r requirements.txt
   

## Set up environment variables

### Create a .env file in the project root directory and add the following environment variables:

      SECRET_KEY=your-secret-key
      DEBUG=True

## Run database migrations
      python manage.py makemigrations
      python manage.py migrate

## Start the development server

      python manage.py runserver
