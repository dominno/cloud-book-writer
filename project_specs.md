Cloud Book Writer Platform

User Stories

1. Unlimited Sections and Subsections
- As a user, I want to be able to create new book. Book is Section object field root=True. Backend should use cloud storage abstraction backend, Django model need to store url to the file.
- As a user, I want to be able to create an unlimited number of sections within my book so that I can organize my content effectively.
- As a user, I want to be able to create multiple subsections within each section, and further child subsections within those, to any level of nesting, so that I can structure my book in a detailed and hierarchical manner.
- As a User I want to be able to read Section hierarchy from root element to bottom elements. Titles are stored in database, content is stored in the cloud storage in nested structure. Use cloud storage abstraction backend to read content data from storage.

2. User Authentication
- As a user, I want to be able to register and create an account on the platform so that I can have a personalized space for my work. 
- As a user, I want to be able to log in securely to my account so that I can access my work and ensure its safety.

3. Permissions & Roles
- As an Author, I want to be the only one who can create new sections and subsections in my book so that I can maintain control over the structure of my book.
- As an Author or a Collaborator, I want to be able to edit sections and subsections so that I can contribute to the content of the book.
- As an Author, I want to be able to grant or revoke access to specific Collaborators so that I can manage who can contribute to my book.

Backend Requirements

1. Python Version: Use Python 3.9 for the backend development.

2. Framework: Use Django 4.2 as the primary framework for backend development.

3. API: Implement the API using Django Rest Framework.

4. Database: Use SQLite as the database for storing data.

5. Coding Style: Follow PEP-8 coding style guidelines for writing Python code.

6. Unit Tests: Write unit tests for all API endpoints to ensure they work as expected.

7. API Documentation: Document the API endpoints clearly, explaining what each endpoint does, the required parameters, and the response format. This will help frontend developers understand how to interact with the API.

8. Cloud Storage Abstraction: Create a cloud storage abstraction backend API proxy. For testing, it should be able to read and write files from the local disk. Include an example in the documentation on how to use the cloud storage abstraction backend with the boto3 library instead of the localhost provider. The unit tests should use the localhost cloud storage abstraction backend.

9.  How creation of new section works on backend.
	Database Structure:
	- Create a Section model in your Django application's models.py file to represent a section. The model should have fields such as title, author, parent_section, 		and root.
	- The parent_section field is a foreign key to the Section model itself, representing the parent section if any. It allows for the creation of nested sections.
	- The root field is a boolean field that indicates whether the section is the root section of a book. By default, it is set to False.

	Adding Sections:
	- When a user wants to add a new section to a book, create a new instance of the Section model and set its title, author, parent_section, 			and root fields accordingly.
	- Save the new section to the database using the Django ORM.
	- Ensure that the section is associated with the correct parent_section and

	Cloud Storage:
	- When a new section is added, create a corresponding folder in the cloud storage system to represent the section and file content.txt with section content.
	- folder name can be derived from the section's title as slugified string
	- create a folder structure that mirrors the section hierarchy.
	- Store the section content such as text within the corresponding folder in the cloud storage system.
10. User Authentication: Implement user authentication using the built-in authentication system of Django Rest Framework.



