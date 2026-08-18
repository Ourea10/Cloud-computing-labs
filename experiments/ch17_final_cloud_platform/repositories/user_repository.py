class UserRepository:

    def __init__(self):

        self.users = {}

    def create(self, user):

        self.users[user.id] = user

        return user

    def find_by_email(
        self,
        email: str,
    ):

        for user in self.users.values():

            if user.email == email:

                return user

        return None

    def get(self, user_id: str):

        return self.users.get(
            user_id
        )