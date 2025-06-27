import pytest

from testapp.models import SampleSignalsModel

pytestmark = pytest.mark.django_db


def test_context_passing_detailed():
    """Test that context is properly passed to pre_save and post_save methods."""

    # Track context
    context_received = {
        "pre_save": None,
        "post_save": None,
    }

    # Create object
    obj = SampleSignalsModel(name="test context")

    # Store original methods
    original_pre_save = obj.pre_save
    original_post_save = obj.post_save

    def custom_pre_save(context):
        print(f"pre_save called with context: {context}")
        context_received["pre_save"] = context
        original_pre_save(context)

    def custom_post_save(context):
        print(f"post_save called with context: {context}")
        context_received["post_save"] = context
        original_post_save(context)

    # Replace methods
    obj.pre_save = custom_pre_save
    obj.post_save = custom_post_save

    # Test creation
    obj.save()

    # Verify context was passed
    assert (
        context_received["pre_save"] is not None
    ), "pre_save context should not be None"
    assert (
        context_received["post_save"] is not None
    ), "post_save context should not be None"

    # Verify context content
    assert (
        "is_creation" in context_received["pre_save"]
    ), "Context should contain 'is_creation'"
    assert (
        context_received["pre_save"]["is_creation"] is True
    ), "is_creation should be True for new objects"

    assert (
        "is_creation" in context_received["post_save"]
    ), "Context should contain 'is_creation'"
    assert (
        context_received["post_save"]["is_creation"] is True
    ), "is_creation should be True for new objects"

    print(f"Pre-save context: {context_received['pre_save']}")
    print(f"Post-save context: {context_received['post_save']}")

    # Test update
    obj.name = "updated name"
    obj.save()

    # Verify context for update
    assert (
        context_received["pre_save"]["is_creation"] is False
    ), "is_creation should be False for updates"
    assert (
        context_received["post_save"]["is_creation"] is False
    ), "is_creation should be False for updates"

    print(f"Pre-save context after update: {context_received['pre_save']}")
    print(f"Post-save context after update: {context_received['post_save']}")
