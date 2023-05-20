from hashlib import sha256


class User:
    def __init__(self, *, login: str = None, password: str = None, name: str = None,
                 second_name: str = None, role: str = None, id: str = None):
        self.login = login
        self.hash_password = sha256(password.encode('utf-8')).hexdigest()
        self.name = name
        self.second_name = second_name
        self.role = role
        self.id = id

    def to_json(self) -> dict[str, str]:
        return {
            'name': self.name,
            'second_name': self.second_name,
            'role': self.role,
            'id': self.id
        }

    def str_to_gen_id(self) -> str:
        return f'{self.login}{self.hash_password}{self.name}{self.second_name}{self.role}'

    def __eq__(self, other):
        if not isinstance(other, User):
            return False

        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
