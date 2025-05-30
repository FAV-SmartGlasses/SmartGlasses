import json
import os
from dataclasses import dataclass, asdict, field
from enum import IntEnum


class Theme(IntEnum):
    LIGHT = 0
    DARK = 1
    CUSTOM = 2

class Language(IntEnum):
    ENGLISH = 0
    CZECH = 1

class KeyboardLayout(IntEnum):
    QWERTY_ENGLISH = 0
    QWERTZ_ENGLISH = 1
    QWERTY_CZECH = 2
    QWERTZ_CZECH = 3

class WIFI:
    def __init__(self, name, password):
        self.name = name
        self.password = password

@dataclass
class SettingsModel:
    theme: Theme = Theme.LIGHT
    custom_theme_font_color: tuple = (0,0,0)
    custom_theme_nice_color: tuple = (0,0,0)
    custom_theme_neutral_color: tuple = (0,0,0)
    custom_theme_neutral_color2: tuple = (0,0,0)

    language: Language = Language.ENGLISH
    saved_wifi: dict = field(default_factory=dict)
    saved_bluetooth_devices: dict = field(default_factory=dict)
    airplane_mode_ON: bool = False
    bluetooth_ON: bool = True
    wifi_ON: bool = True
    keyboard_layout: KeyboardLayout = KeyboardLayout.QWERTY_ENGLISH
    volume: int = 50  # (0-100)
    microphone_ON: bool = True
    brightness: int = 50  # (0-100)
    assistant_ON: bool = True
    GPS_ON: bool = True
    apps_transparency: float = 0.5 # (0-1)
    discord_api_ip: str = "127.0.0.1:8080"
    discord_name: str = "OptiForge user"
    discord_pfp_url: str = "https://avatars.githubusercontent.com/u/189787689?s=96&v=4"
    # TODO: implementation of other headset settings


_settings_file = "../resources/settings.json"  # saves JSON into folder AR
_settings = SettingsModel()


def load_settings():
    global _settings

    if os.path.exists(_settings_file):
        try:
            with open(_settings_file, "r") as file:
                data = json.load(file)
                #_settings = Settings(**data)
                _settings = SettingsModel(
                    theme=Theme(data["theme"]),
                    custom_theme_font_color=tuple(data["custom_theme_font_color"]),
                    custom_theme_nice_color=tuple(data["custom_theme_nice_color"]),
                    custom_theme_neutral_color=tuple(data["custom_theme_neutral_color"]),
                    custom_theme_neutral_color2=tuple(data["custom_theme_neutral_color2"]),

                    language=Language(data["language"]),
                    keyboard_layout=KeyboardLayout(data["keyboard_layout"]),
                    **{k: v for k, v in data.items() if k not in {
                        "theme",
                        "custom_theme_font_color", "custom_theme_nice_color",
                        "custom_theme_neutral_color", "custom_theme_neutral_color2",
                        "language", "keyboard_layout"
                    }}
                )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error loading settings: {e}. Creating default settings.")
            save_settings()
    else:
        save_settings()  # Save default settings if file doesn't exist

def save_settings():
    with open(_settings_file, "w") as file:
        json.dump(asdict(_settings), file, indent=4)

def get_settings():
    load_settings()
    return _settings

def set_settings(**kwargs):
    for key, value in kwargs.items():
        if hasattr(_settings, key):
            setattr(_settings, key, value)
    save_settings()

def get_theme():
    load_settings()
    return _settings.theme

def get_custom_theme_font_color():
    load_settings()
    return _settings.custom_theme_font_color

def get_custom_theme_nice_color():
    load_settings()
    return _settings.custom_theme_nice_color

def get_custom_theme_neutral_color():
    load_settings()
    return _settings.custom_theme_neutral_color

def get_custom_theme_neutral_color2():
    load_settings()
    return _settings.custom_theme_neutral_color2

def get_app_transparency():
    load_settings()
    return _settings.apps_transparency
