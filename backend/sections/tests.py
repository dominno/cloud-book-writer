from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Section
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

class SectionTestCase(TestCase):

    @override_settings(CLOUD_STORAGE_CLASS="sections.storage_backend.LocalCloudStorageBackend")
    def setUp(self):        
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.collaborator_group = Group.objects.get(name='Collaborators')
        self.author_group = Group.objects.get(name='Authors')
        self.user.groups.add(self.author_group)
        
        self.client.login(username='testuser', password='testpass')
        self.section = Section.objects.create(title='Test Section', author=self.user, root=True)

    def test_create_section(self):
        response = self.client.post('/api/sections/', {'title': 'New Section', 'root': True})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'New Section')

    def test_get_section(self):
        response = self.client.get(f'/api/sections/{self.section.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Section')

    def test_update_section(self):
        response = self.client.put(f'/api/sections/{self.section.id}/', {'title': 'Updated Section', 'root': True})
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.content}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Section')

    def test_delete_section(self):
        self.user.groups.clear()
        self.user.groups.add(self.author_group)
        response = self.client.delete(f'/api/sections/{self.section.id}/')
        self.assertEqual(response.status_code, 204)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.post('/api/sections/', {'title': 'New Section', 'root': True})
        self.assertEqual(response.status_code, 403)
    
    def test_get_non_existent_section(self):
        response = self.client.get('/api/sections/9999/')
        self.assertEqual(response.status_code, 404)

    def test_create_section_with_invalid_data(self):
        response = self.client.post('/api/sections/', {'title': '', 'root': True})
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_root_section_displays_nested_sections(self):
        # Create a nested section
        nested_section = Section.objects.create(title='Nested Section', author=self.user, root=False, parent_section=self.section)

        # Fetch the root section
        response = self.client.get(f'/api/sections/{self.section.id}/')

        # Check if the nested section is present in the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('nested_sections', response.data)
        self.assertTrue(any(section['id'] == nested_section.id for section in response.data['nested_sections']))

    def test_collaborator_can_edit_section(self):
        # Create a collaborator user
        collaborator = get_user_model().objects.create_user(username='collaborator', password='testpass')
        collaborator.groups.add(self.collaborator_group)

        # Add the collaborator to the section's collaborators
        self.section.collaborators.add(collaborator)

        # Log in as the collaborator
        self.client.login(username='collaborator', password='testpass')

        # Attempt to edit the section
        response = self.client.put(f'/api/sections/{self.section.id}/', {'title': 'Updated by Collaborator'})

        # Check if the edit was successful
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(response.data['title'], 'Updated by Collaborator')

    def test_collaborator_cannot_create_section(self):
        # Create a collaborator user
        collaborator = get_user_model().objects.create_user(username='collaborator', password='testpass')
        collaborator.groups.add(self.collaborator_group)

        # Log in as the collaborator
        self.client.login(username='collaborator', password='testpass')

        # Attempt to create a new section
        response = self.client.post('/api/sections/', {'title': 'New Section', 'root': True})

        # Check if the creation was unsuccessful
        self.assertNotEqual(response.status_code, 201)

    def test_collaborator_cannot_delete_section(self):
        # Create a collaborator user
        collaborator = get_user_model().objects.create_user(username='collaborator', password='testpass')
        collaborator.groups.add(self.collaborator_group)

        # Add the collaborator to the section's collaborators
        self.section.collaborators.add(collaborator)

        # Log in as the collaborator
        self.client.login(username='collaborator', password='testpass')

        # Attempt to delete the section
        response = self.client.delete(f'/api/sections/{self.section.id}/')

        # Check if the deletion was unsuccessful
        self.assertNotEqual(response.status_code, 204)

    def test_section_ownership(self):
        response = self.client.post('/api/sections/', {'title': 'New Section', 'root': True})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], self.user.id)
    
    def test_non_collaborator_cannot_update_section(self):
        non_collaborator = get_user_model().objects.create_user(username='noncollaborator', password='testpass')
        self.client.login(username='noncollaborator', password='testpass')
        response = self.client.put(f'/api/sections/{self.section.id}/', {'title': 'Updated by Non-Collaborator'})
        self.assertNotEqual(response.status_code, 200)

    def test_get_section_detail(self):
        response = self.client.get(f'/api/sections/{self.section.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.section.id)

    def test_author_can_add_collaborators_to_root_section(self):
        # Create a collaborator user
        collaborator = get_user_model().objects.create_user(username='collaborator', password='testpass')
        collaborator.groups.add(self.collaborator_group)

        # Log in as the author
        self.client.login(username='testuser', password='testpass')

        # Attempt to add the collaborator to the root section
        response = self.client.patch(f'/api/sections/{self.section.id}/', {'collaborators': [collaborator.id]}, format='json')

        # Check if the operation was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(collaborator.id, response.data['collaborators'])




class UserRegistrationLoginTest(APITestCase):
    def test_user_can_register(self):
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, 'testuser')

    def test_user_can_login(self):
        get_user_model().objects.create_user(username='testuser', password='testpass')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertIn('token', response.data)


class RootSectionCreationAuthTokenTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.author_group = Group.objects.get(name='Authors')
        self.user.groups.add(self.author_group)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_can_add_root_section(self):
        data = {'title': 'Root Section', 'root': True}
        response = self.client.post(reverse('section-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Root Section')
        self.assertEqual(response.data['root'], True)