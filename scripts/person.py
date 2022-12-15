from dataclasses import dataclass


@dataclass
class Person:
    name: str
    email: str
    pronoun: str
    groups: set[str]

    @staticmethod
    def from_json(j):
        return Person(
            j['name'], j['email'], j['pronoun'], set(j['groups'])
        )

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return self.name