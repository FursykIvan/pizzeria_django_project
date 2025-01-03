# Pizzeria Restaurant

A Django-based web application for managing pizzas, type of pizzas, and pizzaiolos in a pizzeria restaurant.

[Website link](https://pizzeria-django-project.onrender.com)

## Features

### User Authentication System
- Custom user model (`Pizzaiolo`) with experience tracking
- User registration and login
- Profile management

### Pizza Management
- Create, update, and delete pizzas
- Categorize pizzas by types
- Search functionality for pizzas and pizza types
- Price management for pizzas

### Cook Management
- Track pizzaiolos experience
- Associate pizzaiolo with pizzas
- View pizzaiolo profiles and their specialties

## Technologies
- Python 3.x
- Django 5.1.3
- Bootstrap 4
- Crispy Forms
- SQLite3

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/FursykIvan/pizzeria_django_project.git
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  
    On Windows: venv\Scripts\activate
    ```

3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Project Structure
- `accounts/` - Custom pizzaiolo management app
- `kitchen/` - Main app for pizza and types of pizzas
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)

## Usage
- Register as a new pizzaiolo or login with existing credentials
- Create pizza types to categorize your pizzas
- Add new pizzas with descriptions and prices
- Assign pizzas to pizzaiolos
- Browse and search through the pizza and pizza types

## Admin Interface
Access the admin interface at `/admin` to manage:
- Users (Pizzaiolos)
- Pizzas
- Pizza Types

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
