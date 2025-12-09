from asana_teams.constants.exception_messages import (
    TEAM_DOES_NOT_EXIST,
    INVALID_TEAM_GID,
)


class TeamDoesNotExistException(Exception):
    def __init__(self, message=TEAM_DOES_NOT_EXIST):
        self.message = message
        super().__init__(self.message)


class InvalidTeamGidException(Exception):
    def __init__(self, message=INVALID_TEAM_GID):
        self.message = message
        super().__init__(self.message)


class UserDoesNotExistException(Exception):
    def __init__(self, message="User does not exist"):
        self.message = message
        super().__init__(self.message)


class WorkspaceDoesNotExistException(Exception):
    def __init__(self, message="Workspace does not exist"):
        self.message = message
        super().__init__(self.message)

