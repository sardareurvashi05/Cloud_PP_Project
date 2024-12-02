# Django Audit Log

A simple Django package for logging user actions on objects within the application.

## Installation

Install via pip:

pip install audit-trail-logger

1. Add auditlog to INSTALLED_APPS in your Django settings. 
2. Use the audit_log decorator on your views or model methods.
    from auditlog.decorators import audit_log 
    @audit_log(action_type='create', object_type='Product') 
    def create_product(request): 
        ## Your logic for creating the product pass