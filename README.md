# Task Manager

A web application built with Django for managing tasks and projects.

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
