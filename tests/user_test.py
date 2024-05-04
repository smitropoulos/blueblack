import pytest
import requests_mock

from blueblack.user import User, UserRepository, UserService


@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def user_repository(mock_api):
    base_url = "https://api.example.com"
    repo = UserRepository(base_url)
    return repo


@pytest.mark.parametrize(
    "user_id, fake_response_data",
    [
        (1, {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}),
        (2, {"id": 2, "name": "Jane Doe", "email": "jane.doe@example.com"}),
    ],
)
def test_get_user_by_id(user_id, fake_response_data, mock_api, user_repository):
    # Register the mock API call with the correct URL and response data
    mock_api.get(f"https://api.example.com/users/{user_id}", json=fake_response_data)

    # Initialize the UserService with the UserRepository
    user_service = UserService(user_repository)

    # Call the get_user_by_id function with the given user_id
    user = user_service.get_user_by_id(user_id)

    # Assert that the returned user is correct
    assert user.id == fake_response_data["id"]
    assert user.name == fake_response_data["name"]
    assert user.email == fake_response_data["email"]
