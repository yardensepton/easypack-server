class UserNotFoundError(Exception):
    def __init__(self, user_id):
        super().__init__(f"User '{user_id}' not found")