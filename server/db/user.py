class User:
    def __init__(self, *, login: str = None, password: str = None, name: str = None,
                 second_name: str = None, role: str = None, _id: int = None):
        self.login = login
        self.password = password
        self.name = name
        self.second_name = second_name
        self.role = role
        self.id = _id

    def to_json(self) -> dict[str, str]:
        return {
            'name': self.name,
            'second_name': self.second_name,
            'role': self.role,
            'id': self.id
        }
