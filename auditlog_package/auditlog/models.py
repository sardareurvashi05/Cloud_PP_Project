from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import json

class Audit_Log(models.Model):
    """
    Model to store audit logs of actions performed on objects within the application.

    Attributes:
        action_type (str): A string representing the type of action (e.g., 'create', 'update', 'delete').
        user (User, optional): The user who performed the action. Can be null if no user is associated.
        object_type (str): The type of object on which the action was performed (e.g., 'Product', 'Order').
        object_id (int): The ID of the object being acted upon.
        timestamp (datetime): The timestamp of when the action occurred.
        details (JSON): A JSON object to store additional details about the action.
    """
    action_type = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    object_type = models.CharField(max_length=255)
    object_id = models.AutoField(primary_key=True) 
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.action_type} - {self.object_type} ({self.object_id}) - {self.timestamp}"

    @property
    def object(self):
        """
        Dynamically return the object related to this audit log entry.
        If the object_type corresponds to a Django model, it attempts to retrieve the object.
        """
        try:
            content_type = ContentType.objects.get(model=self.object_type.lower())
            model_class = content_type.model_class()
            return model_class.objects.get(id=self.object_id)
        except (ContentType.DoesNotExist, model_class.DoesNotExist):
            return None