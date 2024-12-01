from django.test import TestCase
from django.contrib.auth.models import User
from auditlog.models import Audit_Log
from django.utils import timezone

class AuditLogModelTest(TestCase):
    
    def setUp(self):
        # Set up a user instance for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        # Set up an Audit_Log instance for testing
        self.audit_log = Audit_Log.objects.create(
            action_type='create',
            user=self.user,
            object_type='Product',
            object_id=1,
            details={"name": "Product1", "price": 100},
            timestamp=timezone.now()
        )

    def test_audit_log_creation(self):
        # Test that an Audit_Log is created correctly
        log = Audit_Log.objects.first()
        self.assertEqual(log.action_type, 'create')
        self.assertEqual(log.user.username, 'testuser')
        self.assertEqual(log.object_type, 'Product')
        self.assertEqual(log.object_id, 1)
        self.assertEqual(log.details, {"name": "Product1", "price": 100})
        self.assertTrue(isinstance(log.timestamp, timezone.datetime))
    
    def test_audit_log_str_method(self):
        # Test the __str__ method
        log = self.audit_log
        expected_str = f"create - Product (1) - {log.timestamp}"
        self.assertEqual(str(log), expected_str)