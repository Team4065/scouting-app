from dataclasses import dataclass, field

@dataclass
class User:
    """ Represents the data associated with a user. """
    uid: str
    username: str
    email: str
