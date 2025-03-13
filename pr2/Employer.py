from State import State


class Employer:
    def __init__(self, name: str, average_score: float,
                 verifications: list, tags: list, state: State):
        self.name = name
        self.average_score = average_score
        self.verifications = verifications
        self.tags = tags
        self.id = state.employers_last_id

        state.employers_last_id += 1
