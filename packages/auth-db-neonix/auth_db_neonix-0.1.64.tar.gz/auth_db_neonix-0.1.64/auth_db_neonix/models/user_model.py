from .settings_base_class import SettingsBaseClass as User_setting
from ..dto.user_dto import User_Dto_as_Dict
from ..services.settings_factory import settings_from_dict


# region TODOs for future implementations:
# TODO [ ] Add validation logic for profile fields (username, email)
# TODO [ ] Implement methods to serialize/deserialize user data
# TODO [ ] Handle JWT and refresh token expiration automatically
# TODO [ ] Add method to load/save user settings from external source
# TODO [ ] Consider converting to a dataclass for simplicity
# endregion


class User:
    """
    Represents a user object with profile info, authentication tokens, and settings.
    """

    def __init__(self):
        self.profile: dict = {"Username": None, "Email": None}
        """User profile information as dictionary."""

        self.userId: str = None
        """Unique user identifier (Firebase UID)."""

        self.jwt: str = None
        """JWT (ID token) returned by Firebase during login."""

        self.settings: list[User_setting] = []
        """List of user-specific settings objects."""

    @staticmethod
    def from_dto(user: User_Dto_as_Dict, jwt):
        user_instance: User = User()
        user_instance.profile = {"Username": user["Username"], "Email": user["Email"]}
        user_instance.userId = user["UserId"]
        user_instance.jwt = jwt
        user_instance.settings = [settings_from_dict(val) for val in user["Settings"]]
        return user_instance

    def to_dto(self):
        list_of_settings: [dict] = [val.to_dict for val in self.settings]
        user_dto = User_Dto_as_Dict()
        user_dto["Username"] = self.profile["Username"]
        user_dto["Email"] = self.profile["Email"]
        user_dto["UserId"] = self.userId
        user_dto["Settings"] = list_of_settings
        return user_dto
