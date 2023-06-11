import pytest

from buzzbrewclub.users.forms import UserCreationForm
from buzzbrewclub.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserCreationForm:

    def test_clean_username(self):
        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()

        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": "H0-#nt3r2",
                "password2": "H0-#nt3r2",
            }
        )

        assert form.is_valid(), str(form.errors)
        assert form.clean_username() == proto_user.username

        # Creating a user.
        form.save()

        # The user with proto_user params already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": "H0-#nt3r2",
                "password2": "H0-#nt3r2",
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors
