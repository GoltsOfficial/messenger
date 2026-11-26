from repositories.users import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_all(self):
        return self.repo.list_all()
