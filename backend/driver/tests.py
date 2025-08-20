from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from graphene.test import Client
from graphql import GraphQLError
import json

from .models import Driver
from .admin import DriverAdmin
from Project.schema import schema


class DriverModelTest(TestCase):
    """Test cases for Driver model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.driver_data = {
            'name': 'John Doe',
            'phone': '1234567890'
        }
    
    def test_driver_creation(self):
        """Test driver creation with valid data"""
        driver = Driver.objects.create(**self.driver_data)
        self.assertEqual(driver.name, 'John Doe')
        self.assertEqual(driver.phone, '1234567890')
        self.assertTrue(isinstance(driver, Driver))
    
    def test_driver_str_representation(self):
        """Test driver string representation"""
        driver = Driver.objects.create(**self.driver_data)
        self.assertEqual(str(driver), 'John Doe')
    
    def test_driver_creation_without_phone(self):
        """Test driver creation without phone number"""
        driver = Driver.objects.create(name='Jane Doe')
        self.assertEqual(driver.name, 'Jane Doe')
        self.assertIsNone(driver.phone)
    
    def test_driver_creation_with_empty_phone(self):
        """Test driver creation with empty phone number"""
        driver = Driver.objects.create(name='Jane Doe', phone='')
        self.assertEqual(driver.name, 'Jane Doe')
        self.assertEqual(driver.phone, '')
    
    def test_phone_validation_numeric_only(self):
        """Test phone number validation - must be numeric"""
        with self.assertRaises(ValidationError):
            driver = Driver(name='John Doe', phone='123abc7890')
            driver.full_clean()
    
    def test_phone_validation_length(self):
        """Test phone number validation - must be 10 digits"""
        # Test short phone number
        with self.assertRaises(ValidationError):
            driver = Driver(name='John Doe', phone='123456789')
            driver.full_clean()
        
        # Test long phone number
        with self.assertRaises(ValidationError):
            driver = Driver(name='John Doe', phone='12345678901')
            driver.full_clean()
    
    def test_save_method_with_non_numeric_phone(self):
        """Test save method raises error for non-numeric phone"""
        driver = Driver(name='John Doe', phone='123abc7890')
        with self.assertRaises(ValueError) as context:
            driver.save()
        self.assertEqual(str(context.exception), "Phone number must be numeric")
    
    def test_save_method_with_valid_phone(self):
        """Test save method works with valid phone"""
        driver = Driver(name='John Doe', phone='1234567890')
        driver.save()
        self.assertEqual(driver.phone, '1234567890')
    
    def test_driver_update(self):
        """Test updating driver information"""
        driver = Driver.objects.create(**self.driver_data)
        driver.name = 'Jane Smith'
        driver.phone = '0987654321'
        driver.save()
        
        updated_driver = Driver.objects.get(id=driver.id)
        self.assertEqual(updated_driver.name, 'Jane Smith')
        self.assertEqual(updated_driver.phone, '0987654321')
    
    def test_driver_deletion(self):
        """Test driver deletion"""
        driver = Driver.objects.create(**self.driver_data)
        driver_id = driver.id
        driver.delete()
        
        with self.assertRaises(Driver.DoesNotExist):
            Driver.objects.get(id=driver_id)


class DriverAdminTest(TestCase):
    """Test cases for Driver admin"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.site = AdminSite()
        self.admin = DriverAdmin(Driver, self.site)
        self.driver = Driver.objects.create(name='John Doe', phone='1234567890')
    
    def test_list_display(self):
        """Test admin list display fields"""
        expected_fields = ('id', 'name', 'phone')
        self.assertEqual(self.admin.list_display, expected_fields)
    
    def test_admin_string_representation(self):
        """Test admin shows correct string representation"""
        self.assertEqual(str(self.driver), 'John Doe')


class DriverGraphQLQueryTest(TestCase):
    """Test cases for Driver GraphQL queries"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client(schema)
        self.driver1 = Driver.objects.create(name='John Doe', phone='1234567890')
        self.driver2 = Driver.objects.create(name='Jane Smith', phone='0987654321')
        self.driver3 = Driver.objects.create(name='Bob Wilson')  # No phone
    
    def test_all_drivers_query(self):
        """Test querying all drivers"""
        query = '''
            query {
                driver {
                    allDrivers {
                        id
                        name
                        phone
                    }
                }
            }
        '''
        
        result = self.client.execute(query)
        self.assertIsNone(result.get('errors'))
        
        drivers = result['data']['driver']['allDrivers']
        self.assertEqual(len(drivers), 3)
        
        # Check that all drivers are returned
        driver_names = [driver['name'] for driver in drivers]
        self.assertIn('John Doe', driver_names)
        self.assertIn('Jane Smith', driver_names)
        self.assertIn('Bob Wilson', driver_names)
    
    def test_single_driver_query(self):
        """Test querying a single driver"""
        query = '''
            query($id: Int!) {
                driver {
                    driver(id: $id) {
                        id
                        name
                        phone
                    }
                }
            }
        '''
        
        result = self.client.execute(query, variables={'id': self.driver1.id})
        self.assertIsNone(result.get('errors'))
        
        driver = result['data']['driver']['driver']
        self.assertEqual(driver['name'], 'John Doe')
        self.assertEqual(driver['phone'], '1234567890')
        self.assertEqual(driver['id'], str(self.driver1.id))
    
    def test_single_driver_query_not_found(self):
        """Test querying a non-existent driver"""
        query = '''
            query($id: Int!) {
                driver {
                    driver(id: $id) {
                        id
                        name
                        phone
                    }
                }
            }
        '''
        
        result = self.client.execute(query, variables={'id': 9999})
        self.assertIsNotNone(result.get('errors'))
        self.assertIn('Driver with id 9999 not found', str(result['errors']))


class DriverGraphQLMutationTest(TestCase):
    """Test cases for Driver GraphQL mutations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client(schema)
    
    def test_create_driver_basic_structure(self):
        """Test that create driver mutation has correct structure"""
        mutation = '''
            mutation($input: CreateDriverInput!) {
                createDriver(input: $input) {
                    driver {
                        id
                        name
                        phone
                    }
                }
            }
        '''
        
        input_data = {
            'name': 'New Driver',
            'phone': '1234567890'
        }
        
        result = self.client.execute(mutation, variables={'input': input_data})
        
        # We expect an error due to permissions, but the structure should be valid
        if result.get('errors'):
            # Should be permission-related error, not structure error
            error_msg = str(result['errors'][0]['message'])
            self.assertNotIn('Unknown type', error_msg)
            self.assertNotIn('Cannot query field', error_msg)
    
    def test_update_driver_basic_structure(self):
        """Test that update driver mutation has correct structure"""
        mutation = '''
            mutation($id: ID!, $input: UpdateDriverInput!) {
                updateDriver(id: $id, input: $input) {
                    driver {
                        id
                        name
                        phone
                    }
                }
            }
        '''
        
        input_data = {
            'name': 'Updated Name',
        }
        
        result = self.client.execute(mutation, variables={'id': '1', 'input': input_data})
        
        # We expect an error due to permissions, but the structure should be valid
        if result.get('errors'):
            # Should be permission-related error, not structure error
            error_msg = str(result['errors'][0]['message'])
            self.assertNotIn('Unknown type', error_msg)
            self.assertNotIn('Cannot query field', error_msg)
    
    def test_delete_driver_basic_structure(self):
        """Test that delete driver mutation has correct structure"""
        mutation = '''
            mutation($id: ID!) {
                deleteDriver(id: $id) {
                    found
                    deletedId
                }
            }
        '''
        
        result = self.client.execute(mutation, variables={'id': '1'})
        
        # We expect an error due to permissions, but the structure should be valid
        if result.get('errors'):
            # Should be permission-related error, not structure error
            error_msg = str(result['errors'][0]['message'])
            self.assertNotIn('Unknown type', error_msg)
            self.assertNotIn('Cannot query field', error_msg)


class DriverIntegrationTest(TestCase):
    """Integration tests for Driver app"""
    
    def test_driver_lifecycle(self):
        """Test complete driver lifecycle: create, read, update, delete"""
        # Create
        driver = Driver.objects.create(name='Test Driver', phone='1234567890')
        self.assertEqual(Driver.objects.count(), 1)
        
        # Read
        retrieved_driver = Driver.objects.get(id=driver.id)
        self.assertEqual(retrieved_driver.name, 'Test Driver')
        self.assertEqual(retrieved_driver.phone, '1234567890')
        
        # Update
        retrieved_driver.name = 'Updated Driver'
        retrieved_driver.phone = '0987654321'
        retrieved_driver.save()
        
        updated_driver = Driver.objects.get(id=driver.id)
        self.assertEqual(updated_driver.name, 'Updated Driver')
        self.assertEqual(updated_driver.phone, '0987654321')
        
        # Delete
        updated_driver.delete()
        self.assertEqual(Driver.objects.count(), 0)
    
    def test_multiple_drivers_creation(self):
        """Test creating multiple drivers"""
        drivers_data = [
            {'name': 'Driver 1', 'phone': '1111111111'},
            {'name': 'Driver 2', 'phone': '2222222222'},
            {'name': 'Driver 3'},  # No phone
        ]
        
        for data in drivers_data:
            Driver.objects.create(**data)
        
        self.assertEqual(Driver.objects.count(), 3)
        
        # Test filtering
        drivers_with_phone = Driver.objects.exclude(phone__isnull=True).exclude(phone='')
        self.assertEqual(drivers_with_phone.count(), 2)
        
        drivers_without_phone = Driver.objects.filter(phone__isnull=True)
        self.assertEqual(drivers_without_phone.count(), 1)
