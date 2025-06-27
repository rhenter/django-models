import os
import sys
import django
import pytest

# Add the project path to sys.path
sys.path.insert(0, '/Users/rafael.henter.br/workspace/personal/django-models')
sys.path.insert(0, '/Users/rafael.henter.br/workspace/personal/django-models/test-django-project')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_django_project.settings')
django.setup()

from testapp.models import SampleSignalsModel

@pytest.mark.django_db
def test_context_passing():
    print("Testing context passing in SignalsModel...")

    # Test creation
    print("\n=== Testing object creation ===")
    obj = SampleSignalsModel(name='test context')

    # Store original methods
    original_pre_save = obj.pre_save
    original_post_save = obj.post_save

    # Track context
    context_received = {
        'pre_save': None,
        'post_save': None,
    }

    def custom_pre_save(context):
        print(f"pre_save called with context: {context}")
        context_received['pre_save'] = context
        original_pre_save(context)

    def custom_post_save(context):
        print(f"post_save called with context: {context}")
        context_received['post_save'] = context
        original_post_save(context)

    # Replace methods
    obj.pre_save = custom_pre_save
    obj.post_save = custom_post_save

    obj.save()

    print(f"Pre-save context: {context_received['pre_save']}")
    print(f"Post-save context: {context_received['post_save']}")

    # Test update
    print("\n=== Testing object update ===")
    obj.name = 'updated name'
    obj.save()

    print(f"Pre-save context after update: {context_received['pre_save']}")
    print(f"Post-save context after update: {context_received['post_save']}")

    # Check if context is None (which would indicate the issue)
    if context_received['pre_save'] is None:
        print("ERROR: pre_save context is None!")
    if context_received['post_save'] is None:
        print("ERROR: post_save context is None!")

    print(f"\nDebug info: {obj.debug_info}")

if __name__ == '__main__':
    test_context_passing()
