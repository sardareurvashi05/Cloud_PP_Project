from django.test import TestCase
from django.contrib.auth.models import User
from auditlog.decorators import audit_log
from auditlog.models import Audit_Log
from unittest.mock import patch


class AuditLogDecoratorTest(TestCase):

    def setUp(self):
        # Set up a user instance for testing
        self.user = User.objects.create_user(username='testuser', password='password')

    @patch('your_app.decorators.Audit_Log.objects.create')
    def test_audit_log_decorator(self, mock_create):
        """
        Test the `audit_log` decorator to ensure it logs the action correctly.
        """
        # Define a sample function to test the decorator
        @audit_log(action_type='update', object_type='Product', user=self.user)
        def update_product(request, object_id):
            return "Product Updated"
        
        # Simulate calling the function
        update_product(None, object_id=1)
        
        # Verify that Audit_Log.objects.create was called
        mock_create.assert_called_once_with(
            action_type='update',
            user=self.user,
            object_type='Product',
            object_id=1,
            details={'object_id': 1}
        )
    
    @patch('your_app.decorators.Audit_Log.objects.create')
    def test_audit_log_decorator_with_no_user(self, mock_create):
        """
        Test the `audit_log` decorator when no user is provided.
        """
        # Define a sample function to test the decorator
        @audit_log(action_type='delete', object_type='Order', user=None)
        def delete_order(request, object_id):
            return "Order Deleted"
        
        # Simulate calling the function
        delete_order(None, object_id=2)
        
        # Verify that Audit_Log.objects.create was called with user as None
        mock_create.assert_called_once_with(
            action_type='delete',
            user=None,
            object_type='Order',
            object_id=2,
            details={'object_id': 2}
        )
