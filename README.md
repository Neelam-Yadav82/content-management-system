# content-management-system
# Step 1: Clone the Project (if not already done)
### If the Django project is not already on your local machine, clone it from the repository where it's hosted using Git:

#### git clone <repository_url>
#### Replace <repository_url> with the actual URL of your project repository.

# Step 2: Navigate to Project Directory
### Navigate into the project directory:

    1.cd <project_name>
    2.Replace <project_name> with the name of your Django project directory.

# Step 3: Create and Activate Virtual Environment (Optional but Recommended)
### If you prefer using a virtual environment, create and activate it using:
    1.python -m venv env

# Replace myenv with your preferred name for the virtual environment.
#### Activate the virtual environment:
    1.On macOS/Linux:source myenv/bin/activate
    2.On Windows:myenv\Scripts\activate

# Step 4: Install Project Dependencies
### Install the project dependencies listed in the requirements.txt file using pip:
    1.pip install -r requirements.txt
This command will install all the required packages specified in the requirements.txt file.


# Step 5: Run Migrations
### Apply database migrations to create necessary database tables: 
    1.python manage.py makemigration
    2.python manage.py migrate

# Step-6: Seeding Roles
### To seed roles in the database, run the following Django management command:
    1.python manage.py seed_roles_and_tabs

# Step 7: Create a Superuser (Optional)
### If you need to access the Django admin interface, create a superuser: 
    1.python manage.py  createsuperuser
#### Follow the prompts to set a username, email, and password.

# Step 8: Run the Development Server
### Start the Django development server: 
    1.python manage.py runserver

#### Visit http://localhost:8000 in your web browser to see your Django project running.
