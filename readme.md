The backend of the application is built using Django, a high-level Python web framework, and Django Rest Framework, a powerful and flexible toolkit for building Web APIs. Here's a high-level overview of how the backend is structured and built:

1. Models: The Section model is defined in sections/models.py. It represents a section of a book and has fields such as title, author, parent_section, and root. The parent_section field is a foreign key to the Section model itself, allowing for the creation of nested sections. The root field is a boolean field that indicates whether the section is the root section of a book.

2. Views: The views are defined in sections/views.py. They handle the creation, retrieval, and modification of sections. The views use Django Rest Framework's viewsets and serializers to handle HTTP requests and responses. The views also handle user authentication and permissions.

3. Serializers: The serializers are defined in sections/serializers.py. They handle the conversion of complex data types into Python data types that can then be easily rendered into JSON. The serializers are used in the views to serialize the data before sending the HTTP response.

4. URL Configuration: The URL configuration is defined in book_writer/urls.py. It maps URLs to the corresponding views. The URL configuration uses Django's path function to define URL patterns for the API endpoints.

5. Tests: Unit tests are written for all API endpoints to ensure they work as expected. They are defined in sections/tests.py. The tests use Django's built-in testing framework and the APIClient class from Django Rest Framework to send HTTP requests to the API endpoints and assert the responses.

6. Cloud Storage Abstraction: The storage_backend.py file implements a cloud storage abstraction backend. It provides an interface for interacting with cloud storage, such as reading and writing files. The cloud storage abstraction backend is used when creating a new section to store the section content in the cloud storage system.

7. User Authentication: User authentication is implemented using the built-in authentication system of Django Rest Framework. The UserRegistrationLoginTest class in sections/tests.py tests the user registration and login functionality.

8. Running the Server: The Django development server is started using the python manage.py runserver command. This command starts a lightweight and simple server for development purposes.

9. Database: SQLite is used as the database for storing data. Django's Object-Relational Mapping (ORM) system is used to interact with the database. The database schema is defined by the models, and migrations are used to apply changes to the database schema. SQLite is for test pursposes. On production posgresql could be used
 
10. Cloud Storage Optimization: The current implementation of file reading from cloud storage could be optimized. However, for the purpose of this test, this optimization will not be implemented as it could take more time.

11. Cache of sections could be added later, as this would require granular delete when someone else changes a section that is cached.


# Local Setup for Cloud Book Writer Platform

## Backend Setup

1. Ensure Python 3.9 or higher is installed on your machine. You can check this by running `python --version` in your terminal/command prompt.

2. Install Django and other required Python dependencies by navigating to the project directory and running `pip install -r requirements.txt` in your terminal/command prompt.

3. Run `python manage.py migrate` to apply migrations.

4. Run `python manage.py runserver` to start the Django development server. You should be able to see your application running at `http://127.0.0.1:8000/` in your web browser.

5. To run the tests, execute `python manage.py test` in your terminal/command prompt.

6. By default testuser user with password testpass will be created

7. API can be tested at http://127.0.0.1:8000/api/sections
   You need to login with testuser username.

## Frontend Setup

1. Ensure Node.js is installed on your machine. You can check this by running `node --version` in your terminal/command prompt.

2. Install the required JavaScript dependencies by navigating to the project directory and running `npm install` in your terminal/command prompt.

3. Run `npm run dev` to start the Next.js development server. You should be able to see your application running at `http://localhost:3000/` in your web browser.

4. To run the tests, execute `npm test` in your terminal/command prompt.

# API Documentation

User Registration
Endpoint: /register/
Method: POST
Data Parameters: 
{
    "username": "<username>",
    "password": "<password>"
}
Response: 
{
    "token": "<token>"
}
This endpoint allows a new user to register. The username and password should be sent in the request body. If the registration is successful, a token will be returned in the response.

User Login
Endpoint: /login/
Method: POST
Data Parameters: 
{
    "username": "<username>",
    "password": "<password>"
}
Response: 
{
    "token": "<token>"
}
This endpoint allows a user to log in. The username and password should be sent in the request body. If the login is successful, a token will be returned in the response.

Create a New Section
Endpoint: /api/sections/
Method: POST
Headers: 
{
    "Authorization": "Token <token>"
}
Data Parameters: 
{
    "title": "<title>",
    "root": "<true/false>"
}
Response: 
{
    "id": "<section_id>",
    "title": "<title>",
    "root": "<true/false>"
}
This endpoint allows a user to create a new section. The title and root status should be sent in the request body. The user's token should be included in the Authorization header.

Retrieve a Section
Endpoint: /api/sections/<section_id>/
Method: GET
Headers: 
{
    "Authorization": "Token <token>"
}
Response: 
{
    "id": "<section_id>",
    "title": "<title>",
    "root": "<true/false>",
    "nested_sections": [
        {
            "id": "<nested_section_id>",
            "title": "<nested_section_title>",
            "root": false,
            "parent_section": "<parent_section_id>",
            "content": "<nested_section_content>"
        },
        ...
    ],
    "content": "<section_content>"
}
This endpoint allows a user to retrieve a section. The section ID should be included in the URL. The user's token should be included in the Authorization header.

Update a Section
Endpoint: /api/sections/<section_id>/
Method: PUT
Headers: 
{
    "Authorization": "Token <token>"
}
Data Parameters: 
{
    "title": "<new_title>",
    "root": "<true/false>"
}
Response: 
{
    "id": "<section_id>",
    "title": "<new_title>",
    "root": "<true/false>"
}
This endpoint allows a user to update a section. The new title and root status should be sent in the request body. The section ID should be included in the URL. The user's token should be included in the Authorization header.

Delete a Section
Endpoint: /api/sections/<section_id>/
Method: DELETE
Headers: 
{
    "Authorization": "Token <token>"
}
Response: 
{
    "detail": "Section deleted."
}
This endpoint allows a user to delete a section. The section ID should be included in the URL. The user's token should be included in the Authorization header.

Create a Nested Section
Endpoint: /api/sections/
Method: POST
Headers: 
{
    "Authorization": "Token <token>"
}
Data Parameters: 
{
    "title": "<title>",
    "root": false,
    "parent_section": "<parent_section_id>"
}
Response: 
{
    "id": "<section_id>",
    "title": "<title>",
    "root": false,
    "parent_section": "<parent_section_id>"
}
This endpoint allows a user to create a new nested section under an existing section. The title should be sent in the request body. The root status should be set to false. The ID of the parent section should be included in the parent_section field. The user's token should be included in the Authorization header.

Retrieve All Sections
Endpoint: /api/sections/
Method: GET
Headers: 
{
    "Authorization": "Token <token>"
}
Response: 
{
    "count": <total_number_of_sections>,
    "next": <URL_of_next_page>,
    "previous": <URL_of_previous_page>,
    "results": [
        {
            "id": "<section_id>",
            "title": "<title>",
            "root": "<true/false>",
            "nested_sections": [
                {
                    "id": "<nested_section_id>",
                    "title": "<nested_section_title>",
                    "root": false,
                    "parent_section": "<parent_section_id>",
                    "content": "<nested_section_content>"
                },
                ...
            ],
            "content": "<section_content>"
        },
        ...
    ]
}
This endpoint allows a user to retrieve all sections along with their nested sections. The user's token should be included in the Authorization header. The response includes pagination details. The count field indicates the total number of sections. The next and previous fields provide the URLs of the next and previous pages respectively. The results field contains the list of sections for the current page.

Retrieve Root Sections Only
Endpoint: /api/sections/root_list/
Method: GET
Headers: 
{
    "Authorization": "Token <token>"
}
Response: 
{
    "count": <total_number_of_root_sections>,
    "next": <URL_of_next_page>,
    "previous": <URL_of_previous_page>,
    "results": [
        {
            "id": "<section_id>",
            "title": "<title>",
            "root": true,
            "nested_sections": [
                {
                    "id": "<nested_section_id>",
                    "title": "<nested_section_title>",
                    "root": false,
                    "parent_section": "<parent_section_id>",
                    "content": "<nested_section_content>"
                },
                ...
            ],
            "content": "<section_content>"
        },
        ...
    ]
}
This endpoint allows a user to retrieve only the root sections along with their nested sections. The user's token should be included in the Authorization header. The response includes pagination details. The count field indicates the total number of root sections. The next and previous fields provide the URLs of the next and previous pages respectively. The results field contains the list of lts field contains the list of

Response: 
{
    "count": <total_number_of_sections>,
    "next": <URL_of_next_page>,
    "previous": <URL_of_previous_page>,
    "results": [
        {
            "id": "<section_id>",
            "title": "<title>",
            "root": "<true/false>",
            "nested_sections": [
                {
                    "id": "<nested_section_id>",
                    "title": "<nested_section_title>",
                    "root": false,
                    "parent_section": "<parent_section_id>",
                    "content": "<nested_section_content>"
                },
                ...
            ],
            "content": "<section_content>"
        },
        ...
    ]
}
This endpoint allows a user to retrieve all sections along with their nested sections. The user's token should be included in the Authorization header. The response includes pagination details. The count field indicates the total number of sections. The next and previous fields provide the URLs of the next and previous pages respectively. The results field contains the list of sections for the current page.

## Retrieve Root Sections Only(books)

Endpoint: /api/sections/root_list/
Method: GET
Headers: 
{
    "Authorization": "Token <token>"
}
Response: 
{
    "count": <total_number_of_root_sections>,
    "next": <URL_of_next_page>,
    "previous": <URL_of_previous_page>,
    "results": [
        {
            "id": "<section_id>",
            "title": "<title>",
            "root": true,
            "nested_sections": [
                {
                    "id": "<nested_section_id>",
                    "title": "<nested_section_title>",
                    "root": false,
                    "parent_section": "<parent_section_id>",
                    "content": "<nested_section_content>"
                },
                ...
            ],
            "content": "<section_content>"
        },
        ...
    ]
}
This endpoint allows a user to retrieve only the root sections along with their nested sections. The user's token should be included in the Authorization header. The response includes pagination details. The count field indicates the total number of root sections. The next and previous fields provide the URLs of the next and previous pages respectively. The results field contains the list of root sections for the current page.


