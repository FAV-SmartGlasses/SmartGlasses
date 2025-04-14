from settings_manager import SettingsManager, Theme


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (248, 255, 145) #(238, 255, 0)
DARK_BLUE = (140, 0, 10)
LIGHT_GRAY = (200, 200, 200)

def get_font_color():
    theme = SettingsManager.get_theme()
    if theme == Theme.LIGHT:
        return BLACK
    elif theme == Theme.DARK:
        return WHITE
    elif theme == Theme.CUSTOM:
        return SettingsManager.get_custom_theme_font_color()
    else:
        raise ValueError(f"Unknown theme: {theme}")

def get_nice_color():
    theme = SettingsManager.get_theme()
    if theme == Theme.LIGHT:
        return LIGHT_BLUE
    elif theme == Theme.DARK:
        return DARK_BLUE
    elif theme == Theme.CUSTOM:
        return SettingsManager.get_custom_theme_nice_color()
    else:
        raise ValueError(f"Unknown theme: {theme}")

def get_neutral_color():
    theme = SettingsManager.get_theme()
    if theme == Theme.LIGHT:
        return WHITE
    elif theme == Theme.DARK:
        return BLACK
    elif theme == Theme.CUSTOM:
        return SettingsManager.get_custom_theme_neutral_color()
    else:
        raise ValueError(f"Unknown theme: {theme}")

def get_neutral_color2():
    theme = SettingsManager.get_theme()
    if theme == Theme.LIGHT:
        return BLACK
    elif theme == Theme.DARK:
        return WHITE
    elif theme == Theme.CUSTOM:
        return SettingsManager.get_custom_theme_neutral_color2()
    else:
        raise ValueError(f"Unknown theme: {theme}")