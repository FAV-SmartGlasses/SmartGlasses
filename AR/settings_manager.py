from enum import Enum, IntEnum
from dataclasses import dataclass, asdict, field
import json
from pathlib import Path

class Theme(IntEnum):
    LIGHT = 0
    DARK = 1

class Language(IntEnum):
    ENGLISH = 0
    CZECH = 1

class KeyboardLayout(IntEnum):
    QWERTY_ENGLISCH = 0
    AZERTY_ENGLISCH = 1
    QWERTZ_ENGLISCH = 2
    QWERTY_CZECH = 4
    AZERTY_CZECH = 5
    QWERTZ_CZECH = 6

class WIFI:
    def __init__(self, name, password):
        self.name = name
        self.password = password

@dataclass
class Settings:
    theme: Theme = Theme.LIGHT
    language: Language = Language.ENGLISH
    saved_wifi: dict = field(default_factory=dict)
    saved_bluetooth_devices: dict = field(default_factory=dict)
    airplane_mode_ON: bool = False
    bluetooth_ON: bool = True
    wifi_ON: bool = True
    keyboard_layout: KeyboardLayout = KeyboardLayout.QWERTY_ENGLISCH
    volume: int = 50  # (0-100)
    microfon_ON: bool = True
    brightness: int = 50  # (0-100)
    assistent_ON: bool = True
    GPS_ON: bool = True
    # TODO: implementation of other headset settings

class SettingsManager:
    _settings_file = Path(__file__).parent / "settings.json"  # saves JSON into folder AR
    _settings = Settings()

    @staticmethod
    def load_settings():
        if SettingsManager._settings_file.exists():
            try:
                with open(SettingsManager._settings_file, "r") as file:
                    data = json.load(file)
                    #SettingsManager._settings = Settings(**data)
                    SettingsManager._settings = Settings(
                        theme=Theme(data["theme"]),
                        language=Language(data["language"]),
                        keyboard_layout=KeyboardLayout(data["keyboard_layout"]),
                        **{k: v for k, v in data.items() if k not in {"theme", "language", "keyboard_layout"}}
                    )
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error loading settings: {e}. Creating default settings.")
                SettingsManager.save_settings()  # Uloží výchozí nastavení
        else:
            SettingsManager.save_settings()  # Save default settings if file doesn't exist

    @staticmethod
    def save_settings():
        with open(SettingsManager._settings_file, "w") as file:
            json.dump(asdict(SettingsManager._settings), file, indent=4)

    @staticmethod
    def get_settings():
        SettingsManager.load_settings()
        return SettingsManager._settings

    @staticmethod
    def set_settings(**kwargs):
        for key, value in kwargs.items():
            if hasattr(SettingsManager._settings, key):
                setattr(SettingsManager._settings, key, value)
        SettingsManager.save_settings()
