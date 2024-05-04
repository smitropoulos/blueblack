import requests


class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(id=json_data["id"], name=json_data["name"], email=json_data["email"])


class UserRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user(self, user_id: int) -> User:
        response = requests.get(f"{self.base_url}/users/{user_id}")

        if response.status_code == 200:
            return User.from_json(response.json())
        else:
            raise Exception("Failed to fetch user data.")


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user(user_id)
