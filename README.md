# DJCRM (Django CRM)

The Basic CRM Application is a simple Customer Relationship Management (CRM) system designed for managing organizations, teams, agents, leads, and clients. It provides a user-friendly interface for efficiently organizing and handling customer-related data. 
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
- [Screenshots](#screenshots)

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

**IMPORTANT** - Do not forget to install Tailwind CSS following the instructions provided in the official site.

***

### Creating a Superuser

To manage the application and its data, you should create a superuser with full admin rights:

1. Run the following command:

   ```bash
   python manage.py createsuperuser

2. Follow the prompts to set a email(as username) and password for the superuser account.
   
During superuser creation, an organization named "Super Admin" and a team named "Admins" are automatically created and the superuser is automatically added to them.

***

### Usage

Once the application is set up and you have created a superuser, you can start using the DJCRM Application:

 1. Start the development server:

    ```bash
    python manage.py runserver
2. Access the admin panel by navigating to http://localhost:8000/ in your web browser.
4. Log in using the superuser credentials created earlier.
5. You can now view, create and edit organizations, teams, agents, leads, and customers, and manage them.

***

### User Roles

The application includes the following user roles:

 **Superuser**: Has full rights in the admin panel, including creating organizations. Go to "Add org owner" to create an Organization, Team and Organization Owner. When the organization owner is created, an email is automatically sent to the email you entered when creating it. It contains a link to reset the password that was automatically generated during organization owner creation.
 
 **Organization Owner**: Can create teams, agents, leads, and clients within an organization. Has full rights to manage leads and customers created by agents. Go to "Teams" to view all created teams(if any). Go to "Add Team" to create a new team. It will automatically added to the organization you belong to. <br>
 
 **Each organization owner has access to the Django admin panel, but could only see and edit objects from their own organization and no other.**

 **Agent**: Can view all leads and agents from their team. Has rights to change/delete only their own data.

***

### License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### Screenshots

soon...
