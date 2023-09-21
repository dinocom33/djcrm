# DJCRM (Django CRM)

The Basic CRM Application is a simple Customer Relationship Management (CRM) system designed for managing organizations, teams, agents, leads, and customers. It provides a user-friendly interface for efficiently organizing and handling customer-related data. 
It is built with Django, Tailwind CSS and PostgreSQL.
### still in progress...

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Creating a Superuser](#creating-a-superuser)
- [Usage](#usage)
- [User Roles](#user-roles)
- [License](#license)
- [Snapshots](#snapshots)

## Features

- Organize data into distinct organizations.
- User management with different roles.
- Create teams within organizations.
- Manage agents, leads, and customers.
- Fine-grained access control for user roles.
- Team-based access for agents.

## Getting Started

### Installation

Follow these steps to set up the Basic CRM Application:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/dinocom33/djcrm.git

2. Navigate to the project directory:

   ```bash
   cd djcrm

3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt

### Creating a Superuser

To manage the application and its data, you should create a superuser with full admin rights:

1. Run the following command:

   ```bash
   python manage.py createsuperuser

During superuser creation, an organization named "Super Admin" and a team named "Admins" are automatically created and the superuser is automatically added to them.

2. Follow the prompts to set a username, email, and password for the superuser account.

### Usage

Once the application is set up and you have created a superuser, you can start using the DJCRM Application:

 1. Start the development server:

    ```bash
    python manage.py runserver
2. Access the admin panel by navigating to http://localhost:8000/admin/ in your web browser.
3. Log in using the superuser credentials created earlier.
4. You can now view, create and edit organizations, teams, agents, leads, and customers, and manage them through the admin panel.

### User Roles

The application includes the following user roles:

 Superuser: Has full rights in the admin panel, including creating organizations.
 
 Organization Owner: Can create teams, agents, leads, and customers within an organization. Has full rights to manage leads and customers created by agents.
 
 Agent: Can view all leads and agents from their team. Has rights to change/delete only their own data.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
