from ..models.user_settings_models import DbSetting, SocketSettings
from ..models.settings_base_class import SettingsBaseClass, SettingsTypeEnum


def settings_from_dict(record: dict) -> SettingsBaseClass:
    raw_type = record["Type"]
    # TODO costretto a rimuovere il parametro type per brutta architettura dei settings
    record = record.pop("Type", None)

    if isinstance(raw_type, str):
        setting_type = SettingsTypeEnum[raw_type] if not raw_type.isdigit() else SettingsTypeEnum(int(raw_type))
    elif isinstance(raw_type, int):
        setting_type = SettingsTypeEnum(raw_type)
    else:
        raise ValueError(f"Invalid Type: {raw_type}")

    type_map = {
        SettingsTypeEnum.SOCKET: SocketSettings,
        SettingsTypeEnum.PATH: DbSetting,
        # aggiungi le altre
    }

    cls = type_map.get(setting_type)
    if not cls:
        raise ValueError(f"No subclass for setting type {setting_type}")

    return cls.from_dict(record)
